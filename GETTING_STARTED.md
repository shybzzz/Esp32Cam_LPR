# 🚀 Getting Started - Choose Your Path

Welcome! This project provides a complete solution for license plate recognition on ESP32-CAM. Choose the path that fits your experience level.

---

## 📍 I'm New to This - Where Do I Start?

### Path for Beginners (Using Edge Impulse)

**Time Required**: ~4-6 hours total

#### Step 1: Setup (15 min)
```bash
# Open this project in VS Code with PlatformIO installed
# The project is already configured!
```

#### Step 2: Collect Data (1-3 hours)
- Take 200-500 photos of vehicles with license plates
- Take 200-500 photos without license plates (backgrounds, side views, etc.)
- Or download a dataset from: **[Kaggle](https://www.kaggle.com/datasets/andrewmvd/car-plate-detection)** or **[Roboflow](https://universe.roboflow.com/)**

#### Step 3: Train Model (30 min)
1. Go to **[Edge Impulse Studio](https://studio.edgeimpulse.com/)** (free account)
2. Create new project → Image Classification
3. Upload your images (Data Acquisition)
4. Create Impulse:
   - Image: 96x96 grayscale
   - Processing: Image
   - Learning: Transfer Learning (MobileNetV2 0.1)
5. Train (20 epochs)
6. Deploy → Arduino library → Download

#### Step 4: Integrate (15 min)
```bash
# Extract downloaded .zip to lib/ folder
# Rename src/main_edge_impulse.cpp.example to src/main.cpp
# Edit main.cpp and update the include line with your project name
```

#### Step 5: Upload to ESP32-CAM (15 min)
```bash
pio run --target upload
pio device monitor
```

**Done!** 🎉

📖 **Read**: [QUICK_START.md](QUICK_START.md) for detailed instructions

---

## 🔧 I Know ML - I Want Custom Control

### Path for ML Practitioners

**Time Required**: 2-8 hours

#### Option A: TensorFlow Lite Model Maker
```bash
cd model_training
pip install tflite-model-maker tensorflow
python train_model.py
```

1. Prepare dataset (see [DATASET_GUIDE.md](DATASET_GUIDE.md))
2. Train with custom architecture
3. Convert to TFLite with INT8 quantization
4. Generate C header file
5. Copy to `src/lpr_model.h`
6. Build and upload

#### Option B: Pre-Trained Model Adaptation
1. Download MobileNetV2 or similar
2. Fine-tune on your license plate data
3. Optimize for ESP32 constraints
4. Convert and deploy

📖 **Read**: [MODEL_RESOURCES.md](MODEL_RESOURCES.md) for tools and datasets

---

## 🏃 I Just Want to Test the Setup

### Quick Test (No Real Model)

The project includes a placeholder model for testing infrastructure:

```bash
# Build and upload
pio run --target upload

# Monitor output
pio device monitor
```

You should see:
- Camera initialization ✅
- Model loading ✅
- Image capture ✅
- Inference attempt (won't detect plates, just tests plumbing)

This confirms your hardware and software setup works!

---

## 📂 Project Structure Guide

```
Esp32Cam_LPR/
│
├── 📘 README.md                    ← Start here for overview
├── 🚀 QUICK_START.md               ← Fastest path to working demo
├── 📚 DATASET_GUIDE.md             ← How to collect/prepare data
├── 🔧 MODEL_RESOURCES.md           ← Pre-trained models & tools
├── 🐛 TROUBLESHOOTING.md           ← Fix common issues
│
├── platformio.ini                  ← PlatformIO configuration
│
├── src/
│   ├── main.cpp                    ← Main code (TFLite version)
│   ├── main_edge_impulse.cpp.example  ← Edge Impulse version
│   └── lpr_model.h                 ← Your trained model goes here
│
├── model_training/
│   ├── train_model.py              ← Custom TensorFlow training
│   └── edge_impulse_setup.py       ← Edge Impulse helper
│
└── lib/                            ← Put Edge Impulse library here
```

---

## ❓ Common Questions

### Q: Do I need a GPU to train?
**A**: No! 
- Edge Impulse trains on their servers (free)
- CPU training works for small datasets (slower)
- Google Colab offers free GPU if needed

### Q: How much data do I need?
**A**: Minimum 200 images per class, recommended 500+
- See [DATASET_GUIDE.md](DATASET_GUIDE.md)

### Q: Can I use this commercially?
**A**: 
- Code: Yes (check licenses)
- Models: Depends on training data license
- Always verify dataset licenses

### Q: What's the detection accuracy?
**A**: With good training data: 80-95%
- Depends on data quality and diversity
- See [MODEL_RESOURCES.md](MODEL_RESOURCES.md) for benchmarks

### Q: How fast is inference?
**A**: 100-500ms per image
- Depends on model complexity
- See optimization tips in README

### Q: My camera doesn't work!
**A**: Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Usually power supply issue
- Needs 5V, 2A minimum

---

## 🎯 Recommended Learning Order

### Complete Beginner
1. Read: [README.md](README.md) (Overview)
2. Do: [QUICK_START.md](QUICK_START.md) (Edge Impulse path)
3. Reference: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (if issues)
4. Learn: [DATASET_GUIDE.md](DATASET_GUIDE.md) (improve accuracy)

### Intermediate (Some ML Experience)
1. Skim: [README.md](README.md)
2. Review: [MODEL_RESOURCES.md](MODEL_RESOURCES.md) (choose approach)
3. Follow: Custom TensorFlow path
4. Optimize: Model based on performance

### Advanced (ML Expert)
1. Jump to: `model_training/train_model.py`
2. Review: ESP32 constraints in README
3. Experiment: Custom architectures
4. Contribute: Share improvements!

---

## 🔗 Quick Links

| I want to... | Go to... |
|--------------|----------|
| Get started ASAP | [QUICK_START.md](QUICK_START.md) |
| Understand the project | [README.md](README.md) |
| Train a model | [MODEL_RESOURCES.md](MODEL_RESOURCES.md) |
| Collect data | [DATASET_GUIDE.md](DATASET_GUIDE.md) |
| Fix an error | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| See example code | `src/main.cpp` |

---

## 🆘 Getting Help

### Before Asking:
1. ✅ Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. ✅ Review error messages
3. ✅ Try example code first
4. ✅ Verify hardware connections

### Where to Ask:
- **PlatformIO Issues**: https://community.platformio.org/
- **Edge Impulse Issues**: https://forum.edgeimpulse.com/
- **ESP32 Issues**: https://esp32.com/
- **General ML Questions**: https://stackoverflow.com/

### What to Include:
- Full error message
- Serial monitor output
- Hardware details (ESP32-CAM model)
- What you've tried already

---

## 📊 Expected Timeline

| Task | Beginner | Intermediate | Expert |
|------|----------|--------------|--------|
| Setup project | 30 min | 15 min | 5 min |
| Collect data | 2-4 hours | 1-2 hours | 30 min* |
| Train model | 1 hour | 2-4 hours | 1-8 hours |
| Deploy & test | 1 hour | 30 min | 15 min |
| **Total** | **4-6 hours** | **4-7 hours** | **2-9 hours** |

*Expert timeline assumes using existing datasets

---

## ✅ Success Checklist

You'll know it's working when:

- [ ] PlatformIO builds without errors
- [ ] ESP32-CAM uploads successfully
- [ ] Serial monitor shows camera initialization
- [ ] Model loads without errors
- [ ] Images captured successfully
- [ ] Inference runs (even with low accuracy at first)
- [ ] Detection confidence shown for each frame
- [ ] Can detect plates in good conditions

---

## 🎓 Next Steps After Success

1. **Improve Accuracy**:
   - Add more diverse training data
   - Adjust detection threshold
   - Try different model architectures

2. **Add Features**:
   - OCR for reading plate characters
   - Save detected plates to SD card
   - Send results over WiFi/MQTT
   - Add LED indicator for detections

3. **Optimize**:
   - Reduce inference time
   - Lower power consumption
   - Improve frame rate

4. **Deploy**:
   - Build enclosure
   - Add external antenna
   - Weatherproof for outdoor use
   - Integrate with larger system

---

## 🌟 Contributing

Improvements welcome!

- Share your trained models (with proper licensing)
- Report bugs or issues
- Suggest documentation improvements
- Add example datasets
- Optimize code performance

---

**Ready to start? → Go to [QUICK_START.md](QUICK_START.md)** 🚀

**Questions? → Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)** 🔧

**Happy Building!** 🎉
