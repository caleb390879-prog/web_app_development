from flask import Flask
from .routes.recipe import recipe_bp
import os

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-for-local')
    
    # 註冊 Blueprints
    app.register_blueprint(recipe_bp)
    
    return app
