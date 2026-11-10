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
    "environment_blueprint": ".agent-context/environment-blueprint.md",
    "discovery_progress": ".agent-context/discovery-progress.json",
    "clarifications": ".agent-context/clarifications.md",
    "compose_file": ".e2e/compose.yaml",
    "env_example": ".e2e/.env.e2e.example",
    "local_ignore": ".e2e/.gitignore",
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
        "First autonomous mission: E2E characterization": "Build/run the real application via Docker Compose, alongside database and broker services, stub outside-application systems and use Newman for real API assertions.",
        "Evidence and delivery": "Every acceptance criterion links implementation, automated assertion, command, environment, run artifact and pass/fail status.",
        "Detailed reference material": "See .agent-context/e2e-inventory.md for candidate journeys, architecture.md for topology and verification-contract.md for proof requirements.",
    }
    text = "# AGENTS.md — Sample API\n\n" + "\n\n".join(f"## {title}\n{body}" for title, body in sections.items())
    (root / "AGENTS.md").write_text(text, encoding="utf-8")
    for name, path in OUTPUTS.items():
        if name in ("agent_instructions", "discovery_progress", "compose_file", "env_example", "local_ignore", "clarifications"):
            continue
        f = root / path
        f.parent.mkdir(parents=True, exist_ok=True)
        if name == "environment_blueprint":
            f.write_text(
                "# Compose blueprint\n"
                "Build real Maven application from pom.xml. Use a containerized database and broker, "
                "external stub boundaries, an application e2e profile and dedicated environment variables; "
                "include seed/reset, health and test runner requirements.\n",
                encoding="utf-8",
            )
        else:
            f.write_text("# Context\nInspected code reference from pom.xml.\n", encoding="utf-8")
    # Actual Docker foundation is part of the discovery fixture.
    docker = root / ".e2e/docker"
    docker.mkdir(parents=True)
    (docker / "app.Dockerfile").write_text(
        "FROM eclipse-temurin:21-jre\nWORKDIR /app\nCOPY . .\n", encoding="utf-8"
    )
    (root / ".e2e/compose.yaml").write_text(
        "name: sample-e2e\nservices:\n"
        "  app:\n    build:\n      context: ..\n"
        "      dockerfile: .e2e/docker/app.Dockerfile\n"
        "    environment:\n      APP_PROFILE: e2e\n"
        "  db:\n    image: postgres:16\n", encoding="utf-8"
    )
    (root / ".e2e/.env.e2e.example").write_text("APP_PROFILE=e2e\n", encoding="utf-8")
    (root / ".e2e/.gitignore").write_text(".env.e2e.local\n*.secret\n", encoding="utf-8")
    # The developer interview is a required output even when no questions exist.
    (root / OUTPUTS["clarifications"]).write_text(
        "# Developer clarifications\n"
        "## Conversation status\nNo developer clarification required.\n"
        "## Questions and answers\nNo questions after investigation.\n",
        encoding="utf-8",
    )
    # A ready handoff includes the eighth, interactive stage with evidence.
    progress = {
        "schema_version": "0.1.0",
        "revision": "0123456789abcdef",
        "phases": [
            {"id": f"D{i}", "status": "done",
             "evidence": [OUTPUTS["clarifications"]] if i == 7 else ["pom.xml"],
             "blockers": [], "notes": "Example fixture evidence only"}
            for i in range(8)
        ],
    }
    (root / OUTPUTS["discovery_progress"]).write_text(json.dumps(progress), encoding="utf-8")
    manifest = {
        "schema_version": "0.1.0",
        "repository": {"name": "sample", "revision": "0123456789abcdef", "analyzed_at": "2026-11-10T10:00:00Z"},
        "status": "ready_for_e2e_setup", "outputs": OUTPUTS,
        "docker_validation": {
            "status": "not_run",
            "command": "docker compose -f .e2e/compose.yaml --env-file .e2e/.env.e2e.example config --quiet",
            "reason": "Synthetic fixture; Docker Compose not executed."
        },
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
            # D7 is closed only after the unknown is registered as deferred or addressed.
            ledger = root / OUTPUTS["clarifications"]
            ledger.write_text(
                ledger.read_text(encoding="utf-8") + "\nUNK-1: deferred, contract to verify.\n",
                encoding="utf-8",
            )
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


    def test_incomplete_workflow_blocks_ready(self) -> None:
        # Discovery cannot claim readiness until all eight gates are finished.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            path = root / OUTPUTS["discovery_progress"]
            progress = json.loads(path.read_text(encoding="utf-8"))
            progress["phases"][2]["status"] = "pending"
            progress["phases"][2]["evidence"] = []
            path.write_text(json.dumps(progress), encoding="utf-8")
            errors = gate.collect_problems(root)
            self.assertTrue(any("all D0-D7 gates" in x for x in errors))
            self.assertTrue(any("completed after an incomplete" in x for x in errors))

    def test_phase_evidence_is_required(self) -> None:
        # An unchecked or unsupported phase cannot be marked done.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            path = root / OUTPUTS["discovery_progress"]
            progress = json.loads(path.read_text(encoding="utf-8"))
            progress["phases"][1]["evidence"] = []
            path.write_text(json.dumps(progress), encoding="utf-8")
            self.assertTrue(any("done without source evidence" in x for x in gate.collect_problems(root)))

    def test_environment_blueprint_must_describe_compose(self) -> None:
        # A generic dependency note is not a Compose-first implementation handoff.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            path = root / OUTPUTS["environment_blueprint"]
            path.write_text("# Later\nTBD\n", encoding="utf-8")
            self.assertTrue(any("environment blueprint" in x for x in gate.collect_problems(root)))


    def test_missing_compose_and_env_are_rejected(self) -> None:
        # Discovery cannot hand off only a blueprint without Docker resources.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_fixture(root)
            (root / ".e2e/compose.yaml").unlink()
            (root / ".e2e/.env.e2e.example").unlink()
            errors = gate.collect_problems(root)
            self.assertTrue(any("output missing" in e and "compose_file" in e for e in errors))
            self.assertTrue(any("output missing" in e and "env_example" in e for e in errors))

    def test_empty_compose_template_rejected(self) -> None:
        # An empty example must never pass as a real application Docker foundation.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_fixture(root)
            (root / ".e2e/compose.yaml").write_text(
                "name: demo\nservices: {}\n", encoding="utf-8"
            )
            self.assertTrue(any("Docker foundation" in e for e in gate.collect_problems(root)))

    def test_compose_validation_failure_blocks_handoff(self) -> None:
        # Failed config parsing must prevent a ready_for_e2e_setup claim.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_fixture(root)
            manifest["docker_validation"]["status"] = "fail"
            manifest["docker_validation"]["reason"] = "Compose interpolation error"
            (root / ".agent-context/manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            self.assertTrue(any("blocks E2E handoff" in e for e in gate.collect_problems(root)))

    def test_bad_compose_dockerfile_path_rejected(self) -> None:
        # Docker build declarations must point to a real Dockerfile in the checkout.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_fixture(root)
            compose = root / ".e2e/compose.yaml"
            compose.write_text(
                "services:\n  app:\n    build:\n      context: ..\n"
                "      dockerfile: .e2e/docker/nonexistent.Dockerfile\n", encoding="utf-8"
            )
            # The CI test environment includes PyYAML for service and Dockerfile checks.
            if gate.yaml is None:
                self.skipTest("PyYAML is not installed")
            self.assertTrue(any("Dockerfile is missing" in e for e in gate.collect_problems(root)))

    def test_question_is_saved_while_waiting_for_user(self) -> None:
        # Awaiting a human response is a valid persistent discovery state.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = make_fixture(root)
            manifest["status"] = "awaiting_user_clarification"
            manifest["findings"].append({
                "id": "UNK-7", "statement": "External identity integration",
                "confidence": "unresolved", "sources": []
            })
            manifest["next_actions"].append({
                "id": "ACT-7", "category": "developer-question", "description": "Confirm test identity",
                "finding_ids": ["UNK-7"], "searched_sources": ["pom.xml"],
                "hypothesis": "Identity is controlled by an external test provider",
                "why_unresolved": "The external IdP contract is not included in this checkout."
            })
            (root / ".agent-context/manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            progress_file = root / OUTPUTS["discovery_progress"]
            progress = json.loads(progress_file.read_text(encoding="utf-8"))
            progress["phases"][-1]["status"] = "awaiting_user"
            progress_file.write_text(json.dumps(progress), encoding="utf-8")
            (root / OUTPUTS["clarifications"]).write_text(
                "# Developer clarifications\n## Conversation status\nStatus: awaiting_user\n"
                "## Questions and answers\nUNK-7: Does E2E require an external IdP?\n",
                encoding="utf-8",
            )
            self.assertEqual([], gate.collect_problems(root))
            manifest["status"] = "ready_for_e2e_setup"
            (root / ".agent-context/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("requires all D0-D7" in e for e in gate.collect_problems(root)))

    def test_unresolved_unknown_needs_interview_record(self) -> None:
        # A developer-answerable unknown cannot vanish from a completed handoff.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = make_fixture(root)
            manifest["findings"].append({
                "id": "UNK-9", "statement": "Issuer contract unclear",
                "confidence": "unresolved", "sources": []
            })
            manifest["next_actions"].append({
                "id": "ACT-9", "category": "developer-question", "description": "Confirm issuer contract",
                "finding_ids": ["UNK-9"], "searched_sources": ["pom.xml"],
                "hypothesis": "Local test issuer may be supported by the service",
                "why_unresolved": "Issuer details are outside the checked-out repository."
            })
            (root / ".agent-context/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("UNK-9 is missing" in e for e in gate.collect_problems(root)))
            path = root / OUTPUTS["clarifications"]
            path.write_text(path.read_text(encoding="utf-8") + "\nUNK-9: deferred by developer; verify issuer externally.\n", encoding="utf-8")
            self.assertEqual([], gate.collect_problems(root))

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
