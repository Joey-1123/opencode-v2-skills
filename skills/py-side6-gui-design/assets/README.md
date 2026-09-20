# PySide6 GUI Design Assets

## Templates
- `base_window.ui` — Main window template with menu bar, toolbar, status bar

## Stylesheets
- `base.qss` — Complete QSS theme with design tokens (colors, fonts, spacing)

## Icons
- SVG icon set for common actions (open, save, edit, delete, search, etc.)

## Usage
```python
from PySide6.QtWidgets import QApplication
app = QApplication([])
app.setStyleSheet(open("base.qss").read())
```
