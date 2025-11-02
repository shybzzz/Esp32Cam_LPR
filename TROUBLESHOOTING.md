# Troubleshooting Guide

Common issues and solutions for ESP32-CAM License Plate Recognition project.

## 🔴 Build & Upload Issues

### Error: "espressif32 platform not found"

**Solution**:
```bash
# Update PlatformIO core
pio upgrade

# Install ESP32 platform
pio platform install espressif32
```

### Error: "Library not found: EloquentTinyML"

**Cause**: Library dependencies not installed

**Solution**:
```bash
# Let PlatformIO install dependencies
pio lib install

# Or manually install
pio lib install "EloquentTinyML"
pio lib install "EloquentEsp32Cam"
```

### Upload Fails: "Timed out waiting for packet header"

**Cause**: ESP32-CAM not in bootloader mode

**Solution**:
1. Connect GPIO0 to GND
2. Press RESET button
3. Start upload
4. After "Connecting..." appears, release RESET
5. After upload completes, disconnect GPIO0 from GND
6. Press RESET again

### Error: "No module named 'tensorflow'"

**Cause**: Python dependencies not installed

**Solution**:
```bash
# Install TensorFlow for model training
pip install tensorflow numpy pillow matplotlib
```

---

## 🟡 Camera Issues

### Camera Init Failed: 0x20001 or 0x20002

**Cause**: Power supply insufficient or camera connection issue

**Solutions**:
1. **Use external 5V power supply** (not USB from computer)
2. Check camera ribbon cable is firmly connected
3. Ensure correct cable orientation (blue side up on AI-Thinker)
4. Try different power source (minimum 2A)

**Code fix**:
```cpp
// Disable brownout detector
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

void setup() {
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Add this line
    // ... rest of setup
}
```

### Camera Produces Black/Corrupted Images

**Solutions**:
1. Check camera lens focus (some have manual focus ring)
2. Clean camera lens
3. Adjust exposure settings:
```cpp
sensor_t *s = esp_camera_sensor_get();
s->set_brightness(s, 1);     // -2 to 2
s->set_contrast(s, 1);       // -2 to 2
s->set_saturation(s, 0);     // -2 to 2
```

### Camera Freezes After Few Captures

**Cause**: Memory leak or buffer not returned

**Solution**:
```cpp
camera_fb_t *fb = esp_camera_fb_get();
// ... use frame buffer ...
esp_camera_fb_return(fb);  // MUST return buffer!
```

---

## 🟠 Model & Inference Issues

### Error: "Failed to initialize model"

**Possible Causes**:

1. **Model file too large**:
```cpp
// Check model size
Serial.print("Model size: ");
Serial.println(lpr_model_len);
// Should be < 300KB (300000 bytes)
```

2. **Invalid TFLite file**:
   - Verify model converted correctly
   - Check first bytes are TFLite header (0x1c, 0x00, 0x00, 0x00, 0x54, 0x46, 0x4c)

3. **Insufficient tensor arena**:
```cpp
// Try increasing
#define TENSOR_ARENA_SIZE 80*1024  // Increase from 60KB
```

### Error: "Invoke failed" or Inference Errors

**Solutions**:

1. **Check input shape matches model**:
```cpp
// Model expects: 96x96x1 (grayscale)
// Ensure preprocessing outputs correct size
Serial.print("Input size: ");
Serial.println(tinyml.getInputSize());
// Should be 9216 for 96x96
```

2. **Verify normalization**:
```cpp
// Most models expect [0, 1] or [-1, 1]
output[i] = imageData[i] / 255.0f;  // [0, 1]
// or
output[i] = (imageData[i] / 127.5f) - 1.0f;  // [-1, 1]
```

### Out of Memory / Guru Meditation Error

**Solutions**:

1. **Reduce tensor arena**:
```cpp
#define TENSOR_ARENA_SIZE 50*1024  // Reduce size
```

2. **Lower camera resolution**:
```cpp
camera.resolution.qvga();  // 320x240 instead of VGA
```

3. **Use PSRAM** (if available):
```cpp
// In platformio.ini, ensure:
build_flags = 
    -DBOARD_HAS_PSRAM
```

4. **Optimize model**:
   - Use INT8 quantization
   - Reduce number of layers
   - Smaller input resolution

---

## 🟢 Model Performance Issues

### Low Detection Accuracy (< 70%)

**Solutions**:

1. **More training data**:
   - Minimum 500 images per class
   - Include diverse conditions

2. **Improve data quality**:
   - Better lighting
   - Clearer images
   - Proper labeling

3. **Adjust detection threshold**:
```cpp
if (output[0] > 0.5) {  // Try 0.3-0.7 range
    Serial.println("Detected!");
}
```

