---
name: technical-documentation-with-claude
description: Enforce a 5-phase documentation workflow that verifies code reality against docs using grep and structured templates. Use this skill when writing API documentation, user guides, technical reference docs, or any documentation that must accurately reflect the actual codebase. Triggers on tasks involving technical documentation, API docs, inline documentation, code comments, developer guides, or documentation review and verification.
---

# Technical Documentation with Claude

Enforce a rigorous 5-phase documentation workflow that ensures all documentation accurately reflects the actual codebase. No stale docs — every line verified against code reality.

## The 5-Phase Workflow

### Phase 1: Audit

**Goal**: Understand the current state of code and documentation.

**Actions**:
1. **Scan existing docs**: Read all markdown files, docstrings, README, CHANGELOG
2. **Map code structure**: List all modules, classes, functions, APIs, endpoints
3. **Identify gaps**: Find undocumented functions, outdated examples, missing sections
4. **Check for drift**: Compare doc claims against actual code behavior

**Tools**:
- `grep` for function/class definitions
- `find` for existing documentation files
- AST parsing for language-specific analysis

**Output**: Documentation audit report listing what's documented, what's missing, what's stale.

### Phase 2: Structure

**Goal**: Design the documentation architecture.

**Actions**:
1. **Choose documentation type**:
   - API reference (auto-generated from code)
   - User guide (how-to instructions)
   - Tutorial (step-by-step walkthrough)
   - Concept guide (explanatory articles)
   - Reference (specification-style docs)
2. **Define section hierarchy**: Main sections → subsections → examples
3. **Create templates**: Standardized templates for each doc type
4. **Plan cross-references**: Links between related sections

**Template Structure**:
```
[Title]
[Overview paragraph]

## Description
What this module/function/class does

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|

## Returns
[Return type and description]

## Examples
```python
# Working example code
```

## Raises
[List of exceptions]

## See Also
[Related functions/classes]
```

### Phase 3: Generate

**Goal**: Write documentation based on actual code.

**Rules**:
1. **Every claim must be verifiable**: Reference actual code, file paths, line numbers
2. **Use grep to confirm**: Before writing about any function, verify it exists
3. **Read source files**: Don't guess parameter names or types — read the source
4. **Match code style**: Documentation tone matches the project's existing docs
5. **Include working examples**: All code blocks must be runnable

**Process for each item**:
```
1. Find the code definition (grep/search)
2. Read the full function/class body
3. Extract parameters, return type, exceptions
4. Write the docstring/reference entry
5. Verify the example code compiles/runs
6. Cross-reference related items
```

### Phase 4: Verify

**Goal**: Ensure docs match code reality.

**Verification Checklist**:
- [ ] Every function/class mentioned in docs exists in code
- [ ] Every parameter name matches the actual signature
- [ ] Every return type is accurate
- [ ] Every example code block is runnable
- [ ] Every URL/path reference resolves correctly
- [ ] No contradictions between different doc sections
- [ ] No outdated information from previous versions

**Verification Commands**:
```bash
# Check function exists
grep -r "function_name" src/

# Verify parameter names
grep -r "def function_name" src/

# Check example code runs
python -c "import example_code"

# Verify docstring consistency
python -c "import ast; print(ast.get_docstring(ast.parse(open('file.py').read())))"
```

### Phase 5: Maintain

**Goal**: Keep documentation current as code evolves.

**Rules**:
1. **Documentation lives with code**: Co-located in same commits
2. **Update docs on every change**: If code changes, docs must follow
3. **Automate validation**: Pre-commit hooks that check doc consistency
4. **Review process**: Every PR includes a doc review step
5. **Schedule audits**: Quarterly documentation review using this skill

**Automation**:
- Pre-commit hook: `doc-validator` checks for doc drift
- CI integration: `docs-check` verifies all examples run
- Scheduled: Monthly `doc-audit` using Phase 1

## When to Use This Skill

- Writing initial technical documentation for a new project
- Reviewing existing documentation for accuracy
- Adding API documentation to existing code
- Creating user guides and tutorials
- Preparing documentation for release or open sourcing
- Auditing documentation quality before a presentation or demo

## Integration

- `readme-generator` for project-level overview docs
- `skill-creator` for creating new project-specific skills
- `humanize-writing` for making technical prose accessible
- `changelog-generator` for release documentation

## Common Pitfalls

- Writing docs before code is stable — document after implementation
- Copying parameter docs from other languages — always read the actual source
- Forgetting to update docs when code changes — link docs to code changes
- Using vague descriptions — be specific with actual values and examples
- Over-documenting simple things — focus on complexity and non-obvious behavior
