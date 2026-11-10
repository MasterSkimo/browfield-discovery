"""Test the structural brownfield handoff quality gate on synthetic checkouts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_discovery.py")
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

OUTPUTS = {
    "agent_instructions": "AGENTS.md",
    "architecture": ".agent-context/architecture.md",
    "execution": ".agent-context/execution.md",
    "dependencies": ".agent-context/dependencies.md",
    "e2e_inventory": ".agent-context/e2e-inventory.md",
    "unknowns": ".agent-context/unknowns.md",
    "verification_contract": ".agent-context/verification-contract.md",
}


def make_fixture(root: Path) -> dict:
    """Create plausible source evidence and an actionable AGENTS.md."""
    (root / "pom.xml").write_text("<project />\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src/Controller.java").write_text("class Controller {}\n", encoding="utf-8")
    tick = chr(96)
    sections = {
        "Project overview": "This fixture is a Maven Java API. The root pom.xml is the build entry and the source controller belongs to the backend.",
        "Repository map": "The root pom.xml defines the backend and src/Controller.java shows the HTTP entry. No frontend exists in this sample.",
        "Setup commands": f"From root, declared not executed: {tick}mvn dependency:resolve{tick}. Requires JDK and Maven; validate version locally.",
        "Build and run": f"From root, declared not executed: {tick}mvn package{tick}. Check plugin configuration for the startup procedure.",
        "Tests and quality checks": f"From root, declared but not executed: {tick}mvn test{tick}. Check test sources and CI configuration before handoff.",
        "Architecture and code conventions": "Controller code is under src/Controller.java. Follow established Java package organization and validation conventions.",
        "Security and data handling": "Use only environment variable names, no credentials. Determine test role requirements from application auth code and fixtures.",
        "First autonomous mission: E2E characterization": "Run the real application, Docker databases and brokers, stub outside-application services, then exercise real API with Newman assertions.",
        "Evidence and delivery": "Every acceptance criterion links implementation, automated assertion, command, environment, run artifact and pass/fail status.",
        "Detailed reference material": "See .agent-context/e2e-inventory.md for candidate journeys, architecture.md for topology and verification-contract.md for proof requirements.",
    }
    text = "# AGENTS.md — Sample API\n\n" + "\n\n".join(f"## {title}\n{body}" for title, body in sections.items())
    (root / "AGENTS.md").write_text(text, encoding="utf-8")
    for name, path in OUTPUTS.items():
        if name == "agent_instructions":
            continue
        f = root / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# Context\nInspected code reference from pom.xml.\n", encoding="utf-8")
    manifest = {
        "schema_version": "0.1.0",
        "repository": {"name": "sample", "revision": "0123456789abcdef", "analyzed_at": "2026-11-10T10:00:00Z"},
        "status": "ready_for_e2e_setup", "outputs": OUTPUTS,
        "findings": [{"id": "ARC-1", "statement": "Maven build", "confidence": "verified",
                      "sources": [{"path": "pom.xml", "locator": "root"}]},
                     {"id": "APP-1", "statement": "Backend entry", "confidence": "inferred",
                      "reasoning": "The controller source and Maven file suggest a JVM API.",
                      "sources": [{"path": "src/Controller.java", "locator": "class"}]}],
        "next_actions": [],
    }
    (root / ".agent-context/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return manifest


class GateTests(unittest.TestCase):
    """Prevent empty indexes, claims without sources and uninvestigated UNKNOWNs."""

    def test_good_package_passes(self) -> None:
        # Legitimate source-backed operational instructions clear the gate.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            self.assertEqual([], gate.collect_problems(root))
            self.assertEqual(0, gate.main(["--project", str(root)]))

    def test_link_only_agents_md_fails(self) -> None:
        # Merely pointing to architecture documents cannot be considered complete.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            (root / "AGENTS.md").write_text("# AGENTS.md\nSee .agent-context/architecture.md\n", encoding="utf-8")
            self.assertTrue(any("missing or empty" in x for x in gate.collect_problems(root)))

    def test_unexplained_unknown_fails_then_passes_with_evidence(self) -> None:
        # Record a bounded hypothesis and actual search trail before escalation.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = make_fixture(root)
            manifest["findings"].append({"id": "UNK-1", "statement": "Missing remote auth contract",
                                         "confidence": "unresolved", "sources": []})
            out = root / ".agent-context/manifest.json"
            out.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("no linked" in x for x in gate.collect_problems(root)))
            manifest["next_actions"] = [{
                "id": "ACT-1", "category": "investigation", "finding_ids": ["UNK-1"],
                "description": "Obtain contract", "searched_sources": ["pom.xml", "src/Controller.java"],
                "hypothesis": "External auth is delegated to the API gateway",
                "why_unresolved": "The external identity provider contract is not present."
            }]
            out.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual([], gate.collect_problems(root))

    def test_unproven_inference_and_escape_fail(self) -> None:
        # Files outside the project and inference without reasoning are rejected.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = make_fixture(root)
            manifest["findings"][1].pop("reasoning")
            manifest["findings"][0]["sources"][0]["path"] = "../secrets.txt"
            (root / ".agent-context/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            errors = gate.collect_problems(root)
            self.assertTrue(any("reasoning" in x for x in errors))
            self.assertTrue(any("unsafe" in x for x in errors))

    def test_unreplaced_template_fails(self) -> None:
        # A generated guide cannot retain authoring placeholders.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            p = root / "AGENTS.md"
            p.write_text(p.read_text(encoding="utf-8") + "\n{{TODO}}\n", encoding="utf-8")
            self.assertTrue(any("placeholders" in x for x in gate.collect_problems(root)))


if __name__ == "__main__":
    unittest.main()
