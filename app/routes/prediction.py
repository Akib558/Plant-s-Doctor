import os
from flask import Blueprint, request, jsonify, session, render_template
from app.utils.decorators import login_required, admin_required, has_credits
from app.utils.validators import save_upload_file, cleanup_file
from app.ml.predictors import predict_tomato, predict_apple, predict_potato, predict_rice, predict_admin
from app.services.user_service import deduct_prediction_credit
from app.models import Prediction
from app import db

prediction_bp = Blueprint('prediction', __name__)

def handle_prediction(plant_type, predict_function):
    """Generic handler for plant disease prediction"""
    f = request.files.get('image')
    
    if not f:
        return jsonify({'name': "You Haven't Choose anything YET !!!"})
    
    file_path = save_upload_file(f)
    
    if not file_path:
        return jsonify({'name': "Invalid file type. Please upload an image."})
    
    try:
        result = predict_function(file_path)
        
        session['prediction_credits'] = session.get('prediction_credits', 0) - 1
        deduct_prediction_credit(session['user_id'])
        
        prediction = Prediction(
            user_id=session['user_id'],
            plant_type=plant_type,
            image_filename=os.path.basename(file_path),
            prediction_result=result
        )
        db.session.add(prediction)
        db.session.commit()
        
        cleanup_file(file_path)
        
        return jsonify({'name': result})
    
    except Exception as e:
        cleanup_file(file_path)
        return jsonify({'name': f"Error processing image: {str(e)}"})

@prediction_bp.route('/tomato-predict', methods=['POST'])
@login_required
@has_credits
def tomato_predict():
    """Predict tomato disease"""
    return handle_prediction('tomato', predict_tomato)

@prediction_bp.route('/apple-predict', methods=['POST'])
@login_required
@has_credits
def apple_predict():
    """Predict apple disease"""
    return handle_prediction('apple', predict_apple)

@prediction_bp.route('/potato-predict', methods=['POST'])
@login_required
@has_credits
def potato_predict():
    """Predict potato disease"""
    return handle_prediction('potato', predict_potato)

@prediction_bp.route('/rice-predict', methods=['POST'])
@login_required
@has_credits
def rice_predict():
    """Predict rice disease"""
    return handle_prediction('rice', predict_rice)

def handle_admin_prediction(plant_type):
    """Generic handler for admin batch predictions"""
    dir_pos = request.form.get('dir', '').strip()
    pred_val = request.form.get('val', type=int)
    
    if not dir_pos or pred_val is None:
        return "Invalid parameters", 400
    
    from app.ml.preprocessors import get_prediction_from_model
    from app.ml.model_loader import model_loader
    
    correct_predictions = 0
    total_files = 0
    
    try:
        for root, dirs, files in os.walk(dir_pos):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    file_path = os.path.join(root, file)
                    try:
                        result = predict_admin(file_path, plant_type)
                        total_files += 1
                        if result == pred_val:
                            correct_predictions += 1
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        
        accuracy = correct_predictions / total_files if total_files > 0 else 0
        
        return render_template(
            'show_result.html',
            dir_name=dir_pos,
            disease_name=pred_val,
            acc=accuracy
        )
    
    except Exception as e:
        return f"Error processing directory: {str(e)}", 500

@prediction_bp.route('/tomato-predict-admin', methods=['POST'])
@admin_required
def tomato_predict_admin():
    """Admin batch prediction for tomato"""
    return handle_admin_prediction('tomato')

@prediction_bp.route('/apple-predict-admin', methods=['POST'])
@admin_required
def apple_predict_admin():
    """Admin batch prediction for apple"""
    return handle_admin_prediction('apple')

@prediction_bp.route('/potato-predict-admin', methods=['POST'])
@admin_required
def potato_predict_admin():
    """Admin batch prediction for potato"""
    return handle_admin_prediction('potato')

@prediction_bp.route('/rice-predict-admin', methods=['POST'])
@admin_required
def rice_predict_admin():
    """Admin batch prediction for rice"""
    return handle_admin_prediction('rice')
