from tensorflow.keras.models import load_model
from flask import current_app

class ModelLoader:
    """Singleton class for lazy loading ML models"""
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def get_model(self, model_name):
        """Load and cache model on first access"""
        if model_name not in self._models:
            model_path = current_app.config.get(f'MODEL_PATH_{model_name.upper()}')
            if model_path:
                print(f"Loading model: {model_name}")
                self._models[model_name] = load_model(model_path)
            else:
                raise ValueError(f"Model path not configured for: {model_name}")
        return self._models[model_name]
    
    def get_tomato_model(self):
        return self.get_model('tomato')
    
    def get_apple_model(self):
        return self.get_model('apple')
    
    def get_potato_model(self):
        return self.get_model('potato')
    
    def get_rice_model(self):
        return self.get_model('rice')
    
    def get_error_model(self):
        return self.get_model('error')
    
    def get_error_model_2(self):
        return self.get_model('error_2')

model_loader = ModelLoader()
