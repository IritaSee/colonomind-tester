# ColonoMind Automated Testing System

Automated testing system for the ColonoMind webapp using Python and Selenium. Tests colonoscopy image classification for MES scoring (0-3) with performance and accuracy metrics.

**Built with UV** - Fast, reliable Python package management (10-100x faster than pip)

## 🎯 Features

- **Automated Browser Testing**: Selenium-based automation for Streamlit webapp
- **Batch Processing**: Process 1000+ images with batch saving
- **Performance Metrics**: Measure upload and processing times
- **Accuracy Analysis**: Calculate overall and per-class accuracy
- **Comprehensive Reports**: CSV results, JSON summary, confusion matrix, and markdown report
- **Resume Capability**: Resume testing from any point with `--start-index`
- **Error Handling**: Retry logic and screenshot capture on failures

## 📋 Requirements

- Python 3.8+
- Google Chrome browser
- Internet connection to access the webapp

## 🚀 Installation

This project uses **UV** for fast and reliable Python dependency management.

### Quick Setup (Recommended)

```bash
# Run the automated setup script
./setup.sh
```

This will:
- Check if UV is installed (install if needed)
- Create a virtual environment (`.venv/`)
- Install all dependencies
- Verify the system is ready

### Manual Setup

#### 1. Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Create Virtual Environment

```bash
uv venv
```

#### 3. Activate Environment

```bash
source .venv/bin/activate
# or use the helper script
source activate.sh
```

#### 4. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### What Gets Installed

- `selenium` - Browser automation
- `webdriver-manager` - Automatic ChromeDriver management
- `pandas` - Data manipulation
- `matplotlib` & `seaborn` - Visualization
- `scikit-learn` - Accuracy metrics
- `tqdm` - Progress bars

### Why UV?

✅ **10-100x faster** than pip  
✅ **Reliable** dependency resolution  
✅ **Compatible** with pip and requirements.txt  
✅ **No configuration** needed - drop-in replacement

### Environment Management

```bash
# Activate environment
source activate.sh

# Deactivate environment
deactivate

# Verify installation
python verify_system.py

# Check Python version
python --version
```

## 📂 Preparing Test Dataset

The system expects images organized by MES class in folders:

```
test_images/
├── MES 0/      # MES class 0 (Normal)
│   ├── image1.jpg
│   └── ...
├── MES 1/      # MES class 1 (Mild)
├── MES 2/      # MES class 2 (Moderate)
└── MES 3/      # MES class 3 (Severe)
```

**Folder names should be:** `MES 0`, `MES 1`, `MES 2`, `MES 3` (or just `0`, `1`, `2`, `3`)

**Supported formats:** `.jpg`, `.jpeg`, `.png` (case-insensitive)

## 🏃 Running Tests

### Basic Usage

Test all images in the default directory:
```bash
python run_tests.py
```

### With Custom Image Directory

```bash
python run_tests.py --images /path/to/your/test_images
```

### Quick Test (Limited Images)

Test only first 10 images:
```bash
python run_tests.py --max-images 10
```

### Headless Mode (No Browser Window)

Run without showing browser:
```bash
python run_tests.py --headless
```

### Custom Output Directory

```bash
python run_tests.py --output ./my_results
```

### Resume Testing

If testing was interrupted, resume from image 500:
```bash
python run_tests.py --start-index 500
```

### Full Example

```bash
python run_tests.py \
  --images ./test_images \
  --output ./results \
  --headless \
  --batch-size 100 \
  --max-images 1000
```

## 📊 Output Files

After running tests, you'll find in the output directory:

### 1. `results_detailed.csv`
Detailed results for each image:
- Image path and name
- Ground truth MES score
- Predicted MES score
- Processing time
- Success/failure status
- Error messages (if any)

### 2. `results_summary.json`
JSON file with:
- Overall accuracy
- Per-class accuracy
- Timing statistics (mean, median, min, max)
- Class distribution
- Success/failure counts

### 3. `confusion_matrix.png`
Visual confusion matrix showing prediction patterns

### 4. `REPORT.md`
Human-readable markdown report with:
- Overview statistics
- Accuracy metrics table
- Performance metrics
- Time estimates for 1000 images

### 5. `testing.log`
Detailed log of all operations

### 6. Intermediate Results (during long runs)
`results_intermediate_100.csv`, `results_intermediate_200.csv`, etc.

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Webapp URL default:
WEBAPP_URL = "https://colonomind-335955344592.asia-southeast1.run.app/"

