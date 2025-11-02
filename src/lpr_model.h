/**
 * DEPRECATED: This file is replaced by the 3-stage ALPR models
 * 
 * Use these instead:
 * - detection_model.h (Stage 1: Plate detection)
 * - polygon_model.h (Stage 2: Corner detection)
 * - ocr_model.h (Stage 3: Character recognition)
 */

#ifndef LPR_MODEL_H
#define LPR_MODEL_H

// This is a placeholder - see new model files
const unsigned char lpr_model[] = {
    0x1c, 0x00, 0x00, 0x00, 0x54, 0x46, 0x4c, 0x33,
};

const unsigned int lpr_model_len = sizeof(lpr_model);

#endif // LPR_MODEL_H
