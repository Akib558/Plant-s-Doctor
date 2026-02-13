from app.ml.model_loader import model_loader
from app.ml.preprocessors import error_model_predict, get_prediction_from_model

TOMATO_DISEASES = {
    0: "The Disease is Tomato_Bacterial_Spot",
    1: "The Disease is Tomato_Early_Blight",
    2: "The Disease is Tomato_Late_Blight",
    3: "The Disease is Tomato_Leaf_Mold",
    4: "The Disease is Tomato_Septoria_leaf",
    5: "The Disease is Tomato_Two_spotted_spider_mite",
    6: "The Disease is Tomato_Target_Spot",
    7: "The Disease is Tomato_YellowLeaf_Curl_virus",
    8: "The Disease is Tomato_Mossaic_virus",
    9: "Great....!!! Tomato is Healthy !!!"
}

APPLE_DISEASES = {
    0: "Apple has 'Apple-Scab Disease'",
    1: "Apple has 'Apple-Black-rot Disease'",
    2: "Apple has 'Cedar-Apple-rust Disease'",
    3: "Great !!! Apple has no Disease.. Healthy !!! ... "
}

POTATO_DISEASES = {
    0: "Potato has 'Potato Early-Blight Disease'",
    1: "Great !!! Potato is Healthy !",
    2: "Potato has 'Potato Late-Blight Disease'"
}

RICE_DISEASES = {
    0: "The disease is 'Brown Spot'",
    1: "Rice is Healthy !!!!",
    2: "The disease is 'Hispa'",
    3: "The disease is 'Leaf Blast'"
}

def predict_tomato(img_path):
    """Predict tomato disease"""
    error_model_2 = model_loader.get_error_model_2()
    val = error_model_predict(img_path, error_model_2)
    
    if val == 2:
        model = model_loader.get_tomato_model()
        pred_idx = get_prediction_from_model(img_path, model, (224, 224))
        return TOMATO_DISEASES.get(pred_idx, "Unknown disease")
    else:
        return "Wrong Picture....Not tomato"

def predict_apple(img_path):
    """Predict apple disease"""
    error_model_2 = model_loader.get_error_model_2()
    val = error_model_predict(img_path, error_model_2)
    
    if val == 0:
        model = model_loader.get_apple_model()
        pred_idx = get_prediction_from_model(img_path, model, (256, 256))
        return APPLE_DISEASES.get(pred_idx, "Unknown disease")
    else:
        return "Wrong..... This is not apple"

def predict_potato(img_path):
    """Predict potato disease"""
    error_model_2 = model_loader.get_error_model_2()
    val = error_model_predict(img_path, error_model_2)
    
    if val == 1:
        model = model_loader.get_potato_model()
        pred_idx = get_prediction_from_model(img_path, model, (256, 256))
        return POTATO_DISEASES.get(pred_idx, "Unknown disease")
    else:
        return "Wrong.....This is not potato"

def predict_rice(img_path):
    """Predict rice disease"""
    error_model = model_loader.get_error_model()
    val = error_model_predict(img_path, error_model)
    
    if val == 2:
        model = model_loader.get_rice_model()
        pred_idx = get_prediction_from_model(img_path, model, (1282, 1282))
        return RICE_DISEASES.get(pred_idx, "Unknown disease")
    else:
        return "Wrong.....This is not Rice"

def predict_admin(img_path, plant_type):
    """Admin prediction without error checking"""
    model_map = {
        'tomato': (model_loader.get_tomato_model(), (224, 224)),
        'apple': (model_loader.get_apple_model(), (256, 256)),
        'potato': (model_loader.get_potato_model(), (256, 256)),
        'rice': (model_loader.get_rice_model(), (1282, 1282))
    }
    
    if plant_type not in model_map:
        return None
    
    model, target_size = model_map[plant_type]
    pred_idx = get_prediction_from_model(img_path, model, target_size)
    return pred_idx
