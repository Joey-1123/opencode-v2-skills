# OpenCode V2 Skills

A comprehensive collection of **28 skills** for design, documentation, animation, 3D development, and Python desktop GUI applications — plus a **plugin manager** to auto-install and update them all.

## 🚀 Quick Start

### Option 1: Plugin Manager (Recommended)

```bash
# The plugin is already registered in your OpenCode config!
# Just run inside OpenCode:
/skill-manager install
```

This clones all skills from GitHub and sets them up automatically.

### Option 2: Manual Install

```bash
# Clone and copy
git clone https://github.com/Joey-1123/opencode-v2-skills.git
cp -r opencode-v2-skills/skills/* ~/.config/opencode/skills/
```

### Option 3: Install Script

```bash
cd opencode-v2-skills && bash install.sh
```

## 📊 Quick Stats

| Metric | Count |
|--------|-------|
| **Total Skills** | 28 |
| **From freshtechbro/claudedesignskills** | 22 (MIT) |
| **From ComposioHQ/awesome-claude-skills** | 1 (Apache 2.0) |
| **Original (Joey-1123)** | 3 (MIT) |
| **Plugin** | 1 skill-manager |

## 🛠️ Plugin Commands

Once installed, use these commands inside OpenCode:

| Command | Description |
|---------|-------------|
| `/skill-manager install` | Clone all skills from GitHub repo |
| `/skill-manager update` | Pull latest changes from repo |
| `/skill-manager list` | Show installed skills count |

## 📦 Skill Categories

### 🎨 Design & UI
- `py-side6-gui-design` — Universal Python desktop GUI design (PySide6/PyQt)
- `modern-web-design` — Modern web design principles, trends, and patterns
- `skill-creator` — Guide for creating effective OpenCode skills

### 📄 Documentation
- `readme-generator` — Generate polished README.md from project structure
- `technical-documentation-with-claude` — 5-phase documentation workflow with code verification
- `changelog-generator` — Transform git commits into user-facing release notes

### 🎬 Animation & Interaction
- `animate` — Build animations from scratch
- `motion-framer` — React/JS animation with spring physics
- `gsap-scrolltrigger` — Scroll-driven animations, timelines, parallax
- `react-spring-physics` — Physics-based animations and gesture interfaces
- `animejs` — Timeline-based animations, SVG morphing, stagger effects
- `lottie-animations` — After Effects animation rendering for web
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

### 🛠️ Tooling
- `skill-creator` — Create, validate, and package OpenCode skills

## 📁 Repo Structure

```
opencode-v2-skills/
├── skills/                    # All 28 skill directories
│   ├── py-side6-gui-design/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   ├── readme-generator/
│   ├── technical-documentation-with-claude/
│   └── ... (25 more)
├── plugins/
│   └── skill-manager.js       # Plugin for auto-management
├── install.sh                 # One-command install script
├── README.md
└── LICENSE                    # MIT
```

## 🔧 Install the Plugin Manually

If the plugin isn't auto-loaded:

```bash
# Copy plugin to OpenCode plugins directory
cp plugins/skill-manager.js ~/.config/opencode/plugins/

# Add to opencode.jsonc
# "plugins": ["skill-manager"]
```

## 📄 Skill Format

All skills follow the [OpenCode skill format](https://docs.opencode.ai/skills):

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── scripts/          # Optional: Executable Python/Bash scripts
├── references/       # Optional: Documentation loaded on demand
└── assets/           # Optional: Templates, stylesheets, icons
```

## 📜 Changelog

### v1.1.0 — Plugin Manager
- Added `skill-manager` plugin for auto-install/update/list
- Plugin registered in `opencode.jsonc`
- `install.sh` script for easy setup

### v1.0.0 — Initial Release
- 22 skills from freshtechbro/claudedesignskills
- 1 skill from ComposioHQ/awesome-claude-skills
- 3 original skills (py-side6-gui-design, readme-generator, technical-documentation-with-claude)
- Full scripts, references, and assets for all skills

## 📝 License

- Original skills (`py-side6-gui-design`, `readme-generator`, `technical-documentation-with-claude`, `skill-manager`) — **MIT**
- freshtechbro skills — **MIT License** (from [freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills))
- ComposioHQ skills — **Apache 2.0** (from [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills))

## 🤝 Contributing

1. Fork this repository
2. Create a new skill directory with `SKILL.md`
3. Validate with `skill-creator/scripts/quick_validate.py`
4. Submit a Pull Request

## Acknowledgments

- [freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills) — Original design/3D/animation skills
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — changelog-generator skill
- [OpenCode](https://opencode.ai) — OpenCode skill platform
