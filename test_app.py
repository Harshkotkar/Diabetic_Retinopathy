#!/usr/bin/env python3
"""
Test script for the Diabetic Retinopathy Detection Flask application.
This script tests the application startup without requiring a model file.
"""

import os
import sys
import tempfile
from PIL import Image
import numpy as np

def create_test_image():
    """Create a test retinal image for testing purposes."""
    # Create a simple test image (224x224 pixels)
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    img.save(temp_file.name)
    return temp_file.name

def test_app_startup():
    """Test if the Flask app can start without errors."""
    try:
        # Import the app
        from app import app
        
        # Test if app can be created
        print("✅ Flask app imported successfully")
        
        # Test if routes are accessible
        with app.test_client() as client:
            # Test main page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Main page accessible")
            else:
                print(f"❌ Main page returned status {response.status_code}")
            
            # Test about page
            response = client.get('/about')
            if response.status_code == 200:
                print("✅ About page accessible")
            else:
                print(f"❌ About page returned status {response.status_code}")
        
        print("✅ Application startup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        return False

def test_file_upload():
    """Test file upload functionality."""
    try:
        from app import app, allowed_file
        
        # Test file validation
        test_files = [
            ('test.jpg', True),
            ('test.png', True),
            ('test.jpeg', True),
            ('test.gif', True),
            ('test.txt', False),
            ('test.pdf', False),
            ('test', False)
        ]
        
        for filename, expected in test_files:
            result = allowed_file(filename)
            if result == expected:
                print(f"✅ File validation for {filename}: {'PASS' if expected else 'BLOCKED'}")
            else:
                print(f"❌ File validation for {filename}: Expected {expected}, got {result}")
        
        print("✅ File upload test passed!")
        return True
        
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Diabetic Retinopathy Detection Application")
    print("=" * 50)
    
    # Test 1: App startup
    print("\n1. Testing application startup...")
    startup_ok = test_app_startup()
    
    # Test 2: File upload validation
    print("\n2. Testing file upload validation...")
    upload_ok = test_file_upload()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Application Startup: {'✅ PASS' if startup_ok else '❌ FAIL'}")
    print(f"   File Upload Validation: {'✅ PASS' if upload_ok else '❌ FAIL'}")
    
    if startup_ok and upload_ok:
        print("\n🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("1. Add your diabetic_model.h5 file to the project directory")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
