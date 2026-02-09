# SmartCommit - AI Git Commit Generator

A CLI tool that analyzes your git diff and generates meaningful, conventional commit messages using AI.

## Features

- 🤖 Analyzes git diff (staged or unstaged changes)
- ✨ Generates conventional commit messages (feat/fix/docs/style/refactor/test/chore)
- 🔄 Interactive mode - review and edit before committing
- 📚 Learns from your project commit history for better context
- 🎨 Supports custom commit message templates
- 🔗 Can be used as a git hook or standalone CLI

## Installation

```bash
pip install smartcommit
```

## Usage

### Basic usage

```bash
# Analyze staged changes and generate commit message
smartcommit

# Analyze unstaged changes
smartcommit --unstaged

# Interactive mode
smartcommit --interactive
```

### As a git hook

```bash
# Install as pre-commit hook
smartcommit --install-hook
```

## Configuration

Create a `.smartcommit.json` in your project root:

```json
{
  "commit_types": ["feat", "fix", "docs", "style", "refactor", "test", "chore"],
  "max_length": 72,
  "interactive": true,
  "learn_from_history": true
}
```

## License

MIT