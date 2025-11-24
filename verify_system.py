"""
Quick test script to verify the ColonoMind testing system is working.
This tests the basic components without needing a full dataset.
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import config
        print("✓ config.py imported successfully")
        
        from tools import test_dataset_manager
        print("✓ test_dataset_manager.py imported successfully")
        
        from tools import colonoscopy_tester
        print("✓ colonoscopy_tester.py imported successfully")
        
        from tools import results_analyzer
        print("✓ results_analyzer.py imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration values."""
    print("\nTesting configuration...")
    try:
        from config import WEBAPP_URL, MES_CLASSES, OUTPUT_DIR
        
        print(f"  Webapp URL: {WEBAPP_URL}")
        print(f"  MES Classes: {MES_CLASSES}")
        print(f"  Output Dir: {OUTPUT_DIR}")
        
        assert WEBAPP_URL.startswith("https://"), "Invalid webapp URL"
        assert MES_CLASSES == [0, 1, 2, 3], "Invalid MES classes"
        
        print("✓ Configuration is valid")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_dataset_manager():
    """Test dataset manager initialization."""
    print("\nTesting dataset manager...")
    try:
        from tools.test_dataset_manager import TestDatasetManager
        
        manager = TestDatasetManager("./test_images")
        print(f"✓ Dataset manager initialized")
        print(f"  Base directory: {manager.base_dir}")
        print(f"  Supported extensions: {manager.supported_extensions}")
        
        # Test if test_images directory exists
        if manager.base_dir.exists():
            print(f"✓ Test images directory exists")
            
            # Try to load dataset (will be empty initially)
            images = manager.load_dataset()
            print(f"  Found {len(images)} images")
            
            if len(images) == 0:
                print("  ⚠ No images in dataset (expected for fresh install)")
        else:
            print(f"✗ Test images directory not found: {manager.base_dir}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Dataset manager error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_results_analyzer():
    """Test results analyzer."""
    print("\nTesting results analyzer...")
    try:
        from tools.results_analyzer import ResultsAnalyzer
        
        analyzer = ResultsAnalyzer("./test_results")
        print(f"✓ Results analyzer initialized")
        
        # Add a dummy result
        analyzer.add_result(
            image_path="test.jpg",
            ground_truth=2,
            predicted=2,
            processing_time=5.0,
            success=True
        )
        
        # Test metrics calculation
        metrics = analyzer.calculate_accuracy_metrics()
        print(f"✓ Accuracy metrics calculated: {metrics['overall_accuracy']*100:.1f}%")
        
        timing = analyzer.calculate_timing_statistics()
        print(f"✓ Timing statistics calculated: {timing['mean_time']:.1f}s mean")
        
        return True
    except Exception as e:
        print(f"✗ Results analyzer error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test that all required dependencies are installed."""
    print("\nTesting dependencies...")
    required = [
        'selenium',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'tqdm',
        'webdriver_manager'
    ]
    
    all_ok = True
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            all_ok = False
    
    if not all_ok:
        print("\n⚠ Some dependencies are missing. Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True

def main():
    """Run all tests."""
    print("=" * 70)
    print("ColonoMind Testing System - Verification Script")
    print("=" * 70)
    
    results = []
    
    # Run tests
    results.append(("Dependencies", test_dependencies()))
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Dataset Manager", test_dataset_manager()))
    results.append(("Results Analyzer", test_results_analyzer()))
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - System is ready to use!")
        print("\nNext steps:")
        print("1. Place your test images in test_images/{1,2,3,4}/ folders")
        print("2. Run: python run_tests.py --max-images 5")
        print("3. Once verified, run full tests: python run_tests.py")
    else:
        print("✗ SOME TESTS FAILED - Please fix errors above")
        print("\nTroubleshooting:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check that all files are in place")
    print("=" * 70)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
