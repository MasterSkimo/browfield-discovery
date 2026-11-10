#!/usr/bin/env python3
"""Validate generated brownfield context without running application code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


SECTIONS = (
    "Project overview", "Repository map", "Setup commands", "Build and run",
    "Tests and quality checks", "Architecture and code conventions",
    "Security and data handling", "First autonomous mission: E2E characterization",
    "Evidence and delivery", "Detailed reference material",
)
OUTPUTS = (
    "agent_instructions", "architecture", "execution", "dependencies",
    "e2e_inventory", "unknowns", "verification_contract",
)
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}|<PROJECT NAME>|<ADD ONLY|<SOURCE-BACKED", re.IGNORECASE)
HEADING = re.compile(r"(?m)^#{2,3}\s+(.+?)\s*$")


def under_project(project: Path, relative: str) -> Path | None:
    """Reject absolute, parent traversal, and symlink-escaping file references."""
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts:
        return None
    target = (project / p).resolve()
    return target if target.is_relative_to(project.resolve()) else None


def sections_of(markdown: str) -> dict[str, str]:
    """Get content beneath second- or third-level Markdown headings."""
    matches = list(HEADING.finditer(markdown))
    result: dict[str, str] = {}
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        result[match.group(1).strip().lower()] = markdown[match.end():end].strip()
    return result


def collect_problems(project: Path) -> list[str]:
    """Perform structural, link and investigation-quality checks."""
    project = project.resolve()
    agent_file = project / "AGENTS.md"
    manifest_file = project / ".agent-context/manifest.json"
    if not agent_file.is_file():
        return ["missing project-root AGENTS.md"]
    if not manifest_file.is_file():
        return ["missing .agent-context/manifest.json"]
    try:
        agent = agent_file.read_text(encoding="utf-8")
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError) as exc:
        return [f"cannot read AGENTS.md or manifest: {exc}"]
    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]
    issues: list[str] = []

    # A generated AGENTS.md must contain actionable guidance, not just links.
    headings = sections_of(agent)
    for section in SECTIONS:
        text = headings.get(section.lower(), "")
        if not text:
            issues.append(f"AGENTS.md missing or empty section: {section}")
        elif len(re.sub(r"\[[^]]+\]\([^)]*\)", "", text).strip()) < 35:
            issues.append(f"AGENTS.md section too thin: {section}")
    if len(agent.strip()) < 900:
        issues.append("AGENTS.md too short for substantive instructions")
    if PLACEHOLDER.search(agent):
        issues.append("AGENTS.md contains template placeholders")
    if "declared" not in agent.lower() and "observed" not in agent.lower():
        issues.append("AGENTS.md omits declared versus observed command status")
    # Backticked shell commands or fenced blocks must appear in operational sections.
    tick = chr(96)
    commands = [headings.get(name.lower(), "") for name in ("Setup commands", "Build and run", "Tests and quality checks")]
    command_count = sum(section.count(tick) // 2 + section.count("~~~") // 2 for section in commands)
    if command_count < 2:
        issues.append("AGENTS.md needs at least two concrete build/run/test command examples")
    if not re.search(r"(pom\.xml|build\.gradle|package\.json|Cargo\.toml|go\.mod|Makefile|pyproject\.toml|\.github/workflows/|src/|backend/|frontend/)", agent):
        issues.append("AGENTS.md needs project-specific source/build/module references")

    outputs = manifest.get("outputs")
    if not isinstance(outputs, dict):
        issues.append("manifest.outputs must be an object")
        outputs = {}
    for name in OUTPUTS:
        path = outputs.get(name)
        if not isinstance(path, str) or not path:
            issues.append(f"missing manifest.outputs.{name}")
            continue
        target = under_project(project, path)
        if target is None or not target.is_file():
            issues.append(f"output missing or unsafe: {name} -> {path}")
        else:
            try:
                if PLACEHOLDER.search(target.read_text(encoding="utf-8")):
                    issues.append(f"output has placeholders: {path}")
            except UnicodeError:
                issues.append(f"output not readable as UTF-8: {path}")
    if outputs.get("agent_instructions") != "AGENTS.md":
        issues.append("agent_instructions must point to root AGENTS.md")
    if manifest.get("status") not in ("ready_for_e2e_setup", "needs_investigation"):
        issues.append("unsupported manifest status")

    # Static inference is useful only when the source and reasoning are explicit.
    findings = manifest.get("findings")
    if not isinstance(findings, list):
        findings = []
        issues.append("manifest.findings is not an array")
    unresolved: set[str] = set()
    for finding in findings:
        if not isinstance(finding, dict):
            issues.append("malformed finding")
            continue
        fid = str(finding.get("id", "?"))
        level = finding.get("confidence")
        sources = finding.get("sources", [])
        if level == "unresolved":
            unresolved.add(fid)
        if level in ("verified", "inferred") and not sources:
            issues.append(f"{fid}: no sources for {level} statement")
        if level == "inferred" and len(str(finding.get("reasoning", ""))) < 25:
            issues.append(f"{fid}: inference without reasoning chain")
        for source in sources if isinstance(sources, list) else []:
            if not isinstance(source, dict):
                issues.append(f"{fid}: malformed evidence")
                continue
            path = source.get("path")
            target = under_project(project, path) if isinstance(path, str) else None
            if target is None or not target.is_file():
                issues.append(f"{fid}: unsafe or missing evidence path {path}")

    # Escalated unknowns require a search trail and best available hypothesis.
    actions = manifest.get("next_actions")
    if not isinstance(actions, list):
        actions = []
        issues.append("manifest.next_actions is not an array")
    referenced: set[str] = set()
    for action in actions:
        if not isinstance(action, dict):
            issues.append("malformed next action")
            continue
        finding_ids = action.get("finding_ids", [])
        if isinstance(finding_ids, list):
            referenced.update(str(fid) for fid in finding_ids)
        if action.get("category") in ("investigation", "developer-question"):
            if not action.get("searched_sources") or len(str(action.get("why_unresolved", ""))) < 20:
                issues.append(f"{action.get('id')}: no search trail or unresolved rationale")
            if len(str(action.get("hypothesis", ""))) < 12:
                issues.append(f"{action.get('id')}: no bounded hypothesis")
    for fid in sorted(unresolved - referenced):
        issues.append(f"unresolved {fid} has no linked investigation action")
    return issues


def main(argv: list[str] | None = None) -> int:
    """Print the quality report and return nonzero on deficient output."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    if not args.project.is_dir():
        parser.error(f"not a directory: {args.project}")
    issues = collect_problems(args.project)
    for issue in issues:
        print(f"FAIL: {issue}")
    print(f"{'FAIL' if issues else 'PASS'}: discovery quality ({len(issues)} issues)")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
