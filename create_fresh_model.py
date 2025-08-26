#!/usr/bin/env python3
"""
Create a fresh model compatible with current TensorFlow version.
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models

def create_fresh_model():
    """Create a fresh model that's guaranteed to work with current TensorFlow."""
    print("🔄 Creating fresh compatible model...")
    
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
    
    print("✅ Fresh model created!")
    return model

def test_model(model):
    """Test if the model can make predictions."""
    print("Testing fresh model...")
    
    try:
        # Create a test image
        test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Preprocess for EfficientNet
        from tensorflow.keras.applications.efficientnet import preprocess_input
        test_image = preprocess_input(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        
        # Make prediction
        prediction = model.predict(test_image)
        class_idx = np.argmax(prediction)
        confidence = float(np.max(prediction))
        
        print(f"✅ Fresh model test successful!")
        print(f"   Predicted class: {class_idx}")
        print(f"   Confidence: {confidence:.4f}")
        print(f"   Output shape: {prediction.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fresh model test failed: {e}")
        return False

def main():
    """Create and test a fresh model."""
    print("🔄 Fresh Model Creation Tool")
    print("=" * 35)
    
    # Create fresh model
    model = create_fresh_model()
    
    # Test the model
    test_success = test_model(model)
    
    if test_success:
        # Save the model
        model.save("diabetic_model_fresh.h5")
        print("✅ Fresh model saved as 'diabetic_model_fresh.h5'")
        
        print("\n🎉 Fresh model creation completed successfully!")
        print("This model will work with your current TensorFlow version.")
        print("Note: This model has ImageNet weights but needs to be trained on your data.")
        
        return True
    else:
        print("\n❌ Fresh model creation failed!")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n📝 Next Steps:")
        print("1. Use 'diabetic_model_fresh.h5' in your Flask app")
        print("2. Train the model on your diabetic retinopathy dataset")
        print("3. Replace the model file once trained")
    else:
        print("\n⚠️  Please check your TensorFlow installation.")
