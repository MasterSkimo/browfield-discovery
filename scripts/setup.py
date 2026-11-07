#!/usr/bin/env python3
"""Opt-in, cross-platform bootstrap for Cursor and OpenCode discovery agents."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {
    "basic-memory": ("basic-memory", "basic-memory"),
    "mempalace": ("mempalace", "mempalace"),
    "graphify": ("graphify", "graphifyy"),
}
CLIENTS = ("cursor", "opencode")
SKILLS = (
    "brownfield-repository",
    "brownfield-boundaries",
    "brownfield-e2e-readiness",
    "brownfield-handoff",
)


def executable(name: str) -> str | None:
    """Return a PATH-visible binary without importing or running the package."""
    return shutil.which(name)


def ask(prompt: str, default: bool = False) -> bool:
    """Ask explicit consent; empty answers keep the default (normally no)."""
    if not sys.stdin.isatty():
        raise RuntimeError("Interactive setup needs a terminal; use --yes and explicit selections.")
    suffix = "[Y/n]" if default else "[y/N]"
    value = input(f"{prompt} {suffix} ").strip().lower()
    return default if not value else value in ("y", "yes", "o", "oui")


def choose_many(label: str, options: Iterable[str]) -> set[str]:
    """Offer each option independently; an empty selection is valid."""
    print(f"\n{label}")
    return {item for item in options if ask(f"  Select {item}?")}


def parse_csv(value: str | None, allowed: Iterable[str]) -> set[str] | None:
    """Validate comma-separated names, preserving an explicitly empty set."""
    if value is None:
        return None
    result = {part.strip().lower() for part in value.split(",") if part.strip()}
    invalid = result.difference(allowed)
    if invalid:
        raise ValueError(f"Unknown selection(s): {', '.join(sorted(invalid))}")
    return result


def run(command: list[str], dry_run: bool) -> bool:
    """Run a trusted fixed-argument install command, never through a shell."""
    print(f"  $ {subprocess.list2cmdline(command)}")
    if dry_run:
        return True
    try:
        subprocess.run(command, check=True)
        return True
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"  Failed: {exc}", file=sys.stderr)
        return False


def install_tool(name: str, dry_run: bool) -> bool:
    """Install only missing CLI tools with an existing isolated package manager."""
    binary, package = TOOLS[name]
    found = executable(binary)
    if found:
        print(f"  {name}: already installed ({found}); no upgrade")
        return True
    manager = executable("uv") or executable("pipx")
    if not manager:
        print(f"  {name}: missing; install uv (https://docs.astral.sh/uv/) or pipx first.")
        return False
    args = [manager, "tool", "install", package] if Path(manager).stem.lower() == "uv" else [manager, "install", package]
    # Graphify's PyPI name is 'graphifyy', not similarly named third-party packages.
    if name == "basic-memory" and Path(manager).stem.lower() == "uv":
        args.append("--prerelease=allow")
    return run(args, dry_run)


def copy_unmodified(source: Path, destination: Path, dry_run: bool) -> str:
    """Copy only new files, preserving modified or existing destination files."""
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination.exists() or destination.is_symlink():
        if destination.is_file() and destination.read_bytes() == source.read_bytes():
            return "already current"
        return "conflict (left unchanged)"
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return "would create" if dry_run else "created"


def deployment_paths(scope: str, target: Path | None) -> tuple[Path, Path, Path]:
    """Resolve client agent locations and one cross-client skills root."""
    if scope == "project":
        if target is None:
            raise ValueError("--target PATH is required for --scope project")
        root = target.expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"Target directory does not exist: {root}")
        return root / ".cursor" / "agents", root / ".opencode" / "agents", root / ".agents"
    home = Path.home()
    return home / ".cursor" / "agents", home / ".config" / "opencode" / "agents", home / ".agents"


def deploy_clients(clients: set[str], scope: str, target: Path | None, dry_run: bool) -> None:
    """Deploy one client-specific agent plus shared, discoverable skills and references."""
    cursor_dir, opencode_dir, shared = deployment_paths(scope, target)
    if not clients:
        return
    sources: list[tuple[Path, Path]] = []
    if "cursor" in clients:
        sources.append((ROOT / ".cursor/agents/brownfield-discovery.md", cursor_dir / "brownfield-discovery.md"))
    if "opencode" in clients:
        sources.append((ROOT / ".opencode/agents/brownfield-discovery.md", opencode_dir / "brownfield-discovery.md"))
    for skill in SKILLS:
        sources.append((ROOT / ".opencode" / "skills" / skill / "SKILL.md",
                        shared / "skills" / skill / "SKILL.md"))
    # Discovery templates and schemas accompany the globally installed agent.
    for relative in ("templates", "schemas"):
        for source in (ROOT / relative).rglob("*"):
            if source.is_file():
                sources.append((source, shared / "brownfield-discovery" / relative / source.relative_to(ROOT / relative)))
    for source, destination in sources:
        outcome = copy_unmodified(source, destination, dry_run)
        print(f"  {outcome}: {destination}")


def mcp_command(name: str) -> list[str] | None:
    """Resolve locally available MCP entrypoints; no automatic downloads at runtime."""
    if name == "basic-memory" and executable("basic-memory"):
        return [executable("basic-memory"), "mcp"]
    if name == "mempalace" and executable("mempalace-mcp"):
        return [executable("mempalace-mcp")]
    # Graphify requires a project graph and its own registration/transport choices.
    return None


def config_location(client: str, scope: str, target: Path | None) -> Path:
    """Return the documented local MCP configuration location."""
    if scope == "project":
        assert target is not None
        root = target.expanduser().resolve()
        return root / ".cursor/mcp.json" if client == "cursor" else root / "opencode.json"
    return Path.home() / (".cursor/mcp.json" if client == "cursor" else ".config/opencode/opencode.json")


def connect_mcp(client: str, names: set[str], scope: str, target: Path | None, dry_run: bool) -> None:
    """Merge optional MCP entries without replacing existing server definitions."""
    path = config_location(client, scope, target)
    # JSONC files cannot safely be rewritten by the stdlib JSON parser.
    if client == "opencode" and path.with_suffix(".jsonc").exists() and not path.exists():
        print(f"  {client}: found {path.with_suffix('.jsonc')}; merge MCP entries manually.")
        return
    try:
        existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except (OSError, ValueError) as exc:
        print(f"  {client}: cannot safely merge {path}: {exc}")
        return
    if not isinstance(existing, dict):
        print(f"  {client}: unexpected config root at {path}; no changes")
        return
    if client == "cursor":
        servers = existing.get("mcpServers", {})
    else:
        # OpenCode v2 uses mcp.servers, unlike the legacy flat mcp format.
        mcp = existing.get("mcp", {})
        servers = mcp.get("servers", {}) if isinstance(mcp, dict) else None
    if not isinstance(servers, dict):
        print(f"  {client}: existing server configuration has an unexpected shape; no changes")
        return

    # Respect ownership and all existing server names; never upgrade in place.
    added: dict[str, object] = {}
    for name in sorted(names):
        cmd = mcp_command(name)
        if cmd is None:
            print(f"  {name}: no verified MCP executable found; keep CLI-only or follow vendor setup.")
            continue
        if name in servers:
            print(f"  {client} MCP {name}: already configured; unchanged")
            continue
        added[name] = (
            {"command": cmd[0], "args": cmd[1:]}
            if client == "cursor" else {"type": "local", "command": cmd}
        )
    if not added:
        return
    print(f"  {client}: {'would add' if dry_run else 'adding'} MCP {', '.join(added)} to {path}")
    if dry_run:
        return
    # Existing files are preserved except for additive server keys.
    servers.update(added)
    if client == "cursor":
        existing["mcpServers"] = servers
    else:
        existing.setdefault("mcp", {})["servers"] = servers
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".brownfield.tmp")
    try:
        temp.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main(argv: list[str] | None = None) -> int:
    """Apply user-selected package, client and optional MCP operations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Display tool status without changing files")
    parser.add_argument("--tools", help="Comma-separated optional packages: basic-memory,mempalace,graphify")
    parser.add_argument("--clients", help="Comma-separated clients: cursor,opencode")
    parser.add_argument("--scope", choices=("global", "project"), default="global")
    parser.add_argument("--target", type=Path, help="Target repository root (required for project scope)")
    parser.add_argument("--connect-mcp", action="store_true", help="Opt in to MCP registration for selected tools")
    parser.add_argument("--yes", action="store_true", help="Confirm explicitly selected operations")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changing files or installing")
    args = parser.parse_args(argv)
    print("Detected tools:")
    for name, (binary, _) in TOOLS.items():
        print(f"  {name}: {executable(binary) or 'not detected'}")
    if args.check:
        return 0
    try:
        tools = parse_csv(args.tools, TOOLS) 
        clients = parse_csv(args.clients, CLIENTS)
        if tools is None:
            tools = choose_many("Optional CLI tools (nothing is installed by default):", TOOLS)
        if clients is None:
            clients = choose_many("Install discovery agent for:", CLIENTS)
        if not args.yes and not args.dry_run:
            if not ask(f"Proceed with tools={sorted(tools)}, clients={sorted(clients)}, scope={args.scope}?"):
                print("Cancelled; no changes.")
                return 0
        if args.scope == "project":
            deployment_paths(args.scope, args.target)  # Validate before package installation.
        if args.connect_mcp and not clients:
            raise ValueError("--connect-mcp requires --clients")
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    successful = set()
    for name in sorted(tools):
        if install_tool(name, args.dry_run):
            successful.add(name)
    deploy_clients(clients, args.scope, args.target, args.dry_run)
    if args.connect_mcp:
        for client in sorted(clients):
            connect_mcp(client, successful, args.scope, args.target, args.dry_run)
    elif successful:
        print("\nMCP connections were not changed; use --connect-mcp to opt in.")
    if "mempalace" in successful:
        print("MemPalace: existing memories were not imported, mined or modified.")
    if "graphify" in successful:
        print("Graphify: installed CLI only; no repository scan, hook or vendor skill registration.")
    if len(successful) < len(tools):
        print("Some selected tools could not be installed or detected; see above.")
        return 1
    print("Setup finished. Restart your client to pick up new agents, skills or MCP entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
