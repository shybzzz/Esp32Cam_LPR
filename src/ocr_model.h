/**
 * Stage 3: OCR Character Recognition Model
 * 
 * This model reads the actual characters from the license plate
 * Architecture: CNN + CTC decoder
 * Input: 128x64x1 grayscale (perspective-corrected plate)
 * Output: Character probabilities for each position
 * 
 * HOW TO TRAIN:
 * =============
 * 
 * 1. DATASET PREPARATION
 * ----------------------
 * - Collect 10,000+ license plate images with text labels
 * - Use CCPD (Chinese plates), OpenALPR datasets
 * - Generate synthetic plates using Blender or graphics libraries
 * - Balance character distribution (important for accuracy)
 * 
 * 2. CHARACTER SET
 * ----------------
 * ```python
 * CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
 * # Add blank character for CTC: CHARACTERS + " "
 * ```
 * 
 * 3. TRAINING (Python/TensorFlow)
 * -------------------------------
 * ```python
 * import tensorflow as tf
 * from tensorflow import keras
 * 
 * # CNN backbone for feature extraction
 * def create_ocr_model(img_width=128, img_height=64):
 *     input_img = keras.Input(shape=(img_height, img_width, 1), name='image')
 *     
 *     # CNN layers
 *     x = keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
 *     x = keras.layers.MaxPooling2D((2, 2))(x)
 *     
 *     x = keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
 *     x = keras.layers.MaxPooling2D((2, 2))(x)
 *     
 *     x = keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
 *     x = keras.layers.MaxPooling2D((2, 2))(x)
 *     
 *     # Reshape for RNN
 *     x = keras.layers.Reshape(target_shape=((img_width // 8, (img_height // 8) * 128)))(x)
 *     
 *     # RNN layers (optional, use only if ESP32 has enough memory)
 *     # x = keras.layers.Bidirectional(keras.layers.LSTM(128, return_sequences=True))(x)
 *     # x = keras.layers.Bidirectional(keras.layers.LSTM(64, return_sequences=True))(x)
 *     
 *     # Dense layer for character prediction
 *     x = keras.layers.Dense(64, activation='relu')(x)
 *     output = keras.layers.Dense(len(CHARACTERS) + 1, activation='softmax')(x)  # +1 for blank
 *     
 *     model = keras.Model(inputs=input_img, outputs=output, name='ocr_model')
 *     return model
 * 
 * model = create_ocr_model()
 * 
 * # CTC Loss
 * def ctc_loss(y_true, y_pred):
 *     batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
 *     input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
 *     label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")
 *     
 *     input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
 *     label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")
 *     
 *     loss = keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
 *     return loss
 * 
 * model.compile(optimizer='adam', loss=ctc_loss)
 * 
 * # Train
 * model.fit(train_dataset, epochs=50, validation_data=val_dataset)
 * 
 * # Convert to TFLite with quantization
 * converter = tf.lite.TFLiteConverter.from_keras_model(model)
 * converter.optimizations = [tf.lite.Optimize.DEFAULT]
 * converter.target_spec.supported_types = [tf.int8]
 * 
 * tflite_model = converter.convert()
 * with open('ocr_model.tflite', 'wb') as f:
 *     f.write(tflite_model)
 * ```
 * 
 * 4. IMPORTANT: CTC DECODER
 * -------------------------
 * TFLite doesn't include CTC decoder, so you need to:
 * - Implement beam search decoder in C++ (see main.cpp)
 * - Or use greedy decoder for simpler/faster decoding
 * 
 * 5. SYNTHETIC DATA GENERATION
 * ----------------------------
 * ```python
 * from PIL import Image, ImageDraw, ImageFont
 * import random
 * 
 * def generate_plate(text, font_path):
 *     img = Image.new('L', (128, 64), color=255)  # White background
 *     draw = ImageDraw.Draw(img)
 *     font = ImageFont.truetype(font_path, 36)
 *     draw.text((10, 10), text, font=font, fill=0)  # Black text
 *     
 *     # Add noise, blur, perspective transforms
 *     # ...
 *     
 *     return img
 * 
 * # Generate balanced dataset
 * for _ in range(10000):
 *     text = ''.join(random.choices(CHARACTERS, k=7))
 *     img = generate_plate(text, 'font.ttf')
 *     img.save(f'synthetic/{text}.png')
 * ```
 * 
 * TARGET SPECS:
 * - Model size: < 300KB
 * - Inference time: < 500ms
 * - Character accuracy: > 95%
 * - Sequence accuracy: > 85%
 */

#ifndef OCR_MODEL_H
#define OCR_MODEL_H

// Placeholder - Replace with your trained OCR model
const unsigned char ocr_model_data[] = {
    0x1c, 0x00, 0x00, 0x00, 0x54, 0x46, 0x4c, 0x33,
    // Your actual model bytes here...
};

const unsigned int ocr_model_len = sizeof(ocr_model_data);

#endif // OCR_MODEL_H
