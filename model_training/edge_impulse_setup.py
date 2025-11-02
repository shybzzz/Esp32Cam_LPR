"""
Edge Impulse Integration Guide for ESP32-CAM License Plate Recognition

This script helps you prepare data for Edge Impulse and integrate the resulting model.

Edge Impulse provides:
- Web-based model training (no local ML setup needed)
- Automatic optimization for ESP32
- Pre-built Arduino libraries
- Built-in data augmentation
"""

import os
import json
import shutil
from pathlib import Path

def create_edge_impulse_structure():
    """
    Creates folder structure for Edge Impulse data collection
    """
    folders = [
        'edge_impulse_data/training/license_plate',
        'edge_impulse_data/training/no_plate',
        'edge_impulse_data/testing/license_plate',
        'edge_impulse_data/testing/no_plate'
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    print("Edge Impulse data folders created!")
    print("\nFolder structure:")
    for folder in folders:
        print(f"  {folder}/")
    
    print("\n" + "="*60)
    print("NEXT STEPS FOR EDGE IMPULSE:")
    print("="*60)
    print("\n1. COLLECT DATA:")
    print("   - Add license plate images to: edge_impulse_data/training/license_plate/")
    print("   - Add non-plate images to: edge_impulse_data/training/no_plate/")
    print("   - Split ~20% to testing folders")
    print("   - Recommended: 500+ images per class")
    
    print("\n2. CREATE EDGE IMPULSE PROJECT:")
    print("   a. Go to https://studio.edgeimpulse.com/")
    print("   b. Create new project")
    print("   c. Click 'Data acquisition'")
    print("   d. Upload images from your folders")
    print("   e. Label them appropriately")
    
    print("\n3. DESIGN IMPULSE:")
    print("   a. Image data: 96x96 pixels, Grayscale")
    print("   b. Processing block: 'Image'")
    print("   c. Learning block: 'Transfer Learning (Images)' or 'Classification'")
    print("   d. Use MobileNetV2 0.1 (smallest variant)")
    
    print("\n4. TRAIN MODEL:")
    print("   a. Configure neural network:")
    print("      - Number of epochs: 20-50")
    print("      - Learning rate: 0.001")
    print("      - Data augmentation: ON")
    print("   b. Click 'Start training'")
    print("   c. Wait for training to complete")
    
    print("\n5. DEPLOY TO ESP32:")
    print("   a. Go to 'Deployment'")
    print("   b. Select 'Arduino library'")
    print("   c. Download the .zip file")
    print("   d. Extract to Arduino libraries folder, OR:")
    print("      - Extract and copy model files to this project")
    
    print("\n6. INTEGRATE WITH THIS PROJECT:")
    print("   Option A - Use as PlatformIO library:")
    print("     - Extract the zip to lib/ folder in this project")
    print("     - Update main.cpp to use Edge Impulse SDK")
    print("   ")
    print("   Option B - Extract model only:")
    print("     - Find the .tflite or model .h file in the library")
    print("     - Copy to src/lpr_model.h")
    print("="*60)

def create_edge_impulse_main():
    """
    Creates an alternative main.cpp that uses Edge Impulse SDK
    """
    code = """/**
 * ESP32-CAM License Plate Recognition with Edge Impulse
 * 
 * After training your model on Edge Impulse:
 * 1. Download as Arduino library
 * 2. Extract to lib/ folder
 * 3. Update the include below with your project name
 */

#include <your_project_name_inferencing.h>  // Replace with your Edge Impulse project name
#include "edge-impulse-sdk/dsp/image/image.hpp"

// Camera includes
#include "esp_camera.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

// AI-Thinker ESP32-CAM pin definition
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup_camera() {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_GRAYSCALE;
    config.frame_size = FRAMESIZE_96X96;  // Match your Edge Impulse input
    config.jpeg_quality = 12;
    config.fb_count = 1;
    
    // Initialize camera
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed: 0x%x\\n", err);
        return;
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("Edge Impulse ESP32-CAM License Plate Recognition");
    
    // Disable brownout detector
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
    
    setup_camera();
    
    Serial.println("Setup complete!");
}

void loop() {
    ei_impulse_result_t result = {0};
    
    // Capture image
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Camera capture failed");
        delay(1000);
        return;
    }
    
    // Convert to features
    signal_t signal;
    signal.total_length = EI_CLASSIFIER_INPUT_WIDTH * EI_CLASSIFIER_INPUT_HEIGHT;
    signal.get_data = [](size_t offset, size_t length, float *out_ptr) -> int {
        // Image data conversion happens here
        return 0;
    };
    
    // Run classifier
    EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);
    
    if (res != EI_IMPULSE_OK) {
        Serial.printf("ERR: Failed to run classifier (%d)\\n", res);
        esp_camera_fb_return(fb);
        return;
    }
    
    // Print results
    Serial.println("Predictions:");
    for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
        Serial.printf("    %s: %.5f\\n", result.classification[ix].label, 
                      result.classification[ix].value);
    }
    
    // Check if license plate detected
    if (result.classification[0].value > 0.7) {  // Adjust threshold
        Serial.println("✓ License Plate Detected!");
    }
    
    // Return frame buffer
    esp_camera_fb_return(fb);
    
    delay(2000);
}
"""
    
    with open('src/main_edge_impulse.cpp.example', 'w') as f:
        f.write(code)
    
    print("\nCreated: src/main_edge_impulse.cpp.example")
    print("Rename to main.cpp after setting up Edge Impulse library")

def main():
    print("="*60)
    print("EDGE IMPULSE SETUP FOR ESP32-CAM LICENSE PLATE RECOGNITION")
    print("="*60)
    
    create_edge_impulse_structure()
    print("\n")
    create_edge_impulse_main()
    
    print("\n" + "="*60)
    print("HELPFUL RESOURCES:")
    print("="*60)
    print("- Edge Impulse Docs: https://docs.edgeimpulse.com/")
    print("- ESP32-CAM Tutorial: https://docs.edgeimpulse.com/docs/esp32")
    print("- Example Projects: https://docs.edgeimpulse.com/docs/tutorials")
    print("- License Plate Datasets:")
    print("  - Kaggle: https://www.kaggle.com/datasets (search 'license plate')")
    print("  - Roboflow: https://universe.roboflow.com/ (pre-labeled datasets)")
    print("="*60)

if __name__ == '__main__':
    main()
