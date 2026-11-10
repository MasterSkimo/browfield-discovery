#!/usr/bin/env python3
"""Validate generated brownfield context without running application code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

# PyYAML is an optional extra for inspecting Compose service structure.
try:
    import yaml
except ImportError:
    yaml = None


SECTIONS = (
    "Project overview", "Repository map", "Setup commands", "Build and run",
    "Tests and quality checks", "Architecture and code conventions",
    "Security and data handling", "First autonomous mission: E2E characterization",
    "Evidence and delivery", "Detailed reference material",
)
OUTPUTS = (
    "agent_instructions", "architecture", "execution", "dependencies",
    "e2e_inventory", "unknowns", "verification_contract",
    "environment_blueprint", "discovery_progress",
    "compose_file", "env_example", "local_ignore",
)
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}|<PROJECT NAME>|<ADD ONLY|<SOURCE-BACKED|\bPROJECT_NAME\b|\bAPP_MODULES_WITH_PATHS\b|\bEVIDENCE_AND_ACTIONS\b|\bREVISION_REPLACE_WITH_REAL_SHA\b", re.IGNORECASE)
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
    e2e_section = headings.get("first autonomous mission: e2e characterization", "").lower()
    if "compose" not in e2e_section or "build" not in e2e_section:
        issues.append("AGENTS.md must instruct agents to build/run the full real application via Compose")
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
    # A build-first environment blueprint must be more than a file name.
    blueprint_name = outputs.get("environment_blueprint")
    blueprint_file = under_project(project, blueprint_name) if isinstance(blueprint_name, str) else None
    if blueprint_file and blueprint_file.is_file():
        blueprint_text = blueprint_file.read_text(encoding="utf-8").lower()
        if not all(word in blueprint_text for word in ("compose", "build", "profile", "stub", "environment", "database", "broker")):
            issues.append("environment blueprint lacks full-stack Compose/build/config/boundary details")
        if len(blueprint_text.strip()) < 250:
            issues.append("environment blueprint is too short for actionable setup planning")

    # The actual E2E Docker foundation is a required output, not an optional plan.
    compose_name = outputs.get("compose_file")
    compose_path = under_project(project, compose_name) if isinstance(compose_name, str) else None
    if compose_name != ".e2e/compose.yaml":
        issues.append("Compose foundation must be .e2e/compose.yaml")
    if compose_path and compose_path.is_file():
        body = compose_path.read_text(encoding="utf-8")
        if yaml is not None:
            try:
                compose_data = yaml.safe_load(body)
            except yaml.YAMLError as exc:
                compose_data = None
                issues.append(f"Compose YAML is invalid: {exc}")
            services = compose_data.get("services") if isinstance(compose_data, dict) else None
            if not isinstance(services, dict) or not services:
                issues.append("Docker foundation must contain actual Compose services")
            elif not any(isinstance(s, dict) and s.get("build") for s in services.values()):
                issues.append("Docker foundation has no real source-built application service")
            else:
                # Verify source-build contexts and referenced Dockerfiles are part of the checkout.
                for service_name, service in services.items():
                    if not isinstance(service, dict) or not service.get("build"):
                        continue
                    build = service["build"]
                    context_str = build if isinstance(build, str) else build.get("context", ".") if isinstance(build, dict) else None
                    if not isinstance(context_str, str) or "$" in context_str:
                        issues.append(f"{service_name}: unresolved Docker build context")
                        continue
                    context_path = (compose_path.parent / context_str).resolve()
                    if not context_path.is_dir() or not context_path.is_relative_to(project):
                        issues.append(f"{service_name}: missing or unsafe Docker build context")
                        continue
                    df = "Dockerfile" if not isinstance(build, dict) else build.get("dockerfile", "Dockerfile")
                    dockerfile_path = context_path / df if isinstance(df, str) else None
                    if dockerfile_path is None or not dockerfile_path.is_file() or not dockerfile_path.resolve().is_relative_to(project):
                        issues.append(f"{service_name}: Dockerfile is missing or outside checkout")
        else:
            # The stdlib fallback rejects the unpopulated template but cannot prove YAML syntax.
            if not re.search(r"(?m)^services:\s*$", body) or not re.search(r"(?m)^\s+build:\s*(?:$|[^#\s])", body):
                issues.append("Docker foundation has no real source-built Compose service")
    env_name = outputs.get("env_example")
    env_path = under_project(project, env_name) if isinstance(env_name, str) else None
    if env_name != ".e2e/.env.e2e.example":
        issues.append("E2E environment example must be .e2e/.env.e2e.example")
    if env_path and env_path.is_file():
        env_text = env_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\S+", env_text):
            issues.append("E2E env example needs nonsecret variable declarations")
    ignore_name = outputs.get("local_ignore")
    ignore_path = under_project(project, ignore_name) if isinstance(ignore_name, str) else None
    if ignore_name != ".e2e/.gitignore":
        issues.append("E2E local value ignore must be .e2e/.gitignore")
    if ignore_path and ignore_path.is_file():
        if ".env.e2e.local" not in ignore_path.read_text(encoding="utf-8"):
            issues.append("E2E local values must be ignored from Git")
    validation = manifest.get("docker_validation")
    if not isinstance(validation, dict):
        issues.append("manifest must record Docker Compose config validation")
    else:
        status = validation.get("status")
        if status not in ("pass", "fail", "not_run"):
            issues.append("invalid Docker Compose validation status")
        if status == "fail" and manifest.get("status") == "ready_for_e2e_setup":
            issues.append("failed Docker Compose config check blocks E2E handoff readiness")
        if status in ("not_run", "fail") and len(str(validation.get("reason", ""))) < 10:
            issues.append("Docker Compose check needs explanation when not passing")
        if "docker compose" not in str(validation.get("command", "")):
            issues.append("Docker Compose validation command must be recorded")

    # Gate progression and source evidence are explicit, not merely narrative.
    progress_name = outputs.get("discovery_progress")
    progress_file = under_project(project, progress_name) if isinstance(progress_name, str) else None
    if progress_file and progress_file.is_file():
        try:
            progress = json.loads(progress_file.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError, OSError):
            progress = None
            issues.append("invalid discovery progress JSON")
        if not isinstance(progress, dict):
            issues.append("discovery progress must be an object")
        else:
            revision = manifest.get("repository", {}).get("revision") if isinstance(manifest.get("repository"), dict) else None
            if progress.get("revision") != revision:
                issues.append("discovery progress revision does not match analyzed manifest revision")
            phases = progress.get("phases")
            required_ids = [f"D{i}" for i in range(7)]
            if not isinstance(phases, list) or [x.get("id") if isinstance(x, dict) else None for x in phases] != required_ids:
                issues.append("discovery progress phases must be ordered D0-D6")
            else:
                seen_incomplete = False
                for phase in phases:
                    pid = phase["id"]
                    status = phase.get("status")
                    evidence = phase.get("evidence")
                    blockers = phase.get("blockers")
                    if status not in ("pending", "in_progress", "done", "blocked"):
                        issues.append(f"{pid}: invalid phase status")
                    if status == "done":
                        if seen_incomplete:
                            issues.append(f"{pid}: completed after an incomplete previous phase")
                        if not isinstance(evidence, list) or not evidence:
                            issues.append(f"{pid}: done without source evidence")
                        else:
                            for relative in evidence:
                                path = under_project(project, relative) if isinstance(relative, str) else None
                                if path is None or not path.is_file():
                                    issues.append(f"{pid}: missing or unsafe phase evidence {relative}")
                    else:
                        seen_incomplete = True
                    if status == "blocked" and (not isinstance(blockers, list) or not blockers):
                        issues.append(f"{pid}: blocked without an explanation")
                if manifest.get("status") == "ready_for_e2e_setup" and any(
                    phase.get("status") != "done" for phase in phases
                ):
                    issues.append("ready_for_e2e_setup requires all D0-D6 gates complete")
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
