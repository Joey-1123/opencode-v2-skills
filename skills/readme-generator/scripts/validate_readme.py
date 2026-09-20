#!/usr/bin/env python3
"""
README Validator - Verify README.md consistency with codebase

Usage:
    python validate_readme.py --readme <readme_file> --path <project_path>
"""

import sys
import re
from pathlib import Path


def validate_readme(readme_path: Path, project_path: Path) -> list:
    """Validate README against actual project structure."""
    issues = []
    content = readme_path.read_text()

    # Check all referenced files exist
    file_refs = re.findall(r'`([^`]+\.(py|js|ts|toml|yaml|yml|json|md|toml))`', content)
    for ref, ext in file_refs:
        if not (project_path / ref).exists() and not (project_path / ref.lstrip('/')).exists():
            issues.append({
                "severity": "warning",
                "message": f"Referenced file not found: {ref}",
                "fix": f"Create the file or update the reference"
            })

    # Check that mentioned commands exist in scripts
    script_section = re.search(r'## (?:Usage|Commands|CLI)\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if script_section:
        commands = re.findall(r'`(\w+)`', script_section.group(1))
        # Check pyproject.toml scripts
        pyproject = project_path / "pyproject.toml"
        if pyproject.exists():
            pyproject_content = pyproject.read_text()
            for cmd in commands:
                if cmd not in pyproject_content and cmd not in ["pip", "uv", "git", "pytest", "ruff"]:
                    issues.append({
                        "severity": "warning",
                        "message": f"Command '{cmd}' not found in pyproject.toml scripts",
                        "fix": f"Verify command exists or update README"
                    })

    # Check install commands match manifest
    install_section = re.search(r'## Installation\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if install_section:
        install_text = install_section.group(1)
        if 'uv sync' in install_text and not (project_path / "pyproject.toml").exists():
            issues.append({
                "severity": "error",
                "message": "README mentions 'uv sync' but no pyproject.toml found",
                "fix": "Remove or update the install command"
            })

    # Check for placeholder text
    placeholders = ['TODO', 'XXX', 'placeholder', 'Lorem ipsum', '<!-- Add your']
    for placeholder in placeholders:
        if placeholder.lower() in content.lower():
            issues.append({
                "severity": "warning",
                "message": f"Placeholder text found: '{placeholder}'",
                "fix": "Replace with actual content"
            })

    return issues


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate README consistency with codebase")
    parser.add_argument("--readme", required=True, help="Path to README.md")
    parser.add_argument("--path", required=True, help="Project root path")
    args = parser.parse_args()

    readme_path = Path(args.readme)
    project_path = Path(args.path)

    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        sys.exit(1)
    if not project_path.exists():
        print(f"Error: {project_path} not found")
        sys.exit(1)

    issues = validate_readme(readme_path, project_path)

    if not issues:
        print("✅ README is consistent with the codebase")
        sys.exit(0)

    print(f"⚠️  {len(issues)} issue(s) found:")
    for issue in issues:
        icon = "❌" if issue["severity"] == "error" else "⚠️"
        print(f"{icon} [{issue['severity'].upper()}] {issue['message']}")
        print(f"   Fix: {issue['fix']}")

    sys.exit(1 if any(i["severity"] == "error" for i in issues) else 0)


if __name__ == "__main__":
    main()
