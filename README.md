# Diabetic Retinopathy Detection Web Application

A Flask-based web application for detecting diabetic retinopathy from retinal images using deep learning. This application provides a user-friendly interface for uploading retinal images and receiving AI-powered analysis results.

## Features

- 🖼️ **Image Upload**: Drag-and-drop or click-to-upload retinal images
- 🤖 **AI Analysis**: Deep learning model for diabetic retinopathy detection
- 📊 **Results Display**: Clear presentation of prediction results with confidence scores
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🎨 **Modern UI**: Beautiful, intuitive interface with gradient backgrounds
- ⚡ **Real-time Processing**: Fast image analysis and results display

## Diabetic Retinopathy Stages

The application detects 5 stages of diabetic retinopathy:

1. **No DR (0)**: No signs of diabetic retinopathy
2. **Mild (1)**: Small areas of balloon-like swelling
3. **Moderate (2)**: More blood vessels are blocked
4. **Severe (3)**: Many more blood vessels are blocked
5. **Proliferative (4)**: Most severe stage with new blood vessels

## Prerequisites

- Python 3.8 or higher
- TensorFlow 2.x
- A trained model file (`model.h5`)

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Add your trained model**
   - Place your trained model file as `diabetic_model.h5` in the project root directory
   - The model should be trained for 5-class classification (0-4 stages)

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your web browser**
   - Navigate to `http://localhost:5000`
   - The application will be available on your local machine

3. **Upload and analyze images**
   - Click "Browse" to select a retinal image
   - Supported formats: PNG, JPG, JPEG, GIF
   - Click "Analyze Image" to process
   - View results with confidence scores and recommendations

## Project Structure

```
Diabetics/
├── app.py                  # Flask backend application
├── diabetic_model.h5       # Your trained model (add this)
├── static/
│   ├── style.css           # CSS styling
│   └── uploads/            # Uploaded images storage
├── templates/
│   ├── index.html          # Upload form page
│   └── result.html         # Results display page
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Model Requirements

Your `diabetic_model.h5` file should:
- Be trained on retinal images
- Accept input size of 224x224 pixels (EfficientNetB0 compatible)
- Output 5 classes (0-4 for diabetic retinopathy stages)
- Use softmax activation for the final layer
- Use EfficientNet-specific preprocessing

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for production deployment
- `SECRET_KEY`: Change the secret key in `app.py` for production

### Upload Settings
- Maximum file size: Configure in Flask settings if needed
- Allowed extensions: PNG, JPG, JPEG, GIF
- Upload folder: `static/uploads/` (created automatically)

## Deployment

### Local Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## API Endpoints

- `GET /`: Main upload page
- `POST /`: Process uploaded image
- `GET /about`: About page (can be implemented)

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- Missing files
- Model loading errors
- Image processing errors
- File upload issues

## Security Considerations

- File type validation
- Secure filename handling
- Input sanitization
- Error message sanitization
- Upload directory isolation

## Medical Disclaimer

⚠️ **Important**: This application is for educational and research purposes only. It should not be used for actual medical diagnosis. Always consult with qualified healthcare professionals for medical decisions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with any applicable licenses for the model and data used.

## Support

For issues or questions:
1. Check the error logs in the console
2. Verify your model file is correctly placed
3. Ensure all dependencies are installed
4. Check file permissions for the upload directory

## Future Enhancements

- User authentication
- Batch processing
- API endpoints for external integration
- Model versioning
- Result history
- Export functionality
- Multi-language support
