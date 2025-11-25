#!/bin/bash
# Quick start script for ColonoMind automated testing

echo "======================================================================"
echo "ColonoMind Automated Testing System - Quick Start"
echo "======================================================================"
echo ""

# Step 1: Check if we're in the right directory
if [ ! -f "run_tests.py" ]; then
    echo "❌ Error: Please run this script from the colonomind-tester directory"
    exit 1
fi

# Step 2: Create venv and install dependencies using UV
echo "📦 Step 1: Creating virtual environment and installing dependencies with UV..."
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install UV"
        exit 1
    fi
    echo "✅ UV installed successfully"
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate and install dependencies
echo "Installing dependencies..."
source .venv/bin/activate
uv pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Step 3: Verify system
echo "🔍 Step 2: Verifying system..."
python verify_system.py

if [ $? -ne 0 ]; then
    echo "⚠️  Some verification tests failed - please check above"
    echo "💡 You may still be able to run tests if core components passed"
fi

echo ""
echo "======================================================================"
echo "✅ Setup Complete!"
echo "======================================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Prepare your test dataset:"
echo "   Place images in: test_images/MES 0/, test_images/MES 1/, test_images/MES 2/, test_images/MES 3/"
echo ""
echo "2. Run a quick test (5 images):"
echo "   python3 run_tests.py --max-images 5"
echo ""
echo "3. Run full test (1000 images):"
echo "   python3 run_tests.py --headless --batch-size 100"
echo ""
echo "4. Check results in: ./results/"
echo ""
echo "======================================================================"
