from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Access variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
TEXT_FOLDER = os.getenv("TEXT_FOLDER", "processed")


def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key_123" 

    # Import and register the Blueprint
    from app.routes import main
    app.register_blueprint(main)
    

    return app