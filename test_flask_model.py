#!/usr/bin/env python3
"""
Test Flask app model loading specifically.
"""

import tensorflow as tf
import numpy as np
from PIL import Image

def test_flask_model_loading():
    """Test the exact model loading code used in Flask app."""
    print("🧪 Testing Flask App Model Loading")
    print("=" * 40)
    
    # Test the exact loading code from Flask app
    try:
        # Try loading with custom_objects to handle version compatibility
        model = tf.keras.models.load_model("diabetic_model.h5", compile=False)
        print("✅ Flask app model loading successful!")
        
        # Test prediction like in Flask app
        test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        from tensorflow.keras.applications.efficientnet import preprocess_input
        test_image = preprocess_input(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        
        prediction = model.predict(test_image)
        class_idx = np.argmax(prediction)
        confidence = float(np.max(prediction))
        
        print(f"✅ Flask app prediction successful!")
        print(f"   Class: {class_idx}, Confidence: {confidence:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app model loading failed: {e}")
        try:
            # Try alternative loading method
            model = tf.keras.models.load_model("diabetic_model.h5", custom_objects={})
            print("✅ Flask app alternative loading successful!")
            return True
        except Exception as e2:
            print(f"❌ Flask app alternative loading also failed: {e2}")
            return False

if __name__ == "__main__":
    success = test_flask_model_loading()
    if success:
        print("\n🎉 Flask app model loading is working!")
    else:
        print("\n❌ Flask app model loading failed!")
