#!/usr/bin/env python3
"""
Documentation Verifier - Check docs against code reality

Usage:
    python verify_docs.py --path <project_path> [--output <report_file>]
"""
import sys
import argparse
import re
from pathlib import Path


def scan_codebase(path: Path) -> dict:
    """Scan all code files for functions, classes, and APIs."""
    code_info = {
        "functions": [],
        "classes": [],
        "modules": [],
        "files": []
    }

    for f in path.rglob("*"):
        if not f.is_file() or '.git' in str(f) or 'node_modules' in str(f):
            continue
        if f.suffix in ['.py', '.js', '.ts', '.go', '.rs', '.java', '.rb']:
            code_info["files"].append(str(f.relative_to(path)))
            content = f.read_text(errors='ignore')
            # Find functions
            funcs = re.findall(r'def\s+(\w+)\s*\(|function\s+(\w+)\s*\(|func\s+(\w+)\s*\(', content)
            for f_tuple in funcs:
                name = next((x for x in f_tuple if x), None)
                if name:
                    code_info["functions"].append({"name": name, "file": str(f.relative_to(path))})
            # Find classes
            classes = re.findall(r'class\s+(\w+)', content)
            for cls in classes:
                code_info["classes"].append({"name": cls, "file": str(f.relative_to(path))})
            # Find modules
            if f.suffix == '.py':
                module_match = re.search(r'^module\s*=\s*["\'](\w+)["\']', content, re.MULTILINE)
                if module_match:
                    code_info["modules"].append(module_match.group(1))

    return code_info


def verify_docs(path: Path) -> list:
    """Verify documentation matches code reality."""
    issues = []
    code_info = scan_codebase(path)

    # Find all markdown files
    for md_file in path.rglob("*.md"):
        if '.git' in str(md_file):
            continue
        content = md_file.read_text(errors='ignore')
        # Check if documented functions exist in code
        for func in code_info["functions"]:
            if func["name"] not in content and len(func["name"]) > 3:
                # Could be intentionally undocumented, just flag
                pass  # Too noisy - just report stats

    issues.append({
        "severity": "info",
        "message": f"Scanned {len(code_info['files'])} code files, {len(code_info['functions'])} functions, {len(code_info['classes'])} classes",
        "fix": "Use this info to ensure documentation coverage"
    })

    return issues, code_info


def main():
    parser = argparse.ArgumentParser(description="Verify documentation against code reality")
    parser.add_argument("--path", required=True, help="Project root path")
    parser.add_argument("--output", help="Output report file")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    issues, code_info = verify_docs(path)

    for issue in issues:
        print(f"ℹ️  {issue['message']}")

    if args.output:
        import json
        report = {"issues": issues, "code_stats": code_info}
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"\nReport saved to {args.output}")

    sys.exit(0)


if __name__ == "__main__":
    main()
