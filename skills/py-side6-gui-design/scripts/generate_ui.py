#!/usr/bin/env python3
"""
PySide6 UI Generator - Generate generic PySide6 UI components from templates

Usage:
    python generate_ui.py --pattern <pattern> --output <file.py>
    python generate_ui.py --list

Patterns:
    main_window     - Main application window with menu bar, toolbar, status bar
    toolbar         - Toolbar with action buttons
    datalist        - Searchable data list with filter, sort, detail panel
    settings_dialog - Preferences/settings dialog with categories
    progress_view   - Progress/processing view with task list
    search_view     - Searchable list with instant filtering
    split_view      - Split-pane editor with sidebar + main area
    form_builder    - Form with labeled fields and validation
    status_bar      - Status bar with progress, indicators, and messages
    empty_state     - Empty state placeholder with call-to-action
"""

import sys
import argparse
from pathlib import Path


PATTERNS_INFO = {
    "main_window": {
        "desc": "Main application window with menu, toolbar, status bar",
        "imports": "from PySide6.QtWidgets import QMainWindow, QMenuBar, QToolBar, QStatusBar, QVBoxLayout, QWidget\nfrom PySide6.QtCore import Qt, Signal\nfrom PySide6.QtGui import QAction",
        "code": '''class MainWindow(QMainWindow):
    """Main application window with menu bar, toolbar, and status bar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application")
        self.setMinimumSize(800, 600)
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_status_bar()
        self._setup_central_widget()

    def _setup_menu_bar(self):
        menu_bar = self.menuBar()
        # File menu
        file_menu = menu_bar.addMenu("&File")
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

    def _setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

    def _setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _setup_central_widget(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)'''
    },
    "toolbar": {
        "desc": "Toolbar with action buttons",
        "imports": "from PySide6.QtWidgets import QToolBar, QPushButton, QAction\nfrom PySide6.QtCore import Qt",
        "code": '''class ToolBar(QToolBar):
    """Toolbar with action buttons and separators."""

    def __init__(self, title="Toolbar", parent=None):
        super().__init__(title, parent)
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))

    def add_action(self, name: str, icon: str = None, shortcut: str = None, callback=None):
        action = QAction(name, self)
        if shortcut:
            action.setShortcut(shortcut)
        if callback:
            action.triggered.connect(callback)
        self.addAction(action)
        return action

    def add_separator(self):
        self.addSeparator()'''
    },
    "datalist": {
        "desc": "Searchable data list with filter, sort, detail panel",
        "imports": "from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QLabel\nfrom PySide6.QtCore import Qt, Signal, QStringListModel\nfrom PySide6.QtGui import QFilterProxyModel",
        "code": '''class DataList(QWidget):
    """Searchable data list with filter and detail display."""
    item_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        # Search bar
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.setAccessibleName("Search data")
        self.search.textChanged.connect(self._filter)
        layout.addWidget(self.search)

        # List
        self.list_widget = QListWidget()
        self.list_widget.setAccessibleName("Data list")
        self.list_widget.itemClicked.connect(
            lambda item: self.item_selected.emit(item.data(Qt.UserRole)))
        layout.addWidget(self.list_widget)

        # Detail panel
        self.detail = QLabel("Select an item to see details")
        self.detail.setStyleSheet("padding: 8px; background: #F8FAFC; border-radius: 8px;")
        layout.addWidget(self.detail)

    def set_items(self, items: list):
        self.list_widget.clear()
        for item in items:
            list_item = QListWidgetItem(str(item))
            list_item.setData(Qt.UserRole, item)
            self.list_widget.addItem(list_item)

    def _filter(self, text: str):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())'''
    },
    "settings_dialog": {
        "desc": "Preferences/settings dialog with categories",
        "imports": "from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QWidget\nfrom PySide6.QtCore import Qt, Signal",
        "code": '''class SettingsDialog(QDialog):
    """Settings/preferences dialog with category navigation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setMinimumSize(600, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        # Category list
        self.categories = QListWidget()
        self.categories.setAccessibleName("Settings categories")
        self.categories.setMaximumWidth(150)
        self.categories.setStyleSheet("""
            QListWidget::item:selected {
                background-color: #2563EB;
                color: white;
            }
        """)
        layout.addWidget(self.categories)

        # Content area
        self.content = QWidget()
        layout.addWidget(self.content)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_reset = QPushButton("Reset to Defaults")
        self.btn_apply = QPushButton("Apply")
        self.btn_ok = QPushButton("OK")
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_apply)
        btn_layout.addWidget(self.btn_ok)
        layout.addLayout(btn_layout)'''
    },
    "progress_view": {
        "desc": "Progress view with task list and status indicators",
        "imports": "from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QListWidget, QListWidgetItem\nfrom PySide6.QtCore import Qt, Signal",
        "code": '''class ProgressView(QWidget):
    """Progress view with task list and status bar."""
    task_complete = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Overall progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setAccessibleName("Overall progress")
        layout.addWidget(self.progress_bar)

        # Task list
        self.task_list = QListWidget()
        self.task_list.setAccessibleName("Task list")
        layout.addWidget(self.task_list)

        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAccessibleName("Status message")
        layout.addWidget(self.status_label)

    def add_task(self, name: str, status: str = "Queued"):
        item = QListWidgetItem(f"{name} — {status}")
        self.task_list.addItem(item)'''
    },
    "search_view": {
        "desc": "Searchable list with instant filtering and keyboard navigation",
        "imports": "from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem\nfrom PySide6.QtCore import Qt, Signal",
        "code": '''class SearchView(QWidget):
    """Searchable list with instant filtering."""
    item_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Type to search...")
        self.search.setAccessibleName("Search input")
        self.search.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.search)

        self.list_widget = QListWidget()
        self.list_widget.setAccessibleName("Search results")
        self.list_widget.itemClicked.connect(
            lambda item: self.item_selected.emit(item.text()))
        layout.addWidget(self.list_widget)'''
    },
    "split_view": {
        "desc": "Split-pane layout with resizable sidebar and main content",
        "imports": "from PySide6.QtWidgets import QSplitter, QWidget, QVBoxLayout, QListWidget\nfrom PySide6.QtCore import Qt",
        "code": '''class SplitView(QWidget):
    """Split-pane layout with resizable sidebar and main area."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setAccessibleName("Sidebar navigation")
        self.sidebar.setMinimumWidth(200)
        splitter.addWidget(self.sidebar)

        # Main content
        self.main = QWidget()
        self.main.setStyleSheet("background-color: white;")
        splitter.addWidget(self.main)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        layout.addWidget(splitter)'''
    },
    "form_builder": {
        "desc": "Form with labeled fields and validation",
        "imports": "from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QComboBox\nfrom PySide6.QtCore import Qt, Signal",
        "code": '''class FormBuilder(QWidget):
    """Form with labeled fields and validation."""
    submitted = Signal(dict)

    def __init__(self, fields: list = None, parent=None):
        super().__init__(parent)
        self.fields = fields or []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.field_widgets = {}

        for field in self.fields:
            row = QHBoxLayout()
            label = QLabel(f"{field['label']}:")
            label.setMinimumWidth(120)

            widget = self._create_widget(field)
            widget.setAccessibleName(field['name'])

            row.addWidget(label)
            row.addWidget(widget)
            layout.addLayout(row)
            self.field_widgets[field['name']] = widget

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setAccessibleName("Submit form")
        self.submit_btn.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.submit_btn)

    def _create_widget(self, field: dict):
        ftype = field.get('type', 'text')
        if ftype == 'text':
            return QLineEdit()
        elif ftype == 'number':
            return QSpinBox()
        elif ftype == 'select':
            combo = QComboBox()
            combo.addItems(field.get('options', []))
            return combo
        return QLineEdit()'''
    },
    "status_bar": {
        "desc": "Status bar with progress, indicators, and messages",
        "imports": "from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar\nfrom PySide6.QtCore import Qt",
        "code": '''class AppStatusBar(QStatusBar):
    """Status bar with progress indicator and messages."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._message_label = QLabel("Ready")
        self._progress = QProgressBar()
        self._progress.setRange(0, 0)  # Indeterminate
        self._progress.setFixedWidth(150)
        self._progress.setVisible(False)
        self.addWidget(self._message_label)
        self.addWidget(self._progress)

    def show_message(self, text: str):
        self._message_label.setText(text)

    def show_progress(self, visible: bool = True):
        self._progress.setVisible(visible)

    def set_progress_text(self, text: str):
        self._message_label.setText(text)'''
    },
    "empty_state": {
        "desc": "Empty state placeholder with call-to-action",
        "imports": "from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton\nfrom PySide6.QtCore import Qt, Signal",
        "code": '''class EmptyState(QWidget):
    """Empty state placeholder with icon, text, and call-to-action button."""
    action_clicked = Signal()

    def __init__(self, title: str = "Nothing here yet",
                 description: str = "Get started by adding your first item.",
                 action_text: str = "Add Item",
                 parent=None):
        super().__init__(parent)
        self._setup_ui(title, description, action_text)

    def _setup_ui(self, title, description, action_text):
        layout = QVBoxLayout(self)
        layout.addStretch()

        icon = QLabel("📁")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #64748B;")
        layout.addWidget(desc_label)

        self.action_btn = QPushButton(action_text)
        self.action_btn.setFocusPolicy(Qt.StrongFocus)
        self.action_btn.clicked.connect(lambda: self.action_clicked.emit())
        layout.addWidget(self.action_btn)
        layout.addStretch()'''
    },
}


def generate(pattern_name: str) -> str:
    """Generate code for a specific pattern."""
    if pattern_name not in PATTERNS_INFO:
        available = ", ".join(PATTERNS_INFO.keys())
        return f"Error: Unknown pattern '{pattern_name}'. Available: {available}"
    info = PATTERNS_INFO[pattern_name]
    return f"{info['imports']}\n\n{info['code']}"


def main():
    parser = argparse.ArgumentParser(description="Generate PySide6 UI components")
    parser.add_argument("--pattern", help="Pattern to generate")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--list", action="store_true", help="List all patterns")
    args = parser.parse_args()

    if args.list:
        print("Available patterns:")
        for name in PATTERNS_INFO:
            print(f"  {name:20s} - {PATTERNS_INFO[name]['desc']}")
        sys.exit(0)

    if not args.pattern:
        parser.error("--pattern is required (use --list to see options)")

    code = generate(args.pattern)

    if code.startswith("Error:"):
        print(code)
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(code)
        print(f"Generated {args.pattern} -> {args.output}")
    else:
        print(code)

    sys.exit(0)


if __name__ == "__main__":
    main()
