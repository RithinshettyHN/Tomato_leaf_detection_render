from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://rithurithin1605:XPYMu8C9sgROFPjT@cluster0.qqvakqq.mongodb.net/?retryWrites=true&w=majority')
db = client['flask_database']  # Updated database name
collection = db['tomato_leaf']  # Updated collection name

# Model saved with Keras model.save()
MODEL_PATH = 'model_inception.h5'

# Load your trained model
model = load_model(MODEL_PATH)

def model_predict(img, model):
    # Resize image to the required input size of the model
    img = img.resize((224, 224))

    # Convert image to numpy array
    x = image.img_to_array(img)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)
    
    # Make prediction
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    
    # Map prediction index to label
    labels = ["Bacterial_spot", "Early_blight", "Late_blight", "Leaf_Mold", "Septoria_leaf_spot", "Spider_mites Two-spotted_spider_mite", "Target_Spot", "Tomato_Yellow_Leaf_Curl_Virus", "Tomato_mosaic_virus", "Healthy"]
    result = labels[preds[0]]
    
    return result

@app.route('/')
def index():
    # Fetch all records from MongoDB
    records = collection.find({}, {'_id': 0, 'image_path': 1, 'predicted_disease': 1})
    # Create a list to store image paths and predicted diseases
    data = []
    for record in records:
        data.append({'image_path': record.get('image_path', ''), 'predicted_disease': record.get('predicted_disease', '')})
    return render_template('index.html', data=data)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in request'}), 400

    # Get the image file from the request
    image_file = request.files['image']

    # Convert the image file to a PIL Image object
    img = Image.open(io.BytesIO(image_file.read()))

    # Make prediction
    prediction = model_predict(img, model)

    # Save image and prediction to MongoDB
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG')
    img_byte_array = img_byte_array.getvalue()
    
    result = collection.insert_one({'image': img_byte_array, 'predicted_disease': prediction})

    return jsonify({'message': 'Prediction saved successfully!'}), 200

