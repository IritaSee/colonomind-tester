"""
Test Dataset Manager for ColonoMind automated testing.
Handles loading images from folder structure where each folder represents a MES class.
"""
import os
from pathlib import Path
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class TestDatasetManager:
    """Manages test images organized by MES class in folder structure."""
    
    def __init__(self, base_dir: str, supported_extensions: List[str] = None):
        """
        Initialize dataset manager.
        
        Args:
            base_dir: Base directory containing class folders (e.g., ./test_images)
            supported_extensions: List of supported image extensions
        """
        self.base_dir = Path(base_dir)
        self.supported_extensions = supported_extensions or ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
        self.images = []
        self.total_count = 0
        
    def load_dataset(self) -> List[Tuple[str, int]]:
        """
        Load images from folder structure.
        Expected structure:
            test_images/
            ├── 1/  (MES class 1)
            │   ├── image1.jpg
            │   └── image2.jpg
            ├── 2/  (MES class 2)
            ├── 3/  (MES class 3)
            └── 4/  (MES class 4)
        
        Returns:
            List of tuples (image_path, ground_truth_class)
        """
        if not self.base_dir.exists():
            raise ValueError(f"Dataset directory does not exist: {self.base_dir}")
        
        self.images = []
        
        # Look for subdirectories named MES 0, MES 1, MES 2, MES 3
        for class_label in [0, 1, 2, 3]:
            # Try both "MES X" and just "X" to be flexible, but prioritize "MES X" as requested
            possible_names = [f"MES {class_label}", f"MES{class_label}", str(class_label)]
            
            class_dir = None
            for name in possible_names:
                temp_dir = self.base_dir / name
                if temp_dir.exists():
                    class_dir = temp_dir
                    break
            
            if not class_dir:
                logger.warning(f"Class directory not found for MES {class_label} (checked: {possible_names})")
                continue
            
            # Find all images in this class directory
            for img_path in class_dir.iterdir():
                if img_path.is_file() and img_path.suffix in self.supported_extensions:
                    self.images.append((str(img_path.absolute()), class_label))
        
        self.total_count = len(self.images)
        logger.info(f"Loaded {self.total_count} images from {self.base_dir}")
        
        return self.images
    
    def get_class_distribution(self) -> Dict[int, int]:
        """Get count of images per class."""
        distribution = {0: 0, 1: 0, 2: 0, 3: 0}
        for _, class_label in self.images:
            if class_label in distribution:
                distribution[class_label] += 1
        return distribution
    
    def get_batches(self, batch_size: int) -> List[List[Tuple[str, int]]]:
        """
        Split dataset into batches.
        
        Args:
            batch_size: Number of images per batch
            
        Returns:
            List of batches, each batch is a list of (image_path, ground_truth)
        """
        batches = []
        for i in range(0, len(self.images), batch_size):
            batches.append(self.images[i:i + batch_size])
        return batches
    
    def validate_dataset(self) -> bool:
        """Validate that all image files exist and are accessible."""
        all_valid = True
        for img_path, _ in self.images:
            if not os.path.exists(img_path):
                logger.error(f"Image file not found: {img_path}")
                all_valid = False
        return all_valid