# Timeouts default:
UPLOAD_TIMEOUT = 15  # seconds
PROCESSING_TIMEOUT = 60  # seconds

# Batch size for intermediate saves
BATCH_SIZE = 100

# Browser settings
HEADLESS_MODE = False
```

## 📁 Project Structure

```
colonomind-tester/
├── .venv/                       # UV virtual environment (gitignored)
├── tools/                       # Core modules
│   ├── __init__.py
│   ├── colonoscopy_tester.py    # Selenium automation
│   ├── test_dataset_manager.py  # Dataset loading
│   └── results_analyzer.py      # Results analysis
├── test_images/                 # Test dataset
│   ├── MES 0/                   # MES class 0 images
│   ├── MES 1/                   # MES class 1 images
│   ├── MES 2/                   # MES class 2 images
│   └── MES 3/                   # MES class 3 images
├── results/                     # Test results (gitignored)
├── config.py                    # Configuration settings
├── run_tests.py                 # Main entry point
├── verify_system.py             # System verification
├── setup.sh                     # Automated setup script
├── activate.sh                  # Quick activation helper
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── QUICK_REFERENCE.md           # Quick command reference
```

## 🔍 Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--images` | Directory with test images | `./test_images` |
| `--output` | Output directory for results | `./results` |
| `--headless` | Run browser in background | `False` |
| `--batch-size` | Images per batch save | `100` |
| `--max-images` | Limit number of images | `None` (all) |
| `--start-index` | Resume from this image | `0` |

## 🐛 Troubleshooting

### ChromeDriver Issues
The system auto-downloads ChromeDriver. If you encounter issues:
1. Update Chrome to the latest version
2. Clear webdriver cache: `rm -rf ~/.wdm`
3. Reinstall: `pip install --upgrade webdriver-manager`

### Upload Failures
- Check internet connection
- Verify image file formats
- Increase `UPLOAD_TIMEOUT` in `config.py`

### Classification Not Detected
- Run in non-headless mode to see what's happening
- Check `error_*.png` screenshots in output directory
- Review `testing.log` for details

### Webapp Timeout
- Increase `PROCESSING_TIMEOUT` in `config.py`
- Check if webapp is accessible manually

### Virtual Environment Issues

**Environment not found:**
```bash
./setup.sh  # Recreate environment
```

**Dependencies out of sync:**
```bash
source activate.sh
uv pip install -r requirements.txt
```

**UV not installed:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Import errors:**
```bash
# Make sure environment is activated
source activate.sh
python verify_system.py
```

**Wrong Python version:**
```bash
# Check which Python is being used
which python
python --version
# Should show .venv/bin/python and Python 3.13+
```

## 📝 Example Workflow

### 1. Setup and Verify
```bash
# First time setup
./setup.sh

# Activate environment
source activate.sh

# Verify system
python verify_system.py
```

### 2. Small Test Run
First, verify everything works with a few images:
```bash
python run_tests.py --max-images 5
```

### 3. Review Results
Check the output:
```bash
cat results/REPORT.md
```

### 4. Full Test Run
Run the complete 1000-image test:
```bash
python run_tests.py --headless --batch-size 100
```

### 5. Monitor Progress
Watch the progress bar and logs:
```
Testing images: 45%|████▌     | 450/1000 [45:23<50:12, 5.48s/img] 
Last: GT:2 Pred:2, Time: 5.2s, Failed: 3
```

## 📈 Understanding Results

### Accuracy Metrics
- **Overall Accuracy**: Percentage of correct predictions
- **Per-Class Accuracy**: Accuracy for each MES class (1-4)

### Timing Statistics
- **Mean Time**: Average processing time per image
- **Total Time**: Estimated time for all 1000 images

### Confusion Matrix
Shows where the model makes mistakes:
- Diagonal = correct predictions
- Off-diagonal = misclassifications

## 🎓 Tips

1. **Start Small**: Test with 10-20 images first
2. **Use Headless for Large Runs**: Saves resources
3. **Monitor Logs**: Watch `testing.log` for issues
4. **Save Batches**: Use `--batch-size` to save progress
5. **Resume on Failure**: Use `--start-index` if interrupted

## 🤝 Support

For issues or questions:
1. Check `testing.log` for error details
2. Review error screenshots in output directory
3. Verify dataset structure matches expected format
4. Ensure webapp is accessible in browser manually

## 📄 License

This is an automated testing tool for internal use with the ColonoMind webapp.

---

**Built with:** Python 3, Selenium, Pandas, Matplotlib
