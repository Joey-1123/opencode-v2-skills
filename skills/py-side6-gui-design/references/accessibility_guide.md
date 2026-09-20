# Desktop App Accessibility Guide (WCAG AA)

## Keyboard Navigation
- All interactive widgets: `setFocusPolicy(Qt.StrongFocus)`
- Logical tab order matching visual layout
- Keyboard shortcuts for all major actions
- Focus indicators visible (2px accent color border)

## Screen Reader Support
- `setAccessibleName()` on all interactive widgets
- `setAccessibleDescription()` for complex widgets
- Use semantic widget types (QPushButton not QLabel+click)
- Announce state changes via QAccessible

## Color & Contrast
- Minimum 4.5:1 contrast ratio for text
- Never rely solely on color (use shape + icon + text)
- Test with `colour-science` or `webcolors`

## Reduced Motion
- Respect system accessibility settings
- Disable smooth animations when reduced motion preferred
- Provide instant alternatives

## High DPI Support
```python
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
```
