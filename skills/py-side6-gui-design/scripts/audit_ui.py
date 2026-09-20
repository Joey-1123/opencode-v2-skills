#!/usr/bin/env python3
"""
PySide6 UI Auditor - Audit PySide6 UI code for design best practices

Usage:
    python audit_ui.py --file <ui_file.py> [--report <report.json>]
"""

import sys
import re
import json
import argparse
from pathlib import Path


DESIGN_TOKENS = {
    "colors": ["#2563EB", "#F97316", "#22C55E", "#EF4444", "#EAB308", "#1E293B", "#F8FAFC", "#64748B"],
    "focus": True,
    "layouts": ["QVBoxLayout", "QHBoxLayout", "QGridLayout", "QStackedLayout"],
}

ISSUES = []


def check_color_consistency(content: str, filepath: str):
    """Check for hardcoded colors not in design tokens."""
    hex_colors = re.findall(r'#[0-9A-Fa-f]{6}', content)
    for color in hex_colors:
        if color.upper() not in [c.upper() for c in DESIGN_TOKENS["colors"]]:
            ISSUES.append({
                "file": filepath,
                "severity": "warning",
                "message": f"Non-standard color {color} — use design tokens",
                "fix": "Add to DESIGN_TOKENS and reference by variable name"
            })


def check_threading(content: str, filepath: str):
    """Check for blocking operations on main thread."""
    blocking_patterns = [
        r'time\.sleep\(', r'while True:', r'for \w+ in range\(\d+\):',
        r'librosa\.', r'cv2\.', r'pandas\.read_', r'time\.process_time\('
    ]
    for pattern in blocking_patterns:
        if re.search(pattern, content) and 'QThread' not in content and 'QtConcurrent' not in content:
            ISSUES.append({
                "file": filepath,
                "severity": "error",
                "message": f"Blocking operation detected: {pattern}",
                "fix": "Move to QThread or QtConcurrent.run()"
            })
            break


def check_accessibility(content: str, filepath: str):
    """Check for accessibility attributes."""
    if 'QPushButton' in content or 'QAction' in content:
        if 'setAccessibleName' not in content:
            ISSUES.append({
                "file": filepath,
                "severity": "warning",
                "message": "Interactive widgets missing setAccessibleName",
                "fix": "Add setAccessibleName() to all buttons, actions, and interactive widgets"
            })


def check_focus_policy(content: str, filepath: str):
    """Check that interactive widgets have focus policy."""
    if 'QPushButton' in content and 'setFocusPolicy' not in content:
        ISSUES.append({
            "file": filepath,
            "severity": "warning",
            "message": "Buttons without explicit focus policy",
            "fix": "Add setFocusPolicy(Qt.StrongFocus)"
        })


def check_layout_usage(content: str, filepath: str):
    """Check that layouts are used instead of absolute positioning."""
    if 'setGeometry(' in content or 'setFixedPos(' in content:
        if 'QVBoxLayout' not in content and 'QHBoxLayout' not in content:
            ISSUES.append({
                "file": filepath,
                "severity": "error",
                "message": "Absolute positioning detected without layout managers",
                "fix": "Use QVBoxLayout/QHBoxLayout/QGridLayout instead"
            })


def check_stylesheet(content: str, filepath: str):
    """Check for centralized styling."""
    if 'setStyleSheet(' in content and 'QSS' not in filepath:
        pass  # Individual style sheets are OK for small apps


def audit_file(filepath: str) -> list:
    """Audit a single file for design issues."""
    content = Path(filepath).read_text()
    check_color_consistency(content, filepath)
    check_threading(content, filepath)
    check_accessibility(content, filepath)
    check_focus_policy(content, filepath)
    check_layout_usage(content, filepath)
    return ISSUES


def main():
    parser = argparse.ArgumentParser(description="Audit PySide6 UI code for design best practices")
    parser.add_argument("--file", required=True, help="Python file to audit")
    parser.add_argument("--report", help="Output JSON report file")
    args = parser.parse_args()

    filepath = args.file
    if not Path(filepath).exists():
        print(f"Error: {filepath} not found")
        sys.exit(1)

    global ISSUES
    ISSUES = audit_file(filepath)

    if not ISSUES:
        print(f"✅ {filepath} passes all design audits")
        sys.exit(0)

    print(f"⚠️  {len(ISSUES)} issue(s) found in {filepath}:")
    print("-" * 60)
    for issue in ISSUES:
        icon = "❌" if issue["severity"] == "error" else "⚠️"
        print(f"{icon} [{issue['severity'].upper()}] {issue['message']}")
        print(f"   Fix: {issue['fix']}")
        print()

    if args.report:
        Path(args.report).write_text(json.dumps(ISSUES, indent=2))
        print(f"Report saved to {args.report}")

    sys.exit(1 if any(i["severity"] == "error" for i in ISSUES) else 0)


if __name__ == "__main__":
    main()
