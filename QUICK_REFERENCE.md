# 🚀 ColonoMind Testing - Quick Reference

## ⚡ Quick Start

```bash
# 1. Activate environment
source activate.sh

# 2. Verify system
python verify_system.py

# 3. Run quick test
python run_tests.py --max-images 5

# 4. Run full test
python run_tests.py --headless --batch-size 100
```

## 📋 Common Commands

### Environment
```bash
source activate.sh              # Activate venv
deactivate                      # Deactivate venv
./setup.sh                      # Recreate environment
```

### Testing
```bash
python run_tests.py --max-images 5                    # Quick test (5 images)
python run_tests.py --max-images 50                   # Medium test (50 images)
python run_tests.py --headless                        # Full test (headless)
python run_tests.py --headless --batch-size 100       # Full test with batching
python run_tests.py --start-index 500                 # Resume from image 500
```

### Verification
```bash
python verify_system.py         # Check system health
uv pip list                     # List installed packages
python --version                # Check Python version
```

## 📁 File Structure

```
test_images/
├── MES 0/    # Normal (354 images)
├── MES 1/    # Mild (209 images)
├── MES 2/    # Moderate (201 images)
└── MES 3/    # Severe (233 images)
```

## 📊 Output Files

After running tests, check `results/`:
- `results_detailed.csv` - Per-image results
- `results_summary.json` - Aggregated stats
- `confusion_matrix.png` - Visual matrix
- `REPORT.md` - Human-readable report
- `testing.log` - Detailed logs

## 🔧 Troubleshooting

```bash
# Environment issues
./setup.sh                      # Recreate environment

# Import errors
source activate.sh              # Make sure venv is active

# Dependency issues
uv pip install -r requirements.txt

# Check system
python verify_system.py
```

## 💡 Tips

1. **Always activate** environment before running tests
2. **Use --headless** for long runs (saves resources)
3. **Use --batch-size** to save progress frequently
4. **Check testing.log** for detailed error information
5. **Review confusion_matrix.png** to understand errors

## 📖 Full Documentation

- `README.md` - Complete user guide
- `UV_VENV.md` - UV environment details
- `SETUP_COMPLETE.md` - Setup summary

## ✅ System Status

- Python: 3.13.4
- Package Manager: UV
- Total Images: 997
- Status: ✅ OPERATIONAL
