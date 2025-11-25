#!/bin/bash
# Activation script for the UV virtual environment

echo "🚀 Activating ColonoMind Testing Environment..."
echo ""

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Run './setup.sh' to create it"
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "📦 Python: $(python --version)"
echo "📍 Location: $(which python)"
echo ""
echo "💡 To deactivate, run: deactivate"
echo ""
