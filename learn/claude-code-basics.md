prompt:

help me to get started with basics for using "claude-code" by anthropic


```bash
# mkdir -p ~/projects/wgong/claude-code-demo
cd ~/projects/digital-duck/claude-code-demo


```

I'll help you get started with Claude Code, which is Anthropic's official command-line tool for agentic coding. Let me search for the most current information about how to use it.Based on my search results, here's a comprehensive guide to get started with **Claude Code** by Anthropic:

## What is Claude Code?

Claude Code is Anthropic's official agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before. It can:

- **Build features from descriptions** - Tell Claude what you want in plain English
- **Debug and fix issues** - Describe bugs or paste error messages  
- **Navigate any codebase** - Ask questions about your team's codebase
- **Automate tedious tasks** - Fix lint issues, resolve merge conflicts, write release notes
- **Take direct action** - Edit files, run commands, and create commits

## Installation

### Quick Installation (Recommended)
```bash
# Install via npm (requires Node.js)

# .npm-global
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
# 1.0.72 (Claude Code)
```

### Alternative Installation Methods

**For macOS/Linux:**
```bash
# Install stable version
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version  
curl -fsSL https://claude.ai/install.sh | bash -s latest
```

**For Windows:**
```bash
# Install stable version (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest
```

## Authentication & Setup

### Option 1: Anthropic Console (Pay-per-use)
```bash
# Start Claude Code
claude

# This will prompt you to authenticate via the Anthropic Console
# You'll need active billing at console.anthropic.com
```

### Option 2: Claude Pro/Max Plan (Subscription)
If you have a Claude Pro ($20/month) or Max plan ($100-200/month):

```bash
# Start Claude Code
claude

# When prompted, log in with your Claude Pro/Max credentials
# This gives you shared rate limits across Claude web and Claude Code
```

## Basic Usage

### Getting Started
```bash
# Navigate to your project
cd your-awesome-project

# Start Claude Code
claude

/login  # use chat account subscription
```

### Basic Commands

**In Interactive Mode:**
```bash
# Ask Claude to build something
"Build an streamlit app with a chatbot using LLM models available at openrouter.ai"
"Build a simple REST API with user authentication"

# Debug an issue
"I'm getting this error: [paste error message]"

# Explain code
"Explain how this authentication middleware works"

# Fix problems
"Fix all the lint errors in this project"
```

**Print Mode (One-off commands):**
```bash
# Get quick answers without interactive session
claude -p "Explain this error message and suggest a fix"

# Analyze logs
tail -f app.log | claude -p "Alert me if you see any anomalies"
```

## Key Features & Commands

### Interactive Session Commands
Once in a Claude Code session, you can use these slash commands:

```bash
/help          # Show available commands
/clear         # Clear conversation context
/model         # Switch between Claude models (Sonnet 4, Opus 4)
/login         # Switch authentication method
/logout        # Log out
/bug           # Report issues to Anthropic
```

### Advanced Features

**Permission Control:**
```bash
# Run with automatic permissions (use carefully!)
claude --dangerously-skip-permissions

# Specify allowed tools
claude --allowedTools "Bash(git log:*)" "Read" 

# Specify disallowed tools  
claude --disallowedTools "Bash(rm:*)" "Edit"
```

**Working with Multiple Directories:**
```bash
# Add additional directories Claude can access
claude --add-dir ../frontend ../backend ../shared
```

## Best Practices

### 1. **Use /clear Frequently**
During long sessions, Claude's context window can fill with irrelevant conversation, file contents, and commands. This can reduce performance and sometimes distract Claude. Use the /clear command frequently between tasks to reset the context window.

### 2. **Iterate for Better Results**
Like humans, Claude's outputs tend to improve significantly with iteration. While the first version might be good, after 2-3 iterations it will typically look much better.

### 3. **Use Markdown Checklists for Complex Tasks**
For large tasks with multiple steps or requiring exhaustive solutions—like code migrations, fixing numerous lint errors, or running complex build scripts—improve performance by having Claude use a Markdown file (or even a GitHub issue!) as a checklist and working scratchpad.

### 4. **Store Reusable Commands**
For repeated workflows—debugging loops, log analysis, etc.—store prompt templates in Markdown files within the .claude/commands folder. These become available through the slash commands menu when you type /.

## Pricing & Plans

### Claude Pro Plan ($20/month)
- Best for: Light work on small repositories (typically under 1,000 lines of code)
- Shared usage limits with Claude web interface

### Claude Max Plans ($100-200/month)  
- **Max 5x Pro ($100/month)**: ~50-200 Claude Code prompts every 5 hours
- **Max 20x Pro ($200/month)**: ~200-800 Claude Code prompts every 5 hours
- Best for: Everyday use with larger codebases, or power users
- Access to both Sonnet 4 and Opus 4 models

### API Console (Pay-per-use)
- When used with an Anthropic Console account, Claude Code consumes API tokens at standard API pricing

## System Requirements

Claude Code works on macOS, Linux, and Windows. Specific requirements:
- **macOS**: 10.15+
- **Ubuntu**: 20.04+/Debian 10+  
- **Windows**: 10+ (with WSL 1, WSL 2, or Git for Windows)

## Quick Example Workflows

### 1. Build a Feature
```bash
claude
> "Build a user registration API endpoint with email validation and password hashing"
```

### 2. Debug an Issue  
```bash
claude
> "I'm getting a 500 error when users try to login. Here's the error: [paste error]"
```

### 3. Code Review
```bash
claude
> "Review this pull request and suggest improvements for security and performance"
```

### 4. Fix All Lint Issues
```bash
claude
> "Fix all ESLint errors in this project and explain what you changed"
```

## Getting Help

```bash
# Built-in help
claude --help

# Version info
claude --version

# Check installation
claude doctor

# Report bugs from within Claude Code
/bug
```

## Next Steps

1. **Start Simple**: Try basic tasks like explaining code or fixing lint errors
2. **Experiment with Models**: Switch between Sonnet 4 and Opus 4 to see differences
3. **Learn Slash Commands**: Master the interactive commands for better workflows  
4. **Set Up Custom Commands**: Create reusable prompts in `.claude/commands/`
5. **Integrate with Your Workflow**: Use Claude Code with your existing Git, CI/CD, and development tools

Claude Code is designed to integrate seamlessly into your existing development workflow, making it a powerful addition to your coding toolkit! 🚀