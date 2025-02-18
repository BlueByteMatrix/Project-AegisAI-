from flask import Flask, render_template, request, redirect, url_for
import os
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import json
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MODEL_PATH = 'deepfake_detector_fine_tuned.h5'
model = load_model(MODEL_PATH)

with open('best_hyperparameters.json', 'r') as f:
    hyperparams = json.load(f)

@app.route('/')
def home():
    return render_template('anotherabout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('about_page'))
    return render_template('anotherlogin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('anotherregister.html')

@app.route('/about', methods=['POST', 'GET'])
def about_page():
    return render_template('anotherabout.html')

@app.route('/main', methods=['GET', 'POST'])
def main_page():
    result = None
    processing = False  

    if request.method == 'POST':
        processing = True  
        uploaded_file = request.files.get('user_image')
        if uploaded_file and uploaded_file.filename != '':
            allowed_extensions = {'mp4', 'avi', 'mov', 'jpg', 'png'}
            if '.' in uploaded_file.filename and \
                    uploaded_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)

                try:
                    frames = preprocess_video(file_path)
                    prediction = model.predict(frames)
                    result = "DeepFake Detected" if prediction[0] < 0.7 else "Real"
                except Exception as e:
                    result = f"Error during processing: {str(e)}"
                
                os.remove(file_path)  
            else:
                result = "Invalid file type. Please upload a valid video file."
        else:
            result = "No file uploaded. Please try again."
        processing = False

    return render_template('anothermainpage.html', result=result, processing=processing)


def preprocess_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224)) / 255.0
        frames.append(frame)
    cap.release()
    if not frames:
        raise ValueError("No valid frames extracted from the video.")
    
    # Debugging: Print shape of frames
    print("Frames shape:", np.array(frames).shape)
    return np.array(frames)


def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

try:
    test_image = preprocess_image(uploaded_image_path)
    prediction = model.predict(test_image)
    print("Prediction:", prediction)
except Exception as e:
    print(f"Error during image prediction: {str(e)}")

#print("Frames shape:", frames.shape)  

if __name__ == '__main__':
    app.run(debug=True)
