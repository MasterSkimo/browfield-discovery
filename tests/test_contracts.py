"""Contract and packaging checks for the information-only discovery proposal."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    """Read a JSON schema or example from the repository."""
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class ContractTests(unittest.TestCase):
    """Prevent the proposed agent and its handoff contract from drifting."""

    def test_json_schemas_are_valid(self) -> None:
        # Check schema declarations before trying to validate any examples.
        for schema_name in ("discovery-manifest", "discovery-progress", "task-evidence"):
            schema = load_json(f"schemas/{schema_name}.schema.json")
            Draft202012Validator.check_schema(schema)

    def test_examples_follow_schemas(self) -> None:
        # Examples are deliberately illustrative; they must still be valid.
        for schema_name in ("discovery-manifest", "task-evidence"):
            schema = load_json(f"schemas/{schema_name}.schema.json")
            example = load_json(f"examples/{schema_name}.example.json")
            Draft202012Validator(schema, format_checker=FormatChecker()).validate(example)

    def test_manifest_references_expected_output_templates(self) -> None:
        # Ensure every documented project artifact has a template.
        manifest = load_json("examples/discovery-manifest.example.json")
        for artifact_path in manifest["outputs"].values():
            self.assertTrue((ROOT / "templates" / artifact_path).is_file(), artifact_path)

    def test_agent_and_skills_are_discoverable(self) -> None:
        # OpenCode discovers custom agents and directory-based SKILL.md files.
        agent_path = ROOT / ".opencode/agents/brownfield-discovery.md"
        self.assertTrue(agent_path.is_file())
        agent = agent_path.read_text(encoding="utf-8")
        self.assertTrue(agent.startswith("---\n"))
        self.assertIn("mode: all", agent)

        # The discovery agent must be explicit about the Compose-first downstream handoff.
        self.assertIn("brownfield-runtime-topology", agent)
        self.assertIn("discovery-progress.json", agent)
        # Both provider-specific commands must invoke the complete discovery.
        opencode_command = ROOT / ".opencode/commands/brownfield-discover.md"
        cursor_command = ROOT / ".cursor/commands/brownfield-discover.md"
        self.assertIn("agent: brownfield-discovery", opencode_command.read_text(encoding="utf-8"))
        self.assertIn("subagent: false", opencode_command.read_text(encoding="utf-8"))
        self.assertIn("brownfield-inference", cursor_command.read_text(encoding="utf-8"))
        expected_ids = (
            "brownfield-inference",
            "brownfield-repository",
            "brownfield-runtime-topology",
            "brownfield-boundaries",
            "brownfield-e2e-readiness",
            "brownfield-handoff",
        )
        for name in expected_ids:
            path = ROOT / ".opencode" / "skills" / name / "SKILL.md"
            self.assertTrue(path.is_file(), str(path))
            content = path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"))
            self.assertRegex(content, rf"(?m)^name: {re.escape(name)}$")
            self.assertRegex(content, r"(?m)^description: .+")
            self.assertIn(name, agent)

    def test_evidence_examples_do_not_fake_execution(self) -> None:
        # The seeded example must never pretend Playwright or Newman ran.
        example = load_json("examples/task-evidence.example.json")
        self.assertEqual("incomplete", example["conclusion"]["status"])
        self.assertTrue(all(c["result"] == "not_run" for c in example["checks"]))
        self.assertTrue(all(a["status"] == "not_run" for a in example["acceptance"]))

    def test_accepted_evidence_must_be_traceable(self) -> None:
        # Schema validation ensures that a verified discovery fact has a source.
        schema = load_json("schemas/discovery-manifest.schema.json")
        example = load_json("examples/discovery-manifest.example.json")
        example["findings"][0]["sources"] = []
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(example)


if __name__ == "__main__":
    # Allows running the checks without a test runner dependency.
    unittest.main()
