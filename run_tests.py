"""
Main entry point for ColonoMind automated testing system.
Orchestrates the entire testing process from loading data to generating reports.
"""
import argparse
import logging
import sys
import time
from pathlib import Path
from tqdm import tqdm
import traceback

# Import our modules
from config import *
from test_dataset_manager import TestDatasetManager
from colonoscopy_tester import ColonoMindTester
from results_analyzer import ResultsAnalyzer


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('testing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Automated testing system for ColonoMind webapp'
    )
    
    parser.add_argument(
        '--images',
        type=str,
        default=TEST_IMAGES_DIR,
        help=f'Directory containing test images organized by MES class (default: {TEST_IMAGES_DIR})'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=OUTPUT_DIR,
        help=f'Output directory for results (default: {OUTPUT_DIR})'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no GUI)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=BATCH_SIZE,
        help=f'Number of images to process before saving intermediate results (default: {BATCH_SIZE})'
    )
    
    parser.add_argument(
        '--max-images',
        type=int,
        default=None,
        help='Maximum number of images to test (for quick testing)'
    )
    
    parser.add_argument(
        '--start-index',
        type=int,
        default=0,
        help='Start from this image index (for resuming tests)'
    )
    
    return parser.parse_args()


def run_tests(args):
    """
    Main testing function.
    
    Args:
        args: Parsed command-line arguments
    """
    logger.info("=" * 80)
    logger.info("ColonoMind Automated Testing System")
    logger.info("=" * 80)
    
    # Step 1: Load test dataset
    logger.info(f"\n[Step 1/5] Loading test dataset from: {args.images}")
    dataset_manager = TestDatasetManager(args.images, SUPPORTED_EXTENSIONS)
    
    try:
        images = dataset_manager.load_dataset()
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return False
    
    if not images:
        logger.error("No images found in dataset!")
        return False
    
    # Show class distribution
    class_dist = dataset_manager.get_class_distribution()
    logger.info("Class distribution:")
    for mes_class, count in class_dist.items():
        logger.info(f"  MES {mes_class}: {count} images")
    
    # Validate dataset
    logger.info("Validating dataset...")
    if not dataset_manager.validate_dataset():
        logger.error("Dataset validation failed!")
        return False
    
    # Apply limits if specified
    if args.start_index > 0:
        images = images[args.start_index:]
        logger.info(f"Starting from index {args.start_index}, {len(images)} images remaining")
    
    if args.max_images:
        images = images[:args.max_images]
        logger.info(f"Limited to {len(images)} images for testing")
    
    # Step 2: Initialize tester
    logger.info(f"\n[Step 2/5] Initializing browser automation...")
    tester = ColonoMindTester(WEBAPP_URL, headless=args.headless)
    
    try:
        tester.setup_driver()
        tester.navigate_to_webapp()
    except Exception as e:
        logger.error(f"Failed to initialize tester: {e}")
        traceback.print_exc()
        return False
    
    # Step 3: Initialize results analyzer
    logger.info(f"\n[Step 3/5] Setting up results tracking...")
    ensure_output_dir()
    analyzer = ResultsAnalyzer(args.output)
    
    # Step 4: Run tests
    logger.info(f"\n[Step 4/5] Running tests on {len(images)} images...")
    logger.info(f"Webapp URL: {WEBAPP_URL}")
    logger.info(f"Headless mode: {args.headless}")
    logger.info(f"Batch size: {args.batch_size}")
    logger.info("")
    
    failed_count = 0
    processed_count = 0
    
    # Create progress bar
    with tqdm(total=len(images), desc="Testing images", unit="img") as pbar:
        for idx, (image_path, ground_truth) in enumerate(images):
            pbar.set_description(f"Testing image {idx+1}/{len(images)}")
            
            try:
                # Test the image
                predicted, processing_time, success = tester.test_single_image(image_path)
                
                # Record result
                if success:
                    analyzer.add_result(
                        image_path=image_path,
                        ground_truth=ground_truth,
                        predicted=predicted,
                        processing_time=processing_time,
                        success=True
                    )
                    pbar.set_postfix({
                        'Last': f'GT:{ground_truth} Pred:{predicted}',
                        'Time': f'{processing_time:.1f}s',
                        'Failed': failed_count
                    })
                else:
                    failed_count += 1
                    analyzer.add_result(
                        image_path=image_path,
                        ground_truth=ground_truth,
                        predicted=None,
                        processing_time=processing_time,
                        success=False,
                        error_msg="Failed to process image"
                    )
                    pbar.set_postfix({'Failed': failed_count})
                    
                    # Save screenshot on error if enabled
                    if SAVE_SCREENSHOTS_ON_ERROR:
                        screenshot_path = Path(args.output) / f"error_{idx}_{Path(image_path).stem}.png"
                        tester.save_screenshot(str(screenshot_path))
                
                processed_count += 1
                
                # Reset for next image (reload page)
                if idx < len(images) - 1:  # Don't reset after last image
                    tester.reset_for_next_image()
                
                # Save intermediate results at batch intervals
                if (processed_count % args.batch_size == 0):
                    logger.info(f"\nSaving intermediate results after {processed_count} images...")
                    analyzer.save_detailed_results(f"results_intermediate_{processed_count}.csv")
                
            except KeyboardInterrupt:
                logger.warning("\nTest interrupted by user!")
                break
            except Exception as e:
                logger.error(f"Error processing {image_path}: {e}")
                traceback.print_exc()
                failed_count += 1
                analyzer.add_result(
                    image_path=image_path,
                    ground_truth=ground_truth,
                    predicted=None,
                    processing_time=0.0,
                    success=False,
                    error_msg=str(e)
                )
            
            pbar.update(1)
    
    # Step 5: Generate reports
    logger.info(f"\n[Step 5/5] Generating reports...")
    
    try:
        # Save detailed results
        detailed_path = analyzer.save_detailed_results(DETAILED_RESULTS_FILE)
        logger.info(f"✓ Detailed results: {detailed_path}")
        
        # Save summary
        summary_path = analyzer.save_summary(SUMMARY_FILE)
        logger.info(f"✓ Summary: {summary_path}")
        
        # Generate confusion matrix
        cm_path = analyzer.generate_confusion_matrix(CONFUSION_MATRIX_FILE)
        if cm_path:
            logger.info(f"✓ Confusion matrix: {cm_path}")
        
        # Generate report
        report_path = analyzer.generate_report(REPORT_FILE)
        logger.info(f"✓ Report: {report_path}")
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        traceback.print_exc()
    
    # Cleanup
    logger.info("\nCleaning up...")
    tester.cleanup()
    
    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("TESTING COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total images processed: {processed_count}")
    logger.info(f"Failed tests: {failed_count}")
    logger.info(f"Success rate: {((processed_count - failed_count) / processed_count * 100):.1f}%")
    logger.info(f"\nResults saved to: {args.output}")
    logger.info("=" * 80)
    
    return True


def main():
    """Main entry point."""
    args = parse_arguments()
    
    try:
        success = run_tests(args)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
