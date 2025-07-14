#!/bin/bash

# Devcontainer Setup Script
# This script runs after the container is created to set up the development environment

set -e  # Exit on any error

echo "🚀 Starting devcontainer setup..."

# Update and upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# Set up SSH directory permissions (if SSH directory exists)
if [ -d /home/vscode/.ssh ]; then
    echo "🔐 Setting up SSH permissions..."
    chmod 700 /home/vscode/.ssh
    chmod 600 /home/vscode/.ssh/* 2>/dev/null || true
    echo "✅ SSH permissions configured"
else
    echo "ℹ️  No SSH directory found, skipping SSH setup"
fi

# Configure Git
git config pull.rebase true

echo "🔧 Configuring Git..."
current_name=$(git config --global user.name 2>/dev/null || echo "")
current_email=$(git config --global user.email 2>/dev/null || echo "")

if [ -z "$current_name" ]; then
    echo "📝 Git user.name is not set."
    read -p "Please enter your full name: " user_name
    if [ -n "$user_name" ]; then
        git config --global user.name "$user_name"
        echo "✅ Git user.name set to: $user_name"
    else
        echo "⚠️  No name provided, skipping user.name configuration"
    fi
else
    echo "✅ Git user.name already set: $current_name"
fi

if [ -z "$current_email" ]; then
    echo "📧 Git user.email is not set."
    read -p "Please enter your email address: " user_email
    if [ -n "$user_email" ]; then
        git config --global user.email "$user_email"
        echo "✅ Git user.email set to: $user_email"
    else
        echo "⚠️  No email provided, skipping user.email configuration"
    fi
else
    echo "✅ Git user.email already set: $current_email"
fi

# Create useful aliases
if [ -f /home/vscode/.zshrc ]; then
    if ! grep -q "# Python Development Aliases" /home/vscode/.zshrc; then
        cat >> /home/vscode/.zshrc << 'EOF'

# Python Development Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias pytest-cov='python -m pytest --cov=. --cov-report=html --cov-report=term'
alias run-tests='python -m pytest -v'
alias lint='flake8 . && pylint . && mypy .'
alias format='black . && isort .'

EOF
    else
        echo "ℹ️  Aliases already exist in .zshrc, skipping addition"
    fi
fi

echo "✅ Aliases added to shell configuration"

# Display Python and tool versions
echo "🔍 Installed versions:"
python --version
pip --version
echo "black: $(black --version)"
echo "flake8: $(flake8 --version)"

echo ""
echo "🎉 Devcontainer setup completed successfully!"
echo ""
echo "📝 Available aliases:"
echo "  - run-tests:   Run all tests"
echo "  - pytest-cov: Run tests with coverage report"
echo "  - lint:        Run all linters (flake8, pylint, mypy)"
echo "  - format:      Format code with black and isort"
echo ""
echo "🚀 Happy coding!"