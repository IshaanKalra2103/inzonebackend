from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_cors import CORS

cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:3000"}})

def create_app():
    
    app.config['SECRET_KEY'] = 'INZONE1234'
    
    from .userAPI import userAPI
    app.register_blueprint(userAPI, url_prefix="")

    return app

    
    