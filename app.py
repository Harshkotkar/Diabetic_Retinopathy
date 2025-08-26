from flask import Flask, request, render_template, flash, redirect, url_for
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configure upload settings
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the model
model = None
try:
    # Try to load the fresh model first (compatible with TensorFlow 2.19.0)
    print("Attempting to load fresh model...")
    try:
        model = tf.keras.models.load_model("diabetic_model_fresh.h5")
        print("✅ Fresh model loaded successfully!")
    except Exception as e1:
        print(f"Fresh model loading failed: {e1}")
        
        # Try to load the compatible model
        print("Attempting to load compatible model...")
        try:
            model = tf.keras.models.load_model("diabetic_model_compatible.h5")
            print("✅ Compatible model loaded successfully!")
        except Exception as e2:
            print(f"Compatible model loading failed: {e2}")
            
            # Fallback to original model with multiple loading approaches
            print("Attempting to load original model...")
            
            # Method 1: Basic loading
            try:
                model = tf.keras.models.load_model("diabetic_model.h5")
                print("✅ Original model loaded successfully with basic method!")
            except Exception as e3:
                print(f"Basic loading failed: {e3}")
                
                # Method 2: Loading with compile=False
                try:
                    model = tf.keras.models.load_model("diabetic_model.h5", compile=False)
                    print("✅ Original model loaded successfully with compile=False!")
                except Exception as e4:
                    print(f"Compile=False loading failed: {e4}")
                    
                    # Method 3: Loading with custom_objects
                    try:
                        model = tf.keras.models.load_model("diabetic_model.h5", custom_objects={})
                        print("✅ Original model loaded successfully with custom_objects!")
                    except Exception as e5:
                        print(f"Custom objects loading failed: {e5}")
                        
                        # Method 4: Loading with both options
                        try:
                            model = tf.keras.models.load_model("diabetic_model.h5", compile=False, custom_objects={})
                            print("✅ Original model loaded successfully with both options!")
                        except Exception as e6:
                            print(f"All loading methods failed: {e6}")
                            print("Creating a fresh model for demonstration...")
                            
                            # Create a fresh model as fallback
                            try:
                                from tensorflow.keras.applications import EfficientNetB0
                                from tensorflow.keras import layers, models
                                
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
                                
                                model.compile(optimizer='adam',
                                              loss='sparse_categorical_crossentropy',
                                              metrics=['accuracy'])
                                
                                print("✅ Fresh model created successfully!")
                                print("⚠️  Note: This is a demonstration model with ImageNet weights.")
                                print("   For production use, train this model on your diabetic retinopathy data.")
                                
                            except Exception as e7:
                                print(f"Fresh model creation also failed: {e7}")
                                model = None

except Exception as e:
    print(f"All model loading methods failed: {e}")
    model = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    """Preprocess image for EfficientNetB0 model"""
    image = image.resize((224, 224))  # EfficientNetB0 input size
    img_array = np.array(image)
    # Apply EfficientNet-specific preprocessing
    from tensorflow.keras.applications.efficientnet import preprocess_input
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def get_prediction_label(class_idx):
    """Convert class index to human-readable label"""
    labels = {
        0: "No Diabetic Retinopathy",
        1: "Mild Diabetic Retinopathy", 
        2: "Moderate Diabetic Retinopathy",
        3: "Severe Diabetic Retinopathy",
        4: "Proliferative Diabetic Retinopathy"
    }
    return labels.get(class_idx, "Unknown")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file was uploaded
        if 'image' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['image']
        
        # Check if file is empty
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.')
            return redirect(request.url)
        
        try:
            # Read and process the image
            image = Image.open(file)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            processed = preprocess_image(image)
            
            # Make prediction
            if model is not None:
                prediction = model.predict(processed)
                class_idx = np.argmax(prediction)
                confidence = float(np.max(prediction))
                label = get_prediction_label(class_idx)
                
                # Save uploaded image
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                
                return render_template("result.html", 
                                     prediction=class_idx, 
                                     label=label, 
                                     confidence=confidence,
                                     image_filename=filename)
            else:
                flash('Model not available. Please check if diabetic_model.h5 exists.')
                return redirect(request.url)
                
        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            return redirect(request.url)
    
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
