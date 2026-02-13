import cv2
import numpy as np
from tensorflow.keras.preprocessing import image

def error_model_predict(img_path, model):
    """Predict using error detection model"""
    load_image = cv2.imread(img_path)
    img = cv2.resize(load_image, (256, 256))
    x = image.img_to_array(img)
    x = x / 255
    x = np.expand_dims(x, axis=0)
    
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    
    return preds[0]

def preprocess_image(img_path, target_size):
    """Generic image preprocessing function"""
    load_image = cv2.imread(img_path)
    img = cv2.resize(load_image, target_size)
    
    x = image.img_to_array(img)
    x = x / 255
    x = np.expand_dims(x, axis=0)
    
    return x

def get_prediction_from_model(img_path, model, target_size):
    """Get raw prediction index from model"""
    x = preprocess_image(img_path, target_size)
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    return preds[0]