4. **More training epochs**:
   - Increase from 20 to 50-100 epochs
   - Watch for overfitting

### High False Positive Rate

**Solutions**:

1. **Increase confidence threshold**:
```cpp
if (output[0] > 0.7) {  // More strict (was 0.5)
```

2. **Add more negative examples**:
   - Include similar non-plate rectangles
   - More diverse backgrounds

3. **Post-processing**:
```cpp
// Require multiple consecutive detections
int confirmCount = 0;
if (output[0] > threshold) {
    confirmCount++;
    if (confirmCount >= 3) {  // 3 consecutive frames
        Serial.println("Confirmed detection!");
    }
} else {
    confirmCount = 0;
}
```

### Slow Inference (> 1 second)

**Solutions**:

1. **Smaller model**:
   - Reduce layers
   - Use MobileNetV2 0.1 (smallest variant)

2. **Smaller input size**:
```cpp
#define INPUT_WIDTH 64   // Reduce from 96
#define INPUT_HEIGHT 64
```

3. **INT8 quantization** (if not already):
```python
converter.target_spec.supported_types = [tf.int8]
```

4. **Lower camera resolution**:
```cpp
camera.resolution.qqvga();  // 160x120
```

---

## 🔵 Edge Impulse Specific Issues

### "Cannot find inferencing.h"

**Cause**: Library not properly installed

**Solution**:
1. Download Arduino library from Edge Impulse
2. Extract to `lib/` folder:
```
lib/
└── your_project_name_inferencing/
    ├── src/
    ├── library.properties
    └── ...
```

### Edge Impulse Model Too Large

**Solution in Edge Impulse Studio**:

1. **Reduce image size**: 64x64 instead of 96x96
2. **Use MobileNetV2 0.1** (smallest)
3. **Enable quantization**: INT8
4. **Reduce neurons** in dense layers

### EON Compiler Errors

**Solution**:
- Disable EON compiler in deployment settings
- Use regular TFLite deployment instead

---

## 🟣 Serial Monitor Issues

### Garbled Output

**Solution**:
```bash
# Ensure baud rate matches
# In platformio.ini:
monitor_speed = 115200

# In code:
Serial.begin(115200);
```

### No Serial Output

**Solutions**:
1. Check USB cable supports data (not power-only)
2. Verify correct COM port selected
3. Add delays in setup():
```cpp
void setup() {
    Serial.begin(115200);
    delay(3000);  // Wait for serial to initialize
    Serial.println("Starting...");
}
```

---

## 📊 Debugging Tools

### Enable Debug Logging

```cpp
// In platformio.ini
build_flags = 
    -DCORE_DEBUG_LEVEL=4  // 0=None, 4=Verbose
```

### Memory Usage Check

```cpp
void printMemoryInfo() {
    Serial.print("Free heap: ");
    Serial.println(ESP.getFreeHeap());
    Serial.print("Free PSRAM: ");
    Serial.println(ESP.getFreePsram());
}
```

### Model Info

```cpp
void printModelInfo() {
    Serial.print("Input size: ");
    Serial.println(tinyml.getInputSize());
    Serial.print("Output size: ");
    Serial.println(tinyml.getOutputSize());
    Serial.print("Arena used: ");
    Serial.println(tinyml.getArenaUsedBytes());
}
```

---

## 🆘 Still Having Issues?

### Systematic Debugging:

1. **Isolate the problem**:
   - Test camera only (without model)
   - Test model with dummy data
   - Test preprocessing separately

2. **Check examples**:
   - Run EloquentEsp32Cam examples
   - Run TinyML examples
   - Compare with working code

3. **Serial output**:
   - Enable verbose logging
   - Print variable values
   - Use exception messages

4. **Hardware**:
   - Try different ESP32-CAM board
   - Test with known-good power supply
   - Check for damaged components

### Get Help:

- **PlatformIO**: https://community.platformio.org/
- **ESP32**: https://esp32.com/
- **Edge Impulse**: https://forum.edgeimpulse.com/
- **GitHub Issues**: Open issue with:
  - Full error message
  - Serial output
  - Code snippet
  - Hardware details

---

## ✅ Validation Checklist

Before asking for help, verify:

- [ ] Correct board selected in platformio.ini
- [ ] All libraries installed
- [ ] Model file exists and is valid
- [ ] Power supply adequate (5V, 2A)
- [ ] Camera properly connected
- [ ] Serial monitor at correct baud rate
- [ ] Latest PlatformIO version
- [ ] Reviewed similar GitHub issues
- [ ] Tested with example code

---

**Remember**: Most issues are power-related, memory constraints, or model compatibility!
