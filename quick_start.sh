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

# Step 2: Install dependencies
echo "📦 Step 1: Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "💡 Try: pip3 install --user -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Step 3: Verify system
echo "🔍 Step 2: Verifying system..."
python3 verify_system.py

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
echo "   Place images in: test_images/1/, test_images/2/, test_images/3/, test_images/4/"
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
