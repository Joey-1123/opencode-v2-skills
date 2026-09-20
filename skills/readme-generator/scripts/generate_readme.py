#!/usr/bin/env python3
"""
README Generator - Generate complete README.md from project structure

Usage:
    python generate_readme.py [--path <project_path>] [--output <output_file>]
    python generate_readme.py --path /home/joey/projects/ringforge --output README.md
"""

import argparse
import sys
import os
import json
import re
from pathlib import Path


def find_manifest(path: Path) -> dict:
    """Find and parse project manifest files."""
    manifests = {}

    # Python
    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        manifests["type"] = "python"
        manifests["file"] = "pyproject.toml"
        content = pyproject.read_text()
        # Extract name, description, dependencies
        name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
        desc_match = re.search(r'description\s*=\s*"([^"]+)"', content)
        if name_match:
            manifests["name"] = name_match.group(1)
        if desc_match:
            manifests["description"] = desc_match.group(1)
        # Extract dependencies
        deps = re.findall(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if deps:
            dep_list = re.findall(r'"([^"]+)"', deps[0])
            manifests["dependencies"] = dep_list

    return manifests


def find_scripts(path: Path) -> list:
    """Find CLI scripts and commands."""
    scripts = []

    # Check pyproject.toml for scripts
    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text()
        script_matches = re.findall(r'\[project\.scripts\]\s*\n((?:.*?\n)*?)\n\s*\[', content)
        if not script_matches:
            script_matches = re.findall(r'"([^"]+)"\s*=\s*"([^"]+)"', content)
        for match in script_matches:
            if isinstance(match, tuple) and len(match) == 2:
                scripts.append({"name": match[0], "command": match[1]})
            elif isinstance(match, str):
                scripts.append({"name": match, "command": match})

    # Check for setup.py
    setup = path / "setup.py"
    if setup.exists():
        content = setup.read_text()
        entry_points = re.findall(r'entry_points.*?=\s*\{(.*?)\}', content, re.DOTALL)
        if entry_points:
            scripts.extend(re.findall(r"'([^']+)':\s*'([^']+)'", entry_points[0]))

    return scripts


def find_config_files(path: Path) -> list:
    """Find configuration files."""
    config_files = []
    for f in path.rglob("*"):
        if f.is_file() and f.name.endswith(('.env', '.env.example', '.toml', '.yaml', '.yml', '.ini', '.cfg')):
            if '.git' not in str(f):
                config_files.append(str(f.relative_to(path)))
    return config_files


def find_test_dirs(path: Path) -> list:
    """Find test directories."""
    tests = []
    for d in path.iterdir():
        if d.is_dir() and 'test' in d.name.lower():
            tests.append(str(d.name))
    return tests


def detect_project_type(path: Path) -> str:
    """Detect the project type from manifests."""
    if (path / "pyproject.toml").exists():
        return "Python"
    if (path / "package.json").exists():
        return "Node.js/TypeScript"
    if (path / "Cargo.toml").exists():
        return "Rust"
    if (path / "go.mod").exists():
        return "Go"
    if (path / "pom.xml").exists():
        return "Java"
    if (path / "Gemfile").exists():
        return "Ruby"
    return "Unknown"


def generate_readme(path: Path = None, output: str = None) -> str:
    """Generate a complete README.md."""
    if path is None:
        path = Path.cwd()

    manifest = find_manifest(path)
    scripts = find_scripts(path)
    config_files = find_config_files(path)
    test_dirs = find_test_dirs(path)
    project_type = detect_project_type(path)
    project_name = manifest.get("name", path.name)
    description = manifest.get("description", f"{project_type} project")

    # Generate README content
    readme = f"""# {project_name}

[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

{description}

## Features

<!-- Add your project's key features here -->

## Installation

```bash
# Install dependencies
"""

    if project_type == "Python":
        readme += """uv sync
# Or with extras:
uv sync --extra all
"""
    elif project_type == "Node.js/TypeScript":
        readme += """npm install
# Or with yarn:
yarn install
"""

    readme += f"""

## Quick Start

```bash
# Run the project
"""

    if scripts:
        for script in scripts[:3]:  # Show first 3 scripts
            readme += f"{script['command']}\n"
    else:
        readme += "# Add your start command here\n"

    readme += f"""

## Usage

"""

    if scripts:
        for script in scripts:
            readme += f"### {script['name']}\n\n```bash\n{script['command']}\n```\n\n"
    else:
        readme += "Add usage examples here.\n"

    readme += f"""

## Configuration

"""

    if config_files:
        readme += "Configuration files:\n"
        for cf in config_files[:5]:
            readme += f"- `{cf}`\n"
    else:
        readme += "No configuration files found.\n"

    readme += f"""

## Project Structure

```
{project_name}/
"""

    # List top-level directories
    for d in sorted(path.iterdir()):
        if d.is_dir() and not d.name.startswith('.') and d.name != 'node_modules':
            readme += f"  {d.name}/\n"
    readme += "```\n\n"

    readme += f"""
## Development

```bash
# Run tests
"""

    if test_dirs:
        readme += f"uv run pytest tests/\n" if project_type == "Python" else "npm test\n"
    else:
        readme += "# Add test command here\n"

    readme += """
# Lint
uv run ruff check .\n""" if project_type == "Python" else "npm run lint\n"

    readme += f"""

## Contributing

<!-- Add contribution guidelines -->

## License

MIT License
"""

    # Write output
    if output:
        Path(output).write_text(readme)
        print(f"README generated → {output}")
    else:
        print(readme)

    return readme


def main():
    parser = argparse.ArgumentParser(description="Generate README from project structure")
    parser.add_argument("--path", help="Path to project directory")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    path = Path(args.path) if args.path else Path.cwd()
    if not path.exists():
        print(f"Error: {path} does not exist")
        sys.exit(1)

    generate_readme(path, args.output)
    sys.exit(0)


if __name__ == "__main__":
    main()
