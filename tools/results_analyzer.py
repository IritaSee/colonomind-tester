"""
Results Analyzer for ColonoMind automated testing.
Calculates accuracy metrics, timing statistics, and generates reports.
"""
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Tuple
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import logging

logger = logging.getLogger(__name__)


class ResultsAnalyzer:
    """Analyzes test results and generates comprehensive reports."""
    
    def __init__(self, output_dir: str):
        """
        Initialize results analyzer.
        
        Args:
            output_dir: Directory to save results and reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        
    def add_result(self, image_path: str, ground_truth: int, predicted: int, 
                   processing_time: float, success: bool, error_msg: str = ""):
        """
        Add a test result.
        
        Args:
            image_path: Path to the tested image
            ground_truth: True MES classification
            predicted: Predicted MES classification (or None if failed)
            processing_time: Time taken to process in seconds
            success: Whether the test succeeded
            error_msg: Error message if test failed
        """
        self.results.append({
            'image_path': image_path,
            'image_name': Path(image_path).name,
            'ground_truth': ground_truth,
            'predicted': predicted,
            'processing_time': processing_time,
            'success': success,
            'correct': predicted == ground_truth if predicted is not None else False,
            'error': error_msg
        })
    
    def save_detailed_results(self, filename: str = "results_detailed.csv"):
        """Save detailed results to CSV file."""
        df = pd.DataFrame(self.results)
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Detailed results saved to {output_path}")
        return output_path
    
    def calculate_accuracy_metrics(self) -> Dict:
        """Calculate accuracy metrics."""
        # Filter successful predictions
        successful_results = [r for r in self.results if r['success'] and r['predicted'] is not None]
        
        if not successful_results:
            return {
                'overall_accuracy': 0.0,
                'total_tested': len(self.results),
                'successful_tests': 0,
                'failed_tests': len(self.results)
            }
        
        y_true = [r['ground_truth'] for r in successful_results]
        y_pred = [r['predicted'] for r in successful_results]
        
        overall_accuracy = accuracy_score(y_true, y_pred)
        
        # Per-class accuracy
        per_class_accuracy = {}
        for mes_class in [0, 1, 2, 3]:
            class_results = [r for r in successful_results if r['ground_truth'] == mes_class]
            if class_results:
                correct = sum(1 for r in class_results if r['correct'])
                per_class_accuracy[f'MES_{mes_class}_accuracy'] = correct / len(class_results)
            else:
                per_class_accuracy[f'MES_{mes_class}_accuracy'] = 0.0
        
        metrics = {
            'overall_accuracy': overall_accuracy,
            'total_tested': len(self.results),
            'successful_tests': len(successful_results),
            'failed_tests': len(self.results) - len(successful_results),
            **per_class_accuracy
        }
        
        return metrics
    
    def calculate_timing_statistics(self) -> Dict:
        """Calculate timing statistics."""
        successful_times = [r['processing_time'] for r in self.results if r['success']]
        
        if not successful_times:
            return {
                'mean_time': 0.0,
                'median_time': 0.0,
                'min_time': 0.0,
                'max_time': 0.0,
                'std_time': 0.0,
                'total_time': sum(r['processing_time'] for r in self.results)
            }
        
        return {
            'mean_time': np.mean(successful_times),
            'median_time': np.median(successful_times),
            'min_time': np.min(successful_times),
            'max_time': np.max(successful_times),
            'std_time': np.std(successful_times),
            'total_time': sum(r['processing_time'] for r in self.results)
        }
    
    def generate_confusion_matrix(self, filename: str = "confusion_matrix.png"):
        """Generate and save confusion matrix visualization."""
        successful_results = [r for r in self.results if r['success'] and r['predicted'] is not None]
        
        if not successful_results:
            logger.warning("No successful results to generate confusion matrix")
            return None
        
        y_true = [r['ground_truth'] for r in successful_results]
        y_pred = [r['predicted'] for r in successful_results]
        
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2, 3])
        
        # Create figure
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['MES 0', 'MES 1', 'MES 2', 'MES 3'],
                    yticklabels=['MES 0', 'MES 1', 'MES 2', 'MES 3'])
        plt.title('Confusion Matrix - ColonoMind MES Classification', fontsize=14, fontweight='bold')
        plt.ylabel('True MES Score', fontsize=12)
        plt.xlabel('Predicted MES Score', fontsize=12)
        plt.tight_layout()
        
        output_path = self.output_dir / filename
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Confusion matrix saved to {output_path}")
        return output_path
    
    def save_summary(self, filename: str = "results_summary.json"):
        """Save summary statistics to JSON file."""
        accuracy_metrics = self.calculate_accuracy_metrics()
        timing_stats = self.calculate_timing_statistics()
        
        # Class distribution
        class_distribution = {'ground_truth': {}, 'predicted': {}}
        for mes_class in [0, 1, 2, 3]:
            class_distribution['ground_truth'][f'MES_{mes_class}'] = sum(
                1 for r in self.results if r['ground_truth'] == mes_class
            )
            class_distribution['predicted'][f'MES_{mes_class}'] = sum(
                1 for r in self.results if r['predicted'] == mes_class
            )
        
        summary = {
            'accuracy_metrics': accuracy_metrics,
            'timing_statistics': timing_stats,
            'class_distribution': class_distribution
        }
        
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary saved to {output_path}")
        return output_path
    
    def generate_report(self, filename: str = "REPORT.md") -> Path:
        """Generate a human-readable markdown report."""
        accuracy_metrics = self.calculate_accuracy_metrics()
        timing_stats = self.calculate_timing_statistics()
        
        report_lines = [
            "# ColonoMind Automated Testing Report",
            "",
            "## Overview",
            "",
            f"- **Total Images Tested**: {accuracy_metrics['total_tested']}",
            f"- **Successful Tests**: {accuracy_metrics['successful_tests']}",
            f"- **Failed Tests**: {accuracy_metrics['failed_tests']}",
            f"- **Overall Accuracy**: {accuracy_metrics['overall_accuracy']*100:.2f}%",
            "",
            "## Accuracy Metrics",
            "",
            "### Per-Class Accuracy",
            "",
            "| MES Class | Accuracy |",
            "|-----------|----------|",
        ]
        
        for mes_class in [0, 1, 2, 3]:
            acc_key = f'MES_{mes_class}_accuracy'
            if acc_key in accuracy_metrics:
                acc_value = accuracy_metrics[acc_key] * 100
                report_lines.append(f"| MES {mes_class} | {acc_value:.2f}% |")
        
        report_lines.extend([
            "",
            "## Performance Metrics",
            "",
            f"- **Total Processing Time**: {timing_stats['total_time']:.2f} seconds ({timing_stats['total_time']/60:.2f} minutes)",
            f"- **Mean Processing Time per Image**: {timing_stats['mean_time']:.2f} seconds",
            f"- **Median Processing Time**: {timing_stats['median_time']:.2f} seconds",
            f"- **Min Processing Time**: {timing_stats['min_time']:.2f} seconds",
            f"- **Max Processing Time**: {timing_stats['max_time']:.2f} seconds",
            f"- **Standard Deviation**: {timing_stats['std_time']:.2f} seconds",
            "",
            "## Estimated Time for 1000 Images",
            "",
        ])
        
        if timing_stats['mean_time'] > 0:
            estimated_total = timing_stats['mean_time'] * 1000
            report_lines.append(f"Based on mean processing time: **{estimated_total:.2f} seconds** ({estimated_total/60:.2f} minutes, {estimated_total/3600:.2f} hours)")
        
        report_lines.extend([
            "",
            "## Files Generated",
            "",
            "- `results_detailed.csv`: Detailed results for each image",
            "- `results_summary.json`: Summary statistics in JSON format",
            "- `confusion_matrix.png`: Confusion matrix visualization",
            "- `REPORT.md`: This report",
            "",
            "---",
            "",
            f"*Report generated automatically by ColonoMind Automated Testing System*",
        ])
        
        report_content = "\n".join(report_lines)
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        logger.info(f"Report saved to {output_path}")
        return output_path
