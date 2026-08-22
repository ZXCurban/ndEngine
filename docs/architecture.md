# Architecture

> **The engine doesn't even know what a cube is.**

## Layers

```text
CLI
 ↓
TUI
 ↓
Renderer
 ↓
Projection
 ↓
Scene
 ↓
Geometry
 ↓
Math
```

## Rules

- Core не зависит от TUI/CLI/конкретного renderer.
- Размерность всегда определяется данными, а не кодом.
- Никаких if dimensions == 3.
- Core не знает о Cube, Tesseract и других конкретных фигурах.
- Фигуры создаются генераторами и возвращаются как Geometry.
- Renderer работает с результатом projection, а не с конкретными фигурами.
- Каждый слой отвечает только за свою задачу.

## Pipeline
```text
 → Geometry
 → Transform
 → Camera
 → Projection
 → Renderer
 → Terminal
```