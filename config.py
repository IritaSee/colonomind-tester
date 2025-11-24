"""
Configuration settings for ColonoMind automated testing system.
"""
import os
from pathlib import Path

# Webapp settings
WEBAPP_URL = "https://colonomind-335955344592.asia-southeast1.run.app/"

# Selenium WebDriver settings
HEADLESS_MODE = False  # Set to True to run browser in background
IMPLICIT_WAIT = 10  # seconds
PAGE_LOAD_TIMEOUT = 30  # seconds
SCRIPT_TIMEOUT = 30  # seconds

# Upload and processing timeouts
UPLOAD_TIMEOUT = 15  # seconds to wait for upload to complete
PROCESSING_TIMEOUT = 60  # seconds to wait for classification result
RESULT_CHECK_INTERVAL = 2  # seconds between checking for results

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Test dataset settings
TEST_IMAGES_DIR = "./test_images"  # Directory containing class folders
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']

# MES classification classes
MES_CLASSES = [0, 1, 2, 3]

# Output settings
OUTPUT_DIR = "./results"
DETAILED_RESULTS_FILE = "results_detailed.csv"
SUMMARY_FILE = "results_summary.json"
CONFUSION_MATRIX_FILE = "confusion_matrix.png"
REPORT_FILE = "REPORT.md"

# Batch processing
BATCH_SIZE = 100  # Process images in batches (save intermediate results)
SAVE_SCREENSHOTS_ON_ERROR = True  # Save screenshots when errors occur

# Paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_PATH = PROJECT_ROOT / OUTPUT_DIR

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
