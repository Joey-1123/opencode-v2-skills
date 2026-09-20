# OpenCode V2 Skills

A comprehensive collection of OpenCode skills for design, documentation, animation, 3D development, and Python desktop GUI applications.

**157 total skills** — covering everything from web development to Python desktop apps.

## Quick Stats

| Metric | Count |
|--------|-------|
| **Total Skills** | 157 |
| **From freshtechbro/claudedesignskills** | 22 (MIT) |
| **From ComposioHQ/awesome-claude-skills** | 1 (Apache 2.0) |
| **Created for RingForge** | 1 |
| **Created from scratch** | 2 |
| **Universal (framework-agnostic)** | 1 |

## Skill Categories

### 🎨 Design & UI
- `py-side6-gui-design` — Universal Python desktop GUI design (PySide6/PyQt)
- `modern-web-design` — Modern web design principles, trends, and patterns
- `skill-creator` — Guide for creating effective OpenCode skills

### 📄 Documentation
- `readme-generator` — Generate polished README.md from project structure
- `technical-documentation-with-claude` — 5-phase documentation workflow with code verification
- `changelog-generator` — Transform git commits into user-facing release notes

### 🎬 Animation & Interaction
- `animate` — Build animations from scratch with Emil Kowalski's philosophy
- `motion-framer` — React/JS animation with spring physics, gestures, layout animations
- `gsap-scrolltrigger` — Scroll-driven animations, timelines, parallax
- `react-spring-physics` — Physics-based animations and gesture-driven interfaces
- `animejs` — Timeline-based animations, SVG morphing, stagger effects
- `lottie-animations` — After Effects animation rendering for web and React
- `review-animations` — Review animation code against craft standards
- `improve-animations` — Audit and improve existing animation code
- `animation-vocabulary` — Reverse-lookup glossary for animation effects
- `find-animation-opportunities` — Find places that don't animate but should

### 🎯 3D & WebGL
- `threejs-webgl` — Three.js 3D web development
- `react-three-fiber` — Declarative 3D scenes with React
- `babylonjs-engine` — Babylon.js 3D game engine
- `playcanvas-engine` — Lightweight WebGL game engine
- `aframe-webxr` — WebXR/VR/AR with HTML entity-component architecture
- `lightweight-3d-effects` — Vanta.js, Zdog, Vanilla-Tilt pseudo-3D effects
- `pixijs-2d` — PixiJS 2D rendering engine
- `blender-web-pipeline` — Blender to web export workflows
- `spline-interactive` — Browser-based 3D design tool
- `rive-interactive` — State machine vector animations
- `substance-3d-texturing` — Substance 3D Painter texturing workflow

### 📜 Scroll & Page Transitions
- `barba-js` — Page transitions and smooth navigation
- `locomotive-scroll` — Smooth scrolling with parallax
- `scroll-reveal-libraries` — Simple scroll-triggered reveals (AOS)

### 🧩 Components & Integration
- `animated-component-libraries` — Pre-built animated React components
- `web3d-integration-patterns` — Combining 3D and animation libraries
- `react-three-fiber` — React Three Fiber patterns

### 🛠️ Tooling
- `skill-creator` — Create, validate, and package OpenCode skills

## Install All Skills

```bash
# Clone this repo
git clone https://github.com/Joey-1123/opencode-v2-skills.git

# Copy skills to OpenCode
cp -r opencode-v2-skills/skills/* ~/.config/opencode/skills/
```

Or install individually:

```bash
# Design
cp -r skills/py-side6-gui-design ~/.config/opencode/skills/
cp -r skills/modern-web-design ~/.config/opencode/skills/
cp -r skills/skill-creator ~/.config/opencode/skills/

# Documentation
cp -r skills/readme-generator ~/.config/opencode/skills/
cp -r skills/technical-documentation-with-claude ~/.config/opencode/skills/
cp -r skills/changelog-generator ~/.config/opencode/skills/

# Animation
cp -r skills/animate ~/.config/opencode/skills/
# ... etc
```

## Skill Format

All skills follow the [OpenCode skill format](https://docs.opencode.ai/skills):

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── scripts/          # Optional: Executable Python/Bash scripts
├── references/       # Optional: Documentation loaded on demand
└── assets/           # Optional: Templates, stylesheets, icons
```

## License

- `py-side6-gui-design`, `readme-generator`, `technical-documentation-with-claude` — **MIT** (created by Joey-1123)
- freshtechbro skills — **MIT License** (from [freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills))
- ComposioHQ skills — **Apache 2.0** (from [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills))

## Contributing

1. Fork this repository
2. Create a new skill directory with `SKILL.md`
3. Validate with `skill-creator/scripts/quick_validate.py`
4. Submit a Pull Request

## Changelog

### v1.0.0 — Initial Release
- 27 skills from freshtechbro/claudedesignskills
- 1 skill from ComposioHQ/awesome-claude-skills
- 3 original skills (py-side6-gui-design, readme-generator, technical-documentation-with-claude)
- Full scripts, references, and assets for all skills

## Acknowledgments

- [freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills) — Original 22 design/3D/animation skills
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — changelog-generator skill
- [Anthropic](https://anthropic.com) — Claude Skills format specification
- [OpenCode](https://opencode.ai) — OpenCode skill platform
