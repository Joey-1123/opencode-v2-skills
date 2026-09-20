---
name: readme-generator
description: Generates a complete, polished README.md by scanning the actual project structure, dependencies, and code. Use this skill when a project needs documentation, when writing a README from scratch, or when updating project documentation. Triggers on tasks involving README creation, project documentation, project setup instructions, tech stack overview, usage examples, or configuration guides. Works by scanning pyproject.toml, package.json, setup.py, Cargo.toml, go.mod, and other manifests for real install steps, scripts, and dependencies.
---

# Readme Generator

Generates a complete, polished README.md by scanning the actual project structure, dependencies, and code. No hallucinated boilerplate — documentation that matches the code.

## When to Use This Skill

- Starting a new project and need a README
- Updating an existing README after major changes
- Open sourcing a project
- Adding a new dependency or feature
- Writing documentation for a code review or presentation

## How It Works

### Phase 1: Project Scanning

Scan the repository to understand what the project actually is:

1. **Read project manifests**: `pyproject.toml`, `package.json`, `setup.py`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile`
2. **Identify project name and description**: From manifest `name` and `description` fields
3. **Extract dependencies**: All runtime and dev dependencies with versions
4. **Find scripts/commands**: From `scripts`, `bin`, or command configurations
5. **Read configuration files**: `.env.example`, `config.*`, `settings.*`
6. **Scan test structure**: Test directories, test frameworks
7. **Check for docs**: Existing `docs/`, `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`
8. **Identify project type**: CLI tool, library, application, framework

### Phase 2: Content Generation

Generate the README with these sections (adapt as needed):

#### Required Sections

1. **Title** — Project name from manifest
2. **Description** — One-liner summary from manifest or project root
3. **Badges** — Version, license, CI status (if available)
4. **Features** — Bullet list of key capabilities
5. **Installation** — Actual commands from project manifests
6. **Usage** — Code examples based on actual scripts/commands
7. **Configuration** — Config file paths and key settings
8. **Project Structure** — Directory layout with descriptions
9. **Development** — How to run tests, build, lint
10. **Contributing** — Guidelines if CONTRIBUTING.md exists
11. **License** — From LICENSE file

#### Optional Sections

- **Quick Start** — Minimal example to get running
- **Examples** — Real code examples from the codebase
- **API Reference** — For libraries with documented APIs
- **Changelog** — Link to CHANGELOG.md
- **Authors** — From contributors or config files

### Phase 3: Validation

After generating the README:

1. **Verify install commands work**: Check that `pip install`, `npm install`, etc. match actual manifests
2. **Verify script names match**: Commands in Usage must match actual `scripts` or `bin` entries
3. **Check for consistency**: All mentioned files/dirs must actually exist
4. **Review formatting**: Consistent code blocks, no broken links

## Project Type Detection

| Manifest File | Project Type | Install Command |
|--------------|-------------|----------------|
| `pyproject.toml` | Python | `pip install -e .` or `uv sync` |
| `package.json` | Node.js/TypeScript | `npm install` or `yarn` |
| `setup.py` | Python (legacy) | `pip install -e .` |
| `Cargo.toml` | Rust | `cargo build` |
| `go.mod` | Go | `go build` |
| `pom.xml` | Java | `mvn install` |
| `Gemfile` | Ruby | `bundle install` |

## Template Structure

```markdown
# [Project Name]

[Badges]

[Description]

## Features

- [Feature 1]
- [Feature 2]
- [Feature 3]

## Installation

```bash
# Actual install commands from project manifest
```

## Quick Start

```bash
# Minimal working example
```

## Usage

[Actual usage examples based on scripts/commands]

## Configuration

[Config file paths and key settings]

## Project Structure

[Directory tree with descriptions]

## Development

```bash
# Test, build, lint commands
```

## Contributing

[From CONTRIBUTING.md if exists]

## License

[From LICENSE file]
```

## Best Practices

1. **Never hallucinate**: Only include commands and features that actually exist in the codebase
2. **Use actual manifest data**: Read `pyproject.toml`/`package.json` for real dependencies and scripts
3. **Keep it concise**: README should be scannable in 60 seconds
4. **Include copy-paste commands**: Every code block should be runnable
5. **Update existing READMEs**: Don't overwrite manual sections that contain human insights

## Integration

- Works with `skill-creator` to create new project skills
- References `changelog-generator` for release documentation
- Use `humanize-writing` to make prose sound natural

## Common Pitfalls

- Writing "Coming Soon" sections — only document what exists
- Including fictional API docs — base on actual code structure
- Copying README templates verbatim — customize for each project
- Forgetting to verify install commands — always match actual manifests

## Scripts

- `generate_readme.py` — Main generator script
- `validate_readme.py` — Verifies README consistency with codebase
