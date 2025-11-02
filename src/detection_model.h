/**
 * Stage 1: License Plate Detection Model
 * 
 * This model detects the location of license plates in images
 * Architecture: Tiny YOLOv3 or MobileNetV2-SSD
 * Input: 320x320x1 grayscale image
 * Output: Bounding box coordinates [x1, y1, x2, y2, confidence]
 * 
 * HOW TO TRAIN:
 * =============
 * 
 * 1. DATASET PREPARATION
 * ----------------------
 * - Collect 1000+ vehicle images with visible plates
 * - Annotate bounding boxes using LabelImg or CVAT
 * - Use datasets: CCPD, Stanford Cars, or collect from YouTube traffic cams
 * - Apply data augmentation: rotation, brightness, scale variations
 * 
 * 2. TRAINING (Python/TensorFlow)
 * -------------------------------
 * ```python
 * import tensorflow as tf
 * from tensorflow import keras
 * 
 * # Use MobileNetV2 as backbone for efficiency
 * base_model = tf.keras.applications.MobileNetV2(
 *     input_shape=(320, 320, 3),
 *     alpha=0.35,  # Smallest variant
 *     include_top=False,
 *     weights='imagenet'
 * )
 * 
 * # Add detection head
 * model = keras.Sequential([
 *     base_model,
 *     keras.layers.GlobalAveragePooling2D(),
 *     keras.layers.Dense(128, activation='relu'),
 *     keras.layers.Dense(5)  # [x1, y1, x2, y2, confidence]
 * ])
 * 
 * # Compile with appropriate loss
 * model.compile(
 *     optimizer='adam',
 *     loss='mse',  # For bbox regression
 *     metrics=['accuracy']
 * )
 * 
 * # Train
 * model.fit(train_dataset, epochs=50, validation_data=val_dataset)
 * 
 * # Convert to TFLite with INT8 quantization
 * converter = tf.lite.TFLiteConverter.from_keras_model(model)
 * converter.optimizations = [tf.lite.Optimize.DEFAULT]
 * converter.target_spec.supported_types = [tf.int8]
 * 
 * tflite_model = converter.convert()
 * with open('detection_model.tflite', 'wb') as f:
 *     f.write(tflite_model)
 * ```
 * 
 * 3. CONVERT TO C ARRAY
 * ---------------------
 * ```bash
 * xxd -i detection_model.tflite > detection_model.h
 * # Or use: https://notisrac.github.io/FileToCArray/
 * ```
 * 
 * 4. REPLACE THIS FILE
 * --------------------
 * Replace the placeholder below with your actual model data
 * 
 * TARGET SPECS:
 * - Model size: < 200KB
 * - Inference time: < 300ms
 * - Accuracy: > 95% on validation set
 */

#ifndef DETECTION_MODEL_H
#define DETECTION_MODEL_H

// Placeholder - Replace with your trained detection model
const unsigned char detection_model_data[] = {
    0x1c, 0x00, 0x00, 0x00, 0x54, 0x46, 0x4c, 0x33,
    // Your actual model bytes here...
};

const unsigned int detection_model_len = sizeof(detection_model_data);

#endif // DETECTION_MODEL_H
