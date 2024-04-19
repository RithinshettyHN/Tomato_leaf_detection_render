# from flask import Flask, render_template, request, jsonify
# from pymongo import MongoClient
# from PIL import Image
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import numpy as np
# import io

# app = Flask(__name__)

# # Connect to MongoDB
# client = MongoClient('mongodb+srv://rithurithin1605:XPYMu8C9sgROFPjT@cluster0.qqvakqq.mongodb.net/?retryWrites=true&w=majority')
# db = client['flask_database']  # Updated database name
# collection = db['tomato_leaf']  # Updated collection name

# # Model saved with Keras model.save()
# MODEL_PATH = 'model_inception.h5'

# # Load your trained model
# model = load_model(MODEL_PATH)

# def model_predict(img, model):
#     # Resize image to the required input size of the model
#     img = img.resize((224, 224))

#     # Convert image to numpy array
#     x = image.img_to_array(img)
#     x = x / 255.0
#     x = np.expand_dims(x, axis=0)
    
#     # Make prediction
#     preds = model.predict(x)
#     preds = np.argmax(preds, axis=1)
    
#     # Map prediction index to label
#     labels = ["Bacterial_spot", "Early_blight", "Late_blight", "Leaf_Mold", "Septoria_leaf_spot", "Spider_mites Two-spotted_spider_mite", "Target_Spot", "Tomato_Yellow_Leaf_Curl_Virus", "Tomato_mosaic_virus", "Healthy"]
#     result = labels[preds[0]]
    
#     return result

# @app.route('/')
# def index():
#     # Fetch all records from MongoDB
#     records = collection.find({}, {'_id': 0, 'image_path': 1, 'predicted_disease': 1})
#     # Create a list to store image paths and predicted diseases
#     data = []
#     for record in records:
#         data.append({'image_path': record.get('image_path', ''), 'predicted_disease': record.get('predicted_disease', '')})
#     return render_template('index.html', data=data)

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Check if the request contains an image file
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image found in request'}), 400

#     # Get the image file from the request
#     image_file = request.files['image']

#     # Convert the image file to a PIL Image object
#     img = Image.open(io.BytesIO(image_file.read()))

#     # Make prediction
#     prediction = model_predict(img, model)

#     # Save image and prediction to MongoDB
#     img_byte_array = io.BytesIO()
#     img.save(img_byte_array, format='JPEG')
#     img_byte_array = img_byte_array.getvalue()
    
#     result = collection.insert_one({'image': img_byte_array, 'predicted_disease': prediction})

#     return jsonify({'message': 'Prediction saved successfully!'}), 200

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import base64

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

