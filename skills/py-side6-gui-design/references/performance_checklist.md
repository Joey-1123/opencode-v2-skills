# Desktop App Performance Checklist

## UI Responsiveness
- [ ] All heavy operations run in QThread or QtConcurrent
- [ ] UI never blocks (response < 16ms)
- [ ] Animations use QPropertyAnimation (not manual timers)
- [ ] Window resize is smooth (< 1 frame drop)

## Data Loading
- [ ] Large datasets use pagination or generators
- [ ] Lazy loading for lists > 1000 items
- [ ] QAbstractItemModel for efficient data views
- [ ] Progressive rendering (show rough, refine later)

## Memory
- [ ] Cache size bounded (LRU, max 100-500 items)
- [ ] Data unloaded when not visible
- [ ] No memory leaks (tracemalloc profiling)
- [ ] QPixmapCache for rendered images

## Rendering
- [ ] Use QGraphicsView for complex visuals
- [ ] Hardware acceleration enabled
- [ ] QSS stylesheets compiled once at startup
- [ ] Avoid excessive repaints (update() only when needed)
