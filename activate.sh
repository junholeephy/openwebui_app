#!/bin/bash
# Activate virtual environment for Open WebUI project

echo "🚀 Activating Open WebUI virtual environment..."
source .venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated successfully!"
    echo "🐍 Python: $(which python)"
    echo "📦 Pip: $(which pip)"
    echo ""
    echo "💡 To deactivate, run: deactivate"
    echo "💡 To install packages: pip install <package_name>"
    echo "💡 To run scripts: python <script_name>"
else
    echo "❌ Failed to activate virtual environment"
    echo "💡 Make sure .venv directory exists and run: python3 -m venv .venv"
fi
