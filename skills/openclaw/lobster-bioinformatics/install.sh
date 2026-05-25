#!/bin/bash
# Install Lobster AI Claude Code Skill
# Usage: curl -fsSL https://raw.githubusercontent.com/the-omics-os/lobster-local/main/claude-skill/install.sh | bash

set -e

echo "🦞 Installing Lobster AI Skill for Claude Code..."
echo ""

# Check if Claude Code skills directory exists
SKILLS_DIR="$HOME/.claude/skills/lobster"

# Create skills directory
mkdir -p "$SKILLS_DIR"

# Download SKILL.md
echo "📥 Downloading Skill definition..."
curl -fsSL https://raw.githubusercontent.com/the-omics-os/lobster-local/main/claude-skill/SKILL.md \
  -o "$SKILLS_DIR/SKILL.md"

# Verify installation
if [ -f "$SKILLS_DIR/SKILL.md" ]; then
  echo "✅ Skill installed successfully!"
  echo ""
  echo "📍 Location: $SKILLS_DIR/SKILL.md"
  echo ""

  # Check if lobster is installed
  if command -v lobster &> /dev/null; then
    echo "✅ Lobster AI is already installed"
    echo ""
    echo "🚀 You're ready to go! Start Claude Code and try:"
    echo "   $ claude"
    echo "   You: 'Analyze my single-cell dataset'"
  else
    echo "⚠️  Lobster AI is not installed"
    echo ""
    echo "Install Lobster AI:"
    echo "   $ uv tool install lobster-ai"
    echo "   $ lobster init"
    echo ""
    echo "Then start Claude Code:"
    echo "   $ claude"
  fi
else
  echo "❌ Installation failed"
  exit 1
fi
