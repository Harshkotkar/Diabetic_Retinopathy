#!/usr/bin/env python3
"""
Test script to check model loading compatibility.
"""

import tensorflow as tf
import numpy as np
from PIL import Image

def test_model_loading():
    """Test different model loading approaches."""
    print("🧪 Testing Model Loading Compatibility")
    print("=" * 50)
    
    # Test 1: Basic loading
    print("\n1. Testing basic model loading...")
    try:
        model = tf.keras.models.load_model("diabetic_model.h5")
        print("✅ Basic loading successful!")
        return model
    except Exception as e:
        print(f"❌ Basic loading failed: {e}")
    
    # Test 2: Loading with compile=False
    print("\n2. Testing loading with compile=False...")
    try:
        model = tf.keras.models.load_model("diabetic_model.h5", compile=False)
        print("✅ Loading with compile=False successful!")
        return model
    except Exception as e:
        print(f"❌ Loading with compile=False failed: {e}")
    
    # Test 3: Loading with custom_objects
    print("\n3. Testing loading with custom_objects...")
    try:
        model = tf.keras.models.load_model("diabetic_model.h5", custom_objects={})
        print("✅ Loading with custom_objects successful!")
        return model
    except Exception as e:
        print(f"❌ Loading with custom_objects failed: {e}")
    
    # Test 4: Loading with both options
    print("\n4. Testing loading with both compile=False and custom_objects...")
    try:
        model = tf.keras.models.load_model("diabetic_model.h5", compile=False, custom_objects={})
        print("✅ Loading with both options successful!")
        return model
    except Exception as e:
        print(f"❌ Loading with both options failed: {e}")
    
    print("\n❌ All loading methods failed!")
    return None

def test_model_prediction(model):
    """Test if the loaded model can make predictions."""
    if model is None:
        print("❌ No model to test!")
        return False
    
    print("\n🧪 Testing Model Prediction")
    print("=" * 30)
    
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
        
        print(f"✅ Prediction successful!")
        print(f"   Predicted class: {class_idx}")
        print(f"   Confidence: {confidence:.4f}")
        print(f"   Output shape: {prediction.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def main():
    """Run all tests."""
    # Test model loading
    model = test_model_loading()
    
    if model is not None:
        # Test prediction
        prediction_ok = test_model_prediction(model)
        
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print(f"   Model Loading: ✅ SUCCESS")
        print(f"   Model Prediction: {'✅ SUCCESS' if prediction_ok else '❌ FAIL'}")
        
        if prediction_ok:
            print("\n🎉 Model is working correctly!")
        else:
            print("\n⚠️  Model loaded but prediction failed.")
    else:
        print("\n❌ Model loading failed completely.")

if __name__ == "__main__":
    main()
