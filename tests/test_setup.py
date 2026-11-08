"""Tests for safe, opt-in Cursor/OpenCode bootstrap; no external installations."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("brownfield_setup", ROOT / "scripts" / "setup.py")
assert SPEC and SPEC.loader
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    """Check idempotence, client paths, safe JSON merges and package selection."""

    def test_check_has_no_side_effects(self) -> None:
        # Reading tool status must not install packages or write client files.
        with mock.patch.object(setup, "install_tool", side_effect=AssertionError("install")), \
             mock.patch.object(setup, "deploy_clients", side_effect=AssertionError("copy")):
            self.assertEqual(setup.main(["--check"]), 0)

    def test_project_clients_and_shared_skills(self) -> None:
        # Both clients should find one canonical shared skills directory.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            setup.deploy_clients({"cursor", "opencode"}, "project", root, dry_run=False)
            self.assertTrue((root / ".cursor/agents/brownfield-discovery.md").is_file())
            self.assertTrue((root / ".opencode/agents/brownfield-discovery.md").is_file())
            self.assertTrue((root / ".agents/skills/brownfield-handoff/SKILL.md").is_file())
            self.assertTrue((root / ".agents/brownfield-discovery/templates/AGENTS.md").is_file())
            self.assertTrue((root / ".agents/brownfield-discovery/schemas/task-evidence.schema.json").is_file())

    def test_idempotence_and_customization(self) -> None:
        # Identical destination files are skipped and custom content is retained.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            setup.deploy_clients({"cursor"}, "project", root, dry_run=False)
            agent = root / ".cursor/agents/brownfield-discovery.md"
            original = agent.read_bytes()
            setup.deploy_clients({"cursor"}, "project", root, dry_run=False)
            self.assertEqual(original, agent.read_bytes())
            agent.write_text("CUSTOM\n", encoding="utf-8")
            setup.deploy_clients({"cursor"}, "project", root, dry_run=False)
            self.assertEqual("CUSTOM\n", agent.read_text(encoding="utf-8"))

    def test_dry_run_and_required_target(self) -> None:
        # Dry runs create nothing and project scope never assumes cwd.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            setup.deploy_clients({"cursor", "opencode"}, "project", root, dry_run=True)
            self.assertFalse(list(root.iterdir()))
        with self.assertRaises(ValueError):
            setup.deployment_paths("project", None)

    def test_package_command_uses_official_name(self) -> None:
        # Graphify's official distribution is graphifyy, not graphify.
        with mock.patch.object(setup, "executable", side_effect=lambda name: "/fake/uv" if name == "uv" else None), \
             mock.patch.object(setup, "run", return_value=True) as runner:
            self.assertTrue(setup.install_tool("graphify", dry_run=False))
            runner.assert_called_once_with(["/fake/uv", "tool", "install", "graphifyy"], False)

    def test_client_mcp_merge_is_additive(self) -> None:
        # Preserve existing Cursor servers and use OpenCode v2's mcp.servers.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".cursor").mkdir()
            config = root / ".cursor/mcp.json"
            config.write_text(json.dumps({"mcpServers": {"existing": {"command": "custom"}}}), encoding="utf-8")
            with mock.patch.object(setup, "mcp_command", return_value=["/fake/basic-memory", "mcp"]):
                setup.connect_mcp("cursor", {"basic-memory"}, "project", root, dry_run=False)
                setup.connect_mcp("opencode", {"basic-memory"}, "project", root, dry_run=False)
            cursor = json.loads(config.read_text(encoding="utf-8"))
            opencode = json.loads((root / "opencode.json").read_text(encoding="utf-8"))
            self.assertEqual({"command": "custom"}, cursor["mcpServers"]["existing"])
            self.assertEqual("/fake/basic-memory", cursor["mcpServers"]["basic-memory"]["command"])
            self.assertEqual(
                ["/fake/basic-memory", "mcp"], opencode["mcp"]["servers"]["basic-memory"]["command"]
            )

    def test_jsonc_preservation(self) -> None:
        # Existing JSONC with comments is not parsed as JSON and is never replaced.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "opencode.jsonc"
            config.write_text('{"mcp": {/* manual */}}\n', encoding="utf-8")
            with mock.patch.object(setup, "mcp_command", return_value=["/fake/mempalace-mcp"]):
                setup.connect_mcp("opencode", {"mempalace"}, "project", root, dry_run=False)
            self.assertFalse((root / "opencode.json").exists())
            self.assertIn("/* manual */", config.read_text(encoding="utf-8"))


    def test_context7_remote_mcp_no_local_install(self) -> None:
        # Selecting Context7 registers its remote MCP directly without Node/npm.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(setup, "run", side_effect=AssertionError("No installs")):
                rc = setup.main([
                    "--tools", "context7", "--clients", "cursor,opencode",
                    "--scope", "project", "--target", str(root), "--yes"
                ])
            self.assertEqual(rc, 0)
            cursor = json.loads((root / ".cursor/mcp.json").read_text(encoding="utf-8"))
            opencode = json.loads((root / "opencode.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {"url": "https://mcp.context7.com/mcp"}, cursor["mcpServers"]["context7"]
            )
            self.assertEqual(
                {"type": "remote", "url": "https://mcp.context7.com/mcp"},
                opencode["mcp"]["servers"]["context7"]
            )
            self.assertTrue(setup.context7_configured("cursor", "project", root))
            self.assertTrue(setup.context7_configured("opencode", "project", root))
            # Re-running must keep existing entries and not install packages.
            self.assertEqual(0, setup.main([
                "--tools", "context7", "--clients", "cursor,opencode",
                "--scope", "project", "--target", str(root), "--yes"
            ]))

    def test_context7_preserves_existing_server_definition(self) -> None:
        # Pre-existing MCP entries, including custom headers, are not rewritten.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".cursor").mkdir()
            config = root / ".cursor/mcp.json"
            existing = {"mcpServers": {
                "context7": {"url": "https://custom.example/mcp", "headers": {"X-Test": "existing"}},
                "other": {"command": "existing"}
            }}
            config.write_text(json.dumps(existing), encoding="utf-8")
            setup.connect_mcp("cursor", {"context7"}, "project", root, dry_run=False)
            self.assertEqual(existing, json.loads(config.read_text(encoding="utf-8")))

    def test_context7_dry_run_and_missing_client(self) -> None:
        # No MCP config is written during preview and a client is mandatory.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(0, setup.main([
                "--tools", "context7", "--clients", "cursor",
                "--scope", "project", "--target", str(root), "--dry-run"
            ]))
            self.assertEqual([], list(root.iterdir()))
            with self.assertRaises(SystemExit):
                setup.main([
                    "--tools", "context7", "--clients", "",
                    "--scope", "project", "--target", str(root), "--yes"
                ])

    def test_explicit_noninteractive_selection(self) -> None:
        # A user can deploy agents without installing any optional package.
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(setup, "install_tool", side_effect=AssertionError("install")):
                rc = setup.main(["--tools", "", "--clients", "cursor,opencode", "--scope",
                                 "project", "--target", tmp, "--yes"])
            self.assertEqual(0, rc)
            self.assertTrue((Path(tmp) / ".agents/skills/brownfield-repository/SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
