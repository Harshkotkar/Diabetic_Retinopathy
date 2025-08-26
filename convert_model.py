#!/usr/bin/env python3
"""
Convert model to compatible format for current TensorFlow version.
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models

def create_compatible_model():
    """Create a new model with the same architecture that's compatible with current TensorFlow."""
    print("🔄 Creating compatible model...")
    
    # Create the same architecture as the original model
    base_model = EfficientNetB0(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(5, activation='softmax')
    ])
    
    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    print("✅ Compatible model created!")
    return model

def convert_model():
    """Convert the existing model to a compatible format."""
    print("🔄 Converting model to compatible format...")
    
    try:
        # Try to load the original model
        print("Attempting to load original model...")
        original_model = tf.keras.models.load_model("diabetic_model.h5", compile=False)
        print("✅ Original model loaded successfully!")
        
        # Create a new compatible model
        compatible_model = create_compatible_model()
        
        # Copy weights from original to compatible model
        print("Copying weights...")
        for original_layer, compatible_layer in zip(original_model.layers, compatible_model.layers):
            if hasattr(original_layer, 'get_weights') and hasattr(compatible_layer, 'set_weights'):
                try:
                    weights = original_layer.get_weights()
                    compatible_layer.set_weights(weights)
                    print(f"✅ Copied weights for layer: {original_layer.name}")
                except Exception as e:
                    print(f"⚠️  Could not copy weights for layer {original_layer.name}: {e}")
        
        # Save the compatible model
        compatible_model.save("diabetic_model_compatible.h5")
        print("✅ Compatible model saved as 'diabetic_model_compatible.h5'")
        
        # Test the compatible model
        print("Testing compatible model...")
        test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        from tensorflow.keras.applications.efficientnet import preprocess_input
        test_image = preprocess_input(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        
        prediction = compatible_model.predict(test_image)
        class_idx = np.argmax(prediction)
        confidence = float(np.max(prediction))
        
        print(f"✅ Compatible model test successful!")
        print(f"   Predicted class: {class_idx}")
        print(f"   Confidence: {confidence:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model conversion failed: {e}")
        print("Creating a new model with random weights...")
        
        # Create a new model with random weights as fallback
        compatible_model = create_compatible_model()
        compatible_model.save("diabetic_model_compatible.h5")
        print("✅ New model saved as 'diabetic_model_compatible.h5'")
        print("⚠️  Note: This model has random weights and needs to be retrained!")
        
        return False

if __name__ == "__main__":
    print("🔄 Model Conversion Tool")
    print("=" * 30)
    success = convert_model()
    
    if success:
        print("\n🎉 Model conversion completed successfully!")
        print("You can now use 'diabetic_model_compatible.h5' in your Flask app.")
    else:
        print("\n⚠️  Model conversion completed with fallback.")
        print("The new model needs to be retrained with your data.")
