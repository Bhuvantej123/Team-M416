from flask import Flask



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key_123" 

    # Import and register the Blueprint
    from app.routes import main
    app.register_blueprint(main)
    

    return app