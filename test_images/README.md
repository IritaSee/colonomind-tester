# Sample Test Dataset Structure

This directory should contain your colonoscopy images organized by MES classification.

## Expected Structure

```
test_images/
├── MES 0/      # MES class 0 (Normal)
│   ├── image1.jpg
│   └── ...
├── MES 1/      # MES class 1 (Mild)
│   ├── image1.jpg
│   └── ...
├── MES 2/      # MES class 2 (Moderate)
│   └── ...
└── MES 3/      # MES class 3 (Severe)
    └── ...
```

## Instructions

1. Place your colonoscopy images in the appropriate MES class folder
2. Supported formats: `.jpg`, `.jpeg`, `.png` (case-insensitive)
3. You can have as many images as needed in each folder
4. Folder names should be: `MES 0`, `MES 1`, `MES 2`, `MES 3`

## Example

If you have 250 images per class (1000 total):
- Folder `MES 0/`: 250 images of MES class 0
- Folder `MES 1/`: 250 images of MES class 1
- Folder `MES 2/`: 250 images of MES class 2
- Folder `MES 3/`: 250 images of MES class 3

The testing system will automatically:
- Load all images
- Track ground truth based on folder name
- Compare predictions against ground truth
- Calculate accuracy per class