def get_disease_info(disease):
    info = {
        "Bacterial_spot": {
            "Cause": "Caused by bacteria, typically Xanthomonas campestris.",
            "Effect": "Causes small, dark, water-soaked spots on leaves and fruit, leading to defoliation and reduced yield.",
            "Preventive Measures": "Use disease-resistant varieties, practice crop rotation, avoid overhead irrigation, and apply copper-based fungicides.",
            "Potential Pesticides": "Copper-based fungicides like copper hydroxide or copper oxychloride."
        },
        "Early_blight": {
            "Cause": "Fungal infection, usually Alternaria solani.",
            "Effect": "Causes dark, concentric rings on leaves, leading to leaf yellowing, premature defoliation, and reduced yield.",
            "Preventive Measures": "Practice crop rotation, avoid overhead irrigation, apply fungicides containing chlorothalonil or mancozeb.",
            "Potential Pesticides": "Fungicides containing chlorothalonil or mancozeb."
        },
        "Late_blight": {
            "Cause": "Fungal infection, typically Phytophthora infestans.",
            "Effect": "Causes dark, water-soaked lesions on leaves and stems, leading to rapid defoliation and yield loss.",
            "Preventive Measures": "Practice crop rotation, use certified disease-free seed, avoid overhead irrigation, apply fungicides containing chlorothalonil or mancozeb.",
            "Potential Pesticides": "Fungicides containing chlorothalonil or mancozeb."
        },
        "Leaf_Mold": {
            "Cause": "Fungal infection, typically Fulvia fulva.",
            "Effect": "Causes yellowing and wilting of leaves, with the development of white to gray fuzzy growth on the undersides.",
            "Preventive Measures": "Practice proper spacing between plants for good air circulation, avoid overhead irrigation, apply fungicides containing chlorothalonil or mancozeb.",
            "Potential Pesticides": "Fungicides containing chlorothalonil or mancozeb."
        },
        "Septoria_leaf_spot": {
            "Cause": "Fungal infection, usually Septoria lycopersici.",
            "Effect": "Causes small, circular spots with dark margins on leaves, leading to defoliation and reduced yield.",
            "Preventive Measures": "Practice crop rotation, remove infected plant debris, avoid overhead irrigation, apply fungicides containing chlorothalonil or mancozeb.",
            "Potential Pesticides": "Fungicides containing chlorothalonil or mancozeb."
        },
        "Spider_mites Two-spotted_spider_mite": {
            "Cause": "Caused by spider mites, typically Tetranychus urticae.",
            "Effect": "Feeding by mites causes stippling, webbing, and leaf discoloration, leading to reduced photosynthesis and plant vigor.",
            "Preventive Measures": "Use biological control agents like predatory mites, maintain proper plant hygiene, and avoid dust and drought stress.",
            "Potential Pesticides": "Acaricides like abamectin or bifenthrin."
        },
        "Target_Spot": {
            "Cause": "Fungal infection, usually Corynespora cassiicola.",
            "Effect": "Causes circular, target-like lesions with concentric rings on leaves, leading to defoliation and reduced yield.",
            "Preventive Measures": "Practice crop rotation, remove infected plant debris, avoid overhead irrigation, apply fungicides containing chlorothalonil or mancozeb.",
            "Potential Pesticides": "Fungicides containing chlorothalonil or mancozeb."
        },
        "Tomato_Yellow_Leaf_Curl_Virus": {
            "Cause": "Caused by tomato yellow leaf curl virus transmitted by whiteflies.",
            "Effect": "Causes yellowing, curling, and stunting of leaves, with reduced fruit yield and quality.",
            "Preventive Measures": "Use reflective mulches, employ insecticides to control whiteflies, remove infected plants, and use resistant varieties.",
            "Potential Pesticides": "Insecticides like neonicotinoids or pyrethroids."
        },
        "Tomato_mosaic_virus": {
            "Cause": "Caused by tomato mosaic virus, usually transmitted by contact with infected plants or contaminated tools.",
            "Effect": "Causes mottling, distortion, and yellowing of leaves, leading to reduced plant vigor and yield.",
            "Preventive Measures": "Use disease-free seeds, control aphid populations, remove infected plants promptly, and disinfect tools.",
            "Potential Pesticides": "No specific pesticides for controlling viruses, focus on preventive measures."
        },
        "Healthy": {
            "Cause": "No disease present.",
            "Effect": "Plants are free from any disease symptoms.",
            "Preventive Measures": "Maintain good plant health, practice proper cultural practices, and monitor for any signs of disease.",
            "Potential Pesticides": "No pesticides required for healthy plants."
        }
    }
    return info.get(disease, {})



@app.route('/')
def index():
    # Fetch all records from MongoDB
    records = collection.find({}, {'_id': 0, 'file_data': 1, 'predicted_disease': 1})
    
    # Create a list to store image data, predicted diseases, and image URLs
    data = []
    for record in records:
        if 'file_data' in record:
            # Convert binary image data to base64 for rendering in HTML
            image_data = record['file_data']
            # Encode the binary data as base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            # Construct a data URL for the image
            image_url = f"data:image/jpeg;base64,{image_base64}"
        else:
            # If image data is not available, set image URL to None
            image_url = None
        
        # Get disease information
        disease = record.get('predicted_disease', '')
        disease_info = get_disease_info(disease)
        
        data.append({'image_url': image_url, 'predicted_disease': disease, 'disease_info': disease_info})

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
