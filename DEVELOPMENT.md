# Development Guide

## Rules

### Version Control System (VCS)

#### Branch Naming Convention

All branch names must start with the corresponding issue number (create a new issue if one doesn't exist yet), followed by a short description in **kebab-case**.

**Examples:**
1. `15-fix-some-bug`
2. `453-add-new-feature`

#### Commit Message Convention

All commit messages must start with a hashtag followed by the issue number, a colon, and a concise description. For initial commits, use a prefix like `init:`. If the issue does not yet exist, create one and use its number.

**Examples:**
1. `#15: fix some bug`
2. `#453: add new feature`

## Technology stack

### Development

- Python (3.12)
- pytest
- uv
- ruff
- pyright

### For LLM

- vLLM
- qdrant
- Self-written lightweight SDK

### Interfaces

- Typer
- FastAPI
- MCP

### Sources

- docling (for PDF)
- ...
