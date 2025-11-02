# Model Resources & Pre-Trained Options

This document lists available resources, pre-trained models, and tools for ESP32-CAM license plate recognition.

## 🚀 Quick Model Options

### Option 1: Edge Impulse (Easiest) ⭐ RECOMMENDED

**What it is**: Web-based ML platform with automatic ESP32 optimization

**Pros**:
- No local ML setup needed
- Automatic model optimization
- Built-in data augmentation
- Direct Arduino library export
- Free for public projects

**Steps**:
1. Sign up at https://studio.edgeimpulse.com/
2. Create "Image Classification" or "Object Detection" project
3. Upload 200-500 labeled images
4. Train with MobileNetV2 0.1
5. Download as Arduino library
6. Extract to `lib/` folder

**Expected Model Size**: 150-250KB
**Expected Accuracy**: 85-95% (with good data)
**Training Time**: 20-40 minutes

**Tutorials**:
- [ESP32 Getting Started](https://docs.edgeimpulse.com/docs/development-platforms/officially-supported-mcu-targets/espressif-esp32)
- [Image Classification](https://docs.edgeimpulse.com/docs/edge-impulse-studio/learning-blocks/image-classification)
- [Object Detection (FOMO)](https://docs.edgeimpulse.com/docs/edge-impulse-studio/learning-blocks/object-detection)

---

### Option 2: TensorFlow Lite Model Maker

**What it is**: Google's tool for creating custom TFLite models with transfer learning

**Pros**:
- More control than Edge Impulse
- Well-documented
- Good pre-trained base models
- Free and open source

**Setup**:
```bash
pip install tflite-model-maker
```

**Example Script**:
```python
from tflite_model_maker import image_classifier
from tflite_model_maker.image_classifier import DataLoader

# Load data
data = DataLoader.from_folder('dataset/training')
train_data, test_data = data.split(0.8)

# Create model
model = image_classifier.create(
    train_data,
    model_spec='mobilenet_v2',
    validation_data=test_data,
    epochs=20
)

# Export to TFLite with quantization
model.export(export_dir='.', 
             tflite_filename='lpr_model.tflite',
             quantization_config='int8')
```

**Resources**:
- [Documentation](https://www.tensorflow.org/lite/models/modify/model_maker/image_classification)
- [Colab Tutorial](https://colab.research.google.com/github/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/models/modify/model_maker/image_classification.ipynb)

---

### Option 3: Pre-Trained Models (Fastest Start)

**Warning**: These are NOT trained on license plates, only for testing infrastructure!

#### MobileNetV2 (ImageNet)

```python
import tensorflow as tf

# Load MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(96, 96, 3),
    alpha=0.35,  # Width multiplier (0.35 = smallest)
    include_top=False,
    weights='imagenet'
)

# Add classification head
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(2, activation='softmax')
])

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

#### EfficientNet-Lite

```python
import tensorflow as tf

# Smallest EfficientNet variant
model = tf.keras.applications.EfficientNetB0(
    input_shape=(96, 96, 3),
    include_top=True,
    classes=2,
    weights=None  # Random weights, need training
)
```

---

## 📚 Public Datasets for Training

### License Plate Specific

1. **CCPD (Chinese City Parking Dataset)**
   - **Size**: 250,000+ images
   - **Link**: https://github.com/detectRecog/CCPD
   - **License**: Free for research
   - **Format**: Annotated with plate corners and characters
   - **Note**: Excellent for training, may need adaptation for other regions

2. **OpenALPR Benchmarks**
   - **Size**: Various datasets
   - **Link**: https://github.com/openalpr/benchmarks
   - **License**: Open source
   - **Regions**: USA, Europe
   - **Format**: Images with ground truth

3. **Kaggle: Car License Plate Detection**
   - **Size**: ~400 images
   - **Link**: https://www.kaggle.com/datasets/andrewmvd/car-plate-detection
   - **License**: CC BY 4.0
   - **Format**: XML annotations (Pascal VOC)

4. **Roboflow Universe**
   - **Size**: Multiple datasets, 100-10,000+ images each
   - **Link**: https://universe.roboflow.com/search?q=license%20plate
   - **License**: Various (check individual datasets)
   - **Format**: Pre-processed, multiple export formats
   - **Note**: Many datasets ready for training

### General Vehicle Datasets (Adaptable)

5. **Stanford Cars Dataset**
   - **Link**: http://ai.stanford.edu/~jkrause/cars/car_dataset.html
   - 16,185 images of cars
   - Can extract plate regions

6. **CompCars Dataset**
   - **Link**: http://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/
   - Comprehensive car dataset
   - Multiple viewpoints

---

## 🛠️ Model Conversion Tools

### TensorFlow to TFLite

```python
import tensorflow as tf

# Load your Keras model
model = tf.keras.models.load_model('my_model.h5')

# Convert with INT8 quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Representative dataset for quantization
def representative_data_gen():
    for _ in range(100):
        yield [np.random.rand(1, 96, 96, 1).astype(np.float32)]

converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()

# Save
with open('model_quantized.tflite', 'wb') as f:
    f.write(tflite_model)
```

### TFLite to C Array

**Method 1: xxd (Linux/Mac/Git Bash)**
```bash
xxd -i model.tflite > src/lpr_model.h
```

**Method 2: Online Converter**
- Visit: https://notisrac.github.io/FileToCArray/
- Upload .tflite file
- Download .h file

**Method 3: Python Script**
```python
def tflite_to_c_array(tflite_path, output_path):
    with open(tflite_path, 'rb') as f:
        data = f.read()
    
    with open(output_path, 'w') as f:
        f.write('#ifndef MODEL_H\n#define MODEL_H\n\n')
        f.write('const unsigned char lpr_model[] = {\n')
        
        for i in range(0, len(data), 12):
            chunk = data[i:i+12]
            hex_str = ', '.join([f'0x{b:02x}' for b in chunk])
            f.write(f'  {hex_str},\n')
        
        f.write('};\n\n')
        f.write(f'const unsigned int lpr_model_len = {len(data)};\n\n')
        f.write('#endif\n')

# Usage
tflite_to_c_array('model.tflite', 'src/lpr_model.h')
```

### ONNX to TFLite

```python
import onnx
from onnx_tf.backend import prepare
import tensorflow as tf

# Load ONNX model
onnx_model = onnx.load('model.onnx')
tf_rep = prepare(onnx_model)

# Export to TensorFlow
tf_rep.export_graph('tf_model')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_saved_model('tf_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

---

## 🔬 Model Testing & Validation

### Online TFLite Analyzer

**Netron**: Visualize model architecture
- https://netron.app/
- Upload .tflite file
- See layers, shapes, operations

### Local Testing

```python
import tensorflow as tf
import numpy as np

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

# Get input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input shape:", input_details[0]['shape'])
print("Input type:", input_details[0]['dtype'])
print("Output shape:", output_details[0]['shape'])

# Test inference
input_data = np.random.rand(1, 96, 96, 1).astype(np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])

print("Output:", output_data)
print("Model size:", os.path.getsize('model.tflite') / 1024, "KB")
```

---

## 📦 Pre-Built Solutions (GitHub)

### Repositories with ESP32 + ML

1. **TensorFlow Lite Micro Examples**
   - https://github.com/tensorflow/tflite-micro
   - Official TFLite Micro examples
   - Person detection, keyword spotting

2. **EloquentArduino Examples**
   - https://github.com/eloquentarduino/EloquentTinyML
   - ESP32-CAM specific examples
   - Easy-to-use wrappers

3. **ESP-WHO (Espressif)**
   - https://github.com/espressif/esp-who
   - Face detection/recognition on ESP32
   - Can be adapted for license plates

4. **ESP32-CAM Projects**
   - Search GitHub: "esp32-cam tensorflow"
   - Many object detection examples
   - Adapt for license plates

---

## 💡 Model Optimization Tips

### Reduce Model Size

1. **Quantization** (INT8):
   - Reduces size by ~4x
   - Minimal accuracy loss
   - Faster inference

2. **Pruning**:
   ```python
   import tensorflow_model_optimization as tfmot
   
   pruning_params = {
       'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
           initial_sparsity=0.0,
           final_sparsity=0.5,
           begin_step=0,
           end_step=1000
       )
   }
   
   model = tfmot.sparsity.keras.prune_low_magnitude(model, **pruning_params)
   ```

3. **Smaller Architecture**:
   - MobileNetV2 alpha=0.1 (not 1.0)
   - Fewer layers
   - Smaller dense layers

### Improve Inference Speed

1. **Lower Input Resolution**: 64x64 instead of 96x96
2. **Grayscale**: 1 channel instead of 3
3. **INT8 Operations**: Use quantized arithmetic
4. **Optimize Preprocessing**: Do on ESP32, not in model

---

## 🎯 Model Performance Benchmarks

### Target Specs for ESP32-CAM

| Metric | Target | Acceptable | Poor |
|--------|--------|------------|------|
| Model Size | < 200KB | < 300KB | > 500KB |
| Inference Time | < 200ms | < 500ms | > 1s |
| Accuracy | > 90% | > 80% | < 70% |
| False Positives | < 10% | < 20% | > 30% |
| RAM Usage | < 100KB | < 150KB | > 200KB |

### Example Model Comparison

| Architecture | Size | Accuracy | Inference | Notes |
|--------------|------|----------|-----------|-------|
| MobileNetV2 (α=0.1) | 180KB | 88% | 250ms | Best balance |
| MobileNetV2 (α=0.35) | 320KB | 92% | 420ms | Better accuracy |
| EfficientNet-Lite0 | 280KB | 90% | 380ms | Good alternative |
| Custom CNN | 150KB | 85% | 180ms | Fastest |

---

## 📖 Learning Resources

### Tutorials

1. **TensorFlow Lite for Microcontrollers**
   - https://www.tensorflow.org/lite/microcontrollers
   - Official documentation

2. **Edge Impulse ESP32 Tutorial**
   - https://docs.edgeimpulse.com/docs/development-platforms/officially-supported-mcu-targets/espressif-esp32
   - Step-by-step guide

3. **Eloquent Arduino Blog**
   - https://eloquentarduino.com/
   - ESP32-CAM + ML tutorials

### Courses

- **Coursera: TinyML**
  - https://www.coursera.org/specializations/tinyml
  - Harvard University

- **Edge Impulse University**
  - https://docs.edgeimpulse.com/docs/tutorials
  - Free video tutorials

### Books

- "TinyML" by Pete Warden & Daniel Situnayake
- "AI at the Edge" by Daniel Situnayake et al.

---

## 🔗 Useful Links

- **ESP32-CAM Documentation**: https://github.com/espressif/esp32-camera
- **PlatformIO ESP32**: https://docs.platformio.org/en/latest/platforms/espressif32.html
- **TFLite Model Zoo**: https://www.tensorflow.org/lite/models
- **ONNX Model Zoo**: https://github.com/onnx/models
- **Papers with Code**: https://paperswithcode.com/task/license-plate-recognition

---

## ⚖️ Legal & Ethical Considerations

### Dataset Usage
- Verify license allows your use case
- Commercial vs. research use
- Attribution requirements
- Redistribution restrictions

### Privacy
- License plates are personal data (GDPR, CCPA)
- Blur actual plate numbers in shared datasets
- Obtain consent if required
- Follow local surveillance laws

### Responsible AI
- Don't use for unauthorized surveillance
- Consider bias in training data
- Document model limitations
- Implement user privacy protections

---

**Need a specific model or dataset? Open an issue with requirements!**
