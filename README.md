# ESP32-CAM License Plate Recognition

A complete PlatformIO project for on-device license plate recognition using ESP32-CAM with TensorFlow Lite for Microcontrollers.

## 🎯 Features

- **Fully On-Device Inference**: Runs entirely on ESP32-CAM (no cloud/server needed)
- **Lightweight Model**: Optimized for ESP32's limited resources (520KB SRAM, 4MB Flash)
- **Real-time Processing**: Captures and processes images continuously
- **PlatformIO Support**: Easy build and deployment
- **Two Integration Options**: Edge Impulse or custom TensorFlow Lite models

## 📋 Hardware Requirements

- **ESP32-CAM** (AI-Thinker or compatible)
- **FTDI Programmer** or USB-to-Serial adapter (for initial upload)
- **Power Supply**: 5V, 2A recommended (ESP32-CAM can draw significant current)

## 🔧 Software Requirements

- [PlatformIO IDE](https://platformio.org/) (VS Code extension or CLI)
- Python 3.7+ (for model training scripts)
- TensorFlow 2.x (if training custom models)

## 🚀 Quick Start

### 1. Clone and Open Project

```bash
cd "d:\Sandbox\ESP ML\Esp32Cam_LPR"
```

### 2. Choose Your Approach

#### **Option A: Edge Impulse (Recommended for Beginners)**

Edge Impulse provides the easiest path with web-based training and automatic ESP32 optimization.

1. **Prepare Data Collection Structure**:
   ```bash
   python model_training/edge_impulse_setup.py
   ```

2. **Collect License Plate Images**:
   - Add images to `edge_impulse_data/training/license_plate/`
   - Add non-plate images to `edge_impulse_data/training/no_plate/`
   - Aim for 500+ images per class

3. **Train on Edge Impulse**:
   - Go to [Edge Impulse Studio](https://studio.edgeimpulse.com/)
   - Create new project
   - Upload your images
   - Configure impulse:
     - Image size: **96x96 grayscale**
     - Processing: **Image**
     - Learning: **Transfer Learning (MobileNetV2 0.1)**
   - Train the model
   - Deploy as **Arduino library**

4. **Integrate the Model**:
   - Extract the downloaded .zip to `lib/` folder
   - Rename `src/main_edge_impulse.cpp.example` to `src/main.cpp`
   - Update the include statement with your project name
   - Build and upload!

#### **Option B: Custom TensorFlow Lite Model**

For advanced users who want full control over model architecture.

1. **Train Your Model**:
   ```bash
   cd model_training
   pip install tensorflow numpy pillow
   python train_model.py
   ```

2. **Prepare Your Dataset**:
   - Collect and label license plate images
   - Train the model (see script for details)
   - Convert to TFLite with INT8 quantization
   - Generate C header file

3. **Replace Model File**:
   - Copy your `lpr_model.h` to `src/`
   - The existing `src/main.cpp` is ready to use
   - Adjust `INPUT_WIDTH` and `INPUT_HEIGHT` if needed

### 3. Build and Upload

```bash
# Build the project
pio run

# Upload to ESP32-CAM
pio run --target upload

# Monitor serial output
pio device monitor
```

**Note**: For first upload, you may need to:
1. Connect GPIO0 to GND
2. Press reset button
3. Upload firmware
4. Disconnect GPIO0 from GND
5. Press reset again

## 📁 Project Structure

```
Esp32Cam_LPR/
├── platformio.ini              # PlatformIO configuration
├── src/
│   ├── main.cpp                # Main application (TFLite version)
│   ├── main_edge_impulse.cpp.example  # Edge Impulse version
│   └── lpr_model.h             # Your trained model (placeholder)
├── model_training/
│   ├── train_model.py          # TensorFlow model training script
│   └── edge_impulse_setup.py   # Edge Impulse helper script
└── README.md                   # This file
```

## 🧠 Model Requirements

Due to ESP32-CAM's hardware constraints, your model must be:

- **Model Size**: < 300KB (ideally < 200KB)
- **Tensor Arena**: < 100KB RAM
- **Input Resolution**: 96x96 or 128x128 pixels
- **Quantization**: INT8 for best performance
- **Architecture**: MobileNetV2, EfficientNet-Lite, or similar

## 🎓 Training Your Own Model

### Recommended Dataset Sources

1. **Public Datasets**:
   - [Kaggle License Plate Datasets](https://www.kaggle.com/datasets) - Search "license plate"
   - [Roboflow Universe](https://universe.roboflow.com/) - Pre-labeled datasets
   - [CCPD Dataset](https://github.com/detectRecog/CCPD) - Chinese license plates
   - [OpenALPR Dataset](https://github.com/openalpr/benchmarks)

2. **Create Your Own**:
   - Capture 500-1000 images with ESP32-CAM
   - Include various angles, lighting conditions, distances
   - Label using tools like [LabelImg](https://github.com/tzutalin/labelImg) or [CVAT](https://cvat.org/)

### Training Tips

1. **Data Augmentation**: Essential for small datasets
   - Rotation (±15°)
   - Brightness/contrast variation
   - Random crops and flips
   - Blur and noise

2. **Transfer Learning**: Start with pre-trained MobileNetV2
   - Freeze early layers
   - Fine-tune on license plate data
   - Much faster than training from scratch

3. **Model Optimization**:
   - Use post-training quantization
   - Prune unnecessary layers
   - Verify model size before deploying

## 🔍 Expected Performance

- **Inference Time**: 100-500ms per image (depends on model complexity)
- **Detection Accuracy**: 80-95% (with good training data)
- **Power Consumption**: ~200-300mA during inference
- **Frame Rate**: ~2-5 FPS

## 📊 Serial Output Example

```
ESP32-CAM License Plate Recognition
====================================
Camera initialized successfully!
Model loaded successfully!
Model input size: 9216 bytes
Model output size: 8 bytes

Image captured!
Image size: 320x240
Running inference...

=== Detection Results ===
Inference time: 234 ms
Confidence: 87.3%
License plate detected!
========================
```

## ⚙️ Configuration Options

Edit `src/main.cpp` to customize:

```cpp
// Model input size
#define INPUT_WIDTH 96
#define INPUT_HEIGHT 96

// Tensor arena size
#define TENSOR_ARENA_SIZE 60*1024

// Detection threshold
if (output[0] > 0.5) {  // Adjust confidence threshold
    // License plate detected
}

// Capture interval
delay(2000);  // Wait 2 seconds between captures
```

## 🐛 Troubleshooting

### Camera Fails to Initialize
- Check power supply (needs 5V, 2A)
- Verify camera ribbon cable connection
- Try disabling brownout detector in code

### Model Inference Fails
- Verify model size < 300KB
- Check tensor arena size is sufficient
- Ensure model input dimensions match preprocessing

### Out of Memory Errors
- Reduce `TENSOR_ARENA_SIZE`
- Use smaller input resolution
- Apply more aggressive INT8 quantization
- Switch to QVGA (320x240) or lower camera resolution

### Low Detection Accuracy
- Collect more training data
- Improve data quality (better lighting, angles)
- Increase model complexity slightly
- Adjust detection threshold

## 📚 Resources

### Documentation
- [ESP32-CAM Datasheet](https://github.com/raphaelbs/esp32-cam-ai-thinker/blob/master/assets/ESP32-CAM_Product_Specification.pdf)
- [TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers)
- [Edge Impulse Documentation](https://docs.edgeimpulse.com/)
- [EloquentTinyML Library](https://github.com/eloquentarduino/EloquentTinyML)

### Example Projects
- [Edge Impulse ESP32 Examples](https://github.com/edgeimpulse/example-esp32)
- [TFLite Micro Examples](https://github.com/tensorflow/tflite-micro)

### Datasets
- [Kaggle: Car License Plate Detection](https://www.kaggle.com/datasets/andrewmvd/car-plate-detection)
- [Roboflow: License Plate Recognition](https://universe.roboflow.com/search?q=license%20plate)

## 🤝 Contributing

Improvements welcome! Consider contributing:
- Pre-trained model files (with license compliance)
- Training improvements
- Performance optimizations
- Additional documentation

## ⚖️ License

This project is provided as-is for educational purposes. Ensure you have proper rights to any training data and comply with local regulations regarding automated license plate recognition.

## 🙏 Acknowledgments

- TensorFlow Lite team for microcontroller support
- Edge Impulse for simplified ML deployment
- EloquentArduino for ESP32-CAM libraries
- Open source license plate detection community

## 📧 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Edge Impulse/TensorFlow documentation
3. Open an issue with detailed description and serial output

---

**Happy Coding! 🚗📸🤖**
