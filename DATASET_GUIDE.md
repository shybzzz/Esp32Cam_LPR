# Dataset Requirements for License Plate Recognition

## Overview
To train an effective license plate recognition model for ESP32-CAM, you'll need a well-curated dataset.

## Dataset Size Recommendations

### Minimum (Quick Prototype)
- **200-300 images** per class
- **2 classes**: `license_plate` and `no_license_plate`
- **Total**: 400-600 images

### Recommended (Good Performance)
- **500-1000 images** per class
- **Total**: 1000-2000 images
- Better generalization and accuracy

### Ideal (Production Quality)
- **2000-5000 images** per class
- **Total**: 4000-10000 images
- Include diverse conditions and edge cases

## Image Requirements

### Technical Specifications
- **Format**: JPG, PNG
- **Resolution**: Minimum 320x240 (will be resized to 96x96)
- **Color**: RGB or Grayscale (grayscale preferred for ESP32)
- **File Size**: < 500KB per image

### Content Diversity

#### License Plates (Positive Class)
Include variety in:
- **Distance**: Close-up to 10 meters away
- **Angles**: Front view, slight angles (±30°)
- **Lighting**:
  - Daylight (morning, noon, afternoon)
  - Overcast/cloudy
  - Night with headlights
  - Indoor/garage lighting
- **Plate Types**:
  - Different countries/regions (if applicable)
  - Standard and specialty plates
  - Clean and dirty plates
  - New and weathered plates
- **Backgrounds**:
  - Parking lots
  - Streets
  - Highways
  - Residential areas

#### No License Plate (Negative Class)
Include:
- **Vehicles without plates visible**:
  - Side views
  - Rear views without plates
  - Distant vehicles
- **Similar rectangular objects**:
  - Signs and billboards
  - Windows
  - Building facades
- **Empty scenes**:
  - Roads without vehicles
  - Parking spots
  - Traffic scenes

## Data Collection Methods

### 1. Use Public Datasets
Download and combine existing datasets:

```python
# Example sources:
# - Kaggle: https://www.kaggle.com/datasets/andrewmvd/car-plate-detection
# - Roboflow: https://universe.roboflow.com/
# - GitHub repositories with CC/MIT licenses
```

### 2. Capture Your Own
Use ESP32-CAM or smartphone:

```cpp
// ESP32-CAM data collection sketch
// Save images to SD card with timestamps
// Organize later into training/testing folders
```

### 3. Web Scraping (Legal Sources Only)
- Ensure compliance with terms of service
- Respect copyright and privacy laws
- Blur or anonymize actual plate numbers

## Data Organization Structure

```
dataset/
├── training/           # 80% of data
│   ├── license_plate/
│   │   ├── img_001.jpg
│   │   ├── img_002.jpg
│   │   └── ...
│   └── no_license_plate/
│       ├── img_001.jpg
│       ├── img_002.jpg
│       └── ...
└── testing/            # 20% of data
    ├── license_plate/
    │   └── ...
    └── no_license_plate/
        └── ...
```

## Labeling Guidelines

### For Detection Models
1. **Bounding Boxes**: Draw tight boxes around plates
2. **Class Labels**: "license_plate" or "vehicle_plate"
3. **Tools**: 
   - [LabelImg](https://github.com/tzutalin/labelImg)
   - [CVAT](https://cvat.org/)
   - [Roboflow](https://roboflow.com/)

### For Classification Models (Simpler)
1. Entire image labeled as class
2. Organize into folders by class name
3. No bounding boxes needed

## Data Augmentation

Apply during training to increase effective dataset size:

```python
# Example augmentation pipeline
augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.2),
])
```

### Recommended Augmentations
- **Rotation**: ±15 degrees
- **Brightness**: ±20%
- **Contrast**: ±20%
- **Zoom**: ±10%
- **Horizontal flip**: Only if plates are symmetric
- **Gaussian noise**: Simulate camera noise
- **Blur**: Simulate motion/focus blur

### Avoid
- **Vertical flip**: Plates have orientation
- **Extreme rotation**: Unrealistic angles
- **Color shifts**: If using grayscale

## Data Quality Checklist

- [ ] Images are clear and in focus
- [ ] License plates are visible (not too small)
- [ ] Variety of lighting conditions
- [ ] Balanced classes (similar number of images)
- [ ] No duplicate or near-duplicate images
- [ ] Test set is completely separate from training
- [ ] Privacy considerations addressed (blur plate numbers if needed)
- [ ] Proper file naming convention
- [ ] Metadata documented (camera, conditions, location)

## Privacy and Legal Considerations

### Important Notes
⚠️ **Privacy**: License plates can identify individuals
- Blur or randomize actual plate numbers
- Don't share datasets with identifiable information
- Comply with GDPR, CCPA, and local privacy laws

⚠️ **Usage Rights**: Only use images you have rights to
- Personal photos: OK
- Public datasets: Check license (CC, MIT, etc.)
- Web images: Usually NOT OK without permission
- Commercial use: Requires extra care

### Ethical Guidelines
1. Only collect data in public spaces (where legal)
2. Don't target specific individuals
3. Use data only for stated purpose
4. Implement data retention policies
5. Consider surveillance and privacy implications

## Download Ready-to-Use Datasets

### Free Public Datasets

1. **CCPD (Chinese City Parking Dataset)**
   - 250,000+ images
   - Various conditions
   - [GitHub](https://github.com/detectRecog/CCPD)

2. **Car License Plate Detection (Kaggle)**
   - ~400 annotated images
   - XML annotations
   - [Kaggle](https://www.kaggle.com/datasets/andrewmvd/car-plate-detection)

3. **OpenALPR Benchmark**
   - Multiple countries
   - Ground truth data
   - [GitHub](https://github.com/openalpr/benchmarks)

4. **Roboflow Public Datasets**
   - Pre-processed and augmented
   - Multiple formats
   - [Roboflow Universe](https://universe.roboflow.com/)

## Verification Before Training

Run this checklist:

```python
import os
from pathlib import Path

def verify_dataset(base_path):
    """Verify dataset structure and content"""
    
    classes = ['license_plate', 'no_license_plate']
    splits = ['training', 'testing']
    
    for split in splits:
        print(f"\n{split.upper()}:")
        for cls in classes:
            path = Path(base_path) / split / cls
            if path.exists():
                count = len(list(path.glob('*.jpg'))) + len(list(path.glob('*.png')))
                print(f"  {cls}: {count} images")
            else:
                print(f"  {cls}: MISSING!")
    
    # Check for balance
    # Recommend ratio between classes: 0.5 to 2.0

verify_dataset('dataset')
```

## Next Steps

After preparing your dataset:

1. **Organize** into training/testing splits (80/20)
2. **Upload** to Edge Impulse or use local training
3. **Train** your model with augmentation
4. **Validate** on test set
5. **Optimize** for ESP32-CAM
6. **Deploy** and test in real conditions

---

**Remember**: Quality > Quantity. 500 diverse, well-labeled images beat 5000 similar ones!
