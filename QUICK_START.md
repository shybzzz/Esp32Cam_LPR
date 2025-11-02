# Example: Quick Test Model Setup

This guide helps you get started quickly with a pre-trained or example model.

## Option 1: Use Edge Impulse Pre-Made Project

The fastest way to get a working model:

### Steps:

1. **Go to Edge Impulse Public Projects**:
   - Visit: https://studio.edgeimpulse.com/public
   - Search for "license plate" or "vehicle detection"
   - Clone a suitable project

2. **Or Create from Template**:
   ```
   Login → Create New Project → "License Plate Detection"
   - Choose: Image Classification or Object Detection
   - Upload sample images (100-200 minimum)
   - Use MobileNetV2 0.1 architecture
   - Train for 20 epochs
   ```

3. **Deploy**:
   - Deployment → Arduino library
   - Download .zip
   - Extract to `lib/` folder in this project

4. **Update Code**:
   ```bash
   # Rename Edge Impulse example
   mv src/main_edge_impulse.cpp.example src/main.cpp
   
   # Edit main.cpp and replace:
   # #include <your_project_name_inferencing.h>
   # with your actual Edge Impulse project name
   ```

## Option 2: Download Pre-Trained TFLite Model

### Available Resources:

1. **TensorFlow Hub**:
   - Go to: https://tfhub.dev/
   - Search: "mobilenet v2 quantized"
   - Download and convert to appropriate input size

2. **Model Zoo**:
   - ONNX Model Zoo: https://github.com/onnx/models
   - Convert ONNX → TFLite using tools

### Example Commands:

```python
# If you have a .tflite file
import subprocess

# Convert to C array
subprocess.run([
    'xxd', '-i', 'model.tflite', 'src/lpr_model.h'
])
```

## Option 3: Minimal Test Model

For testing the infrastructure without a real model:

The project already includes a minimal placeholder in `src/lpr_model.h`.

To test the setup:

```bash
# Build (will compile but won't do real inference)
pio run

# Upload
pio run --target upload

# Monitor
pio device monitor
```

You should see camera initialization and model loading messages.

## Quick Dataset Collection

### Using ESP32-CAM to Collect Data:

Create a simple data collection sketch:

```cpp
// Save to src/data_collector.cpp
#include "esp_camera.h"
#include "FS.h"
#include "SD_MMC.h"

int imageCount = 0;

void setup() {
    // Initialize camera (same as main.cpp)
    // Initialize SD card
    if(!SD_MMC.begin()){
        Serial.println("SD Card Mount Failed");
        return;
    }
}

void loop() {
    camera_fb_t *fb = esp_camera_fb_get();
    if(!fb) return;
    
    // Save image
    String path = "/image_" + String(imageCount++) + ".jpg";
    File file = SD_MMC.open(path.c_str(), FILE_WRITE);
    file.write(fb->buf, fb->len);
    file.close();
    
    esp_camera_fb_return(fb);
    delay(5000); // Capture every 5 seconds
}
```

## Recommended Quick Start Path

**For absolute beginners**, follow this order:

1. ✅ **Test project setup** (Option 3 above)
2. ✅ **Run data collection** for 1-2 hours in different conditions
3. ✅ **Upload to Edge Impulse** (100-500 images)
4. ✅ **Train model** (15-30 minutes)
5. ✅ **Deploy and test** (Option 1)
6. ✅ **Iterate** based on results

## Expected Timeline

- **Setup PlatformIO project**: 15 minutes
- **Collect initial dataset**: 1-3 hours
- **Upload to Edge Impulse**: 30 minutes
- **Train first model**: 20-40 minutes
- **Deploy and test**: 30 minutes

**Total**: ~3-5 hours for first working prototype

## Validation Checklist

Before considering your model "ready":

- [ ] Model compiles and fits in ESP32 memory
- [ ] Inference runs without errors
- [ ] Detection confidence > 60% on test images
- [ ] False positive rate < 20%
- [ ] Inference time < 1 second
- [ ] Works in varied lighting conditions
- [ ] Tested with at least 50 real-world images

---

**Need Help?** Check:
- Edge Impulse Docs: https://docs.edgeimpulse.com/
- PlatformIO Docs: https://docs.platformio.org/
- ESP32-CAM Examples: Search GitHub for "esp32-cam tflite"
