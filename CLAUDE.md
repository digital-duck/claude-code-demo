# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code demonstration repository containing examples and documentation for using Claude CLI. It serves as a reference for Claude Code functionality and usage patterns.

## Repository Structure

- `README.md` - Main documentation with setup instructions and OpenRouter.ai configuration
- `cheatsheet.md` - Comprehensive Claude CLI command reference guide
- `claude-code-cheatsheet.pdf` - PDF version of the cheatsheet
- `.gitignore` - Python-focused gitignore with additional tooling (Ruff, Cursor, Marimo, etc.)

## Development Environment

This repository is configured for Python development with comprehensive ignore patterns for:
- Python artifacts (bytecode, distributions, virtual environments)
- Testing and coverage tools
- Documentation builds
- Modern Python tooling (UV, Poetry, PDM, Pixi, Ruff)
- IDE configurations (PyCharm, VSCode, Cursor)
- AI and data science tools (Jupyter, Marimo, Abstra)

## Setup Instructions

The repository references external setup documentation at:
https://github.com/wgong/py4kids/blob/master/lesson-18-ai/SWE/Code-Collab/readme-claude-code.md

## OpenRouter.ai Integration

The project includes configuration for using Claude Code with OpenRouter.ai:
```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1"
export ANTHROPIC_AUTH_TOKEN="or_xxxxxxxxx"
export ANTHROPIC_MODEL="openai/gpt-oss-20b"
```

## Available Commands

This repository does not contain build scripts or package management files. It's primarily a documentation and example repository.

## Key Features

- Contains a comprehensive Claude CLI cheatsheet covering:
  - Installation and setup
  - Interactive and non-interactive usage
  - Session management and resumption
  - In-session slash commands
  - Important flags and configuration options