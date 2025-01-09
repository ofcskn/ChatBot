from flask import Flask

def create_app():
    """
    Factory to create a Flask app.
    """
    app = Flask(__name__)
    from app.routes import bp
    app.register_blueprint(bp)
    return app