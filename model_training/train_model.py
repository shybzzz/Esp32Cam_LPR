"""
License Plate Recognition Model Training Script for ESP32-CAM
This script creates a lightweight TFLite model suitable for ESP32-CAM

Requirements:
pip install tensorflow numpy pillow matplotlib scikit-learn
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pathlib

# Model configuration for ESP32-CAM constraints
INPUT_SHAPE = (96, 96, 1)  # Grayscale 96x96
NUM_CLASSES = 2  # Binary: license_plate_present / no_license_plate

def create_lightweight_model(input_shape, num_classes):
    """
    Creates a MobileNetV2-inspired lightweight model for ESP32-CAM
    Target model size: < 300KB
    """
    model = keras.Sequential([
        # Input layer
        layers.Input(shape=input_shape),
        
        # First convolution block
        layers.Conv2D(16, 3, strides=2, padding='same', activation='relu'),
        layers.BatchNormalization(),
        
        # Depthwise separable convolutions (MobileNet style)
        layers.SeparableConv2D(32, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        
        layers.SeparableConv2D(64, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        
        layers.SeparableConv2D(128, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2),
        
        # Global pooling and classifier
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def convert_to_tflite(model, model_path='lpr_model.tflite'):
    """
    Convert Keras model to quantized TFLite for ESP32-CAM
    Uses INT8 quantization for minimal size
    """
    # Create converter
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Apply optimizations
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # INT8 quantization (smallest size)
    converter.target_spec.supported_types = [tf.int8]
    
    # Convert
    tflite_model = converter.convert()
    
    # Save
    with open(model_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"Model saved to {model_path}")
    print(f"Model size: {len(tflite_model) / 1024:.2f} KB")
    
    return tflite_model

def tflite_to_c_array(tflite_path, output_path='lpr_model.h'):
    """
    Convert TFLite model to C array for Arduino
    """
    with open(tflite_path, 'rb') as f:
        model_data = f.read()
    
    # Generate C header file
    with open(output_path, 'w') as f:
        f.write('#ifndef LPR_MODEL_H\n')
        f.write('#define LPR_MODEL_H\n\n')
        f.write('const unsigned char lpr_model[] = {\n')
        
        # Write bytes in hex format
        for i in range(0, len(model_data), 12):
            chunk = model_data[i:i+12]
            hex_values = ', '.join([f'0x{b:02x}' for b in chunk])
            f.write(f'  {hex_values},\n')
        
        f.write('};\n\n')
        f.write(f'const unsigned int lpr_model_len = {len(model_data)};\n\n')
        f.write('#endif // LPR_MODEL_H\n')
    
    print(f"C array saved to {output_path}")

def main():
    print("Creating lightweight LPR model for ESP32-CAM...")
    
    # Create model
    model = create_lightweight_model(INPUT_SHAPE, NUM_CLASSES)
    
    # Display model summary
    model.summary()
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n" + "="*60)
    print("MODEL CREATED - Next Steps:")
    print("="*60)
    print("1. Collect and label your license plate dataset")
    print("2. Train the model using model.fit(X_train, y_train, ...)")
    print("3. Run convert_to_tflite(model) to create .tflite file")
    print("4. Run tflite_to_c_array('lpr_model.tflite') to create .h file")
    print("5. Copy the .h file to your ESP32-CAM project src/ folder")
    print("\nAlternatively, use Edge Impulse for easier workflow:")
    print("https://www.edgeimpulse.com/")
    print("="*60)
    
    # Example: Create and convert a dummy trained model
    print("\nCreating example model (untrained)...")
    
    # Generate some dummy data for model initialization
    dummy_data = np.random.rand(10, 96, 96, 1).astype(np.float32)
    dummy_labels = np.random.randint(0, 2, 10)
    
    # Fit for one epoch just to initialize weights
    model.fit(dummy_data, dummy_labels, epochs=1, verbose=0)
    
    # Convert to TFLite
    convert_to_tflite(model, 'lpr_model_example.tflite')
    
    # Convert to C array
    tflite_to_c_array('lpr_model_example.tflite', 'lpr_model_example.h')
    
    print("\nExample model files created!")
    print("NOTE: This is an UNTRAINED model for demonstration only.")
    print("You need to train with real data for actual license plate recognition.")

if __name__ == '__main__':
    main()
