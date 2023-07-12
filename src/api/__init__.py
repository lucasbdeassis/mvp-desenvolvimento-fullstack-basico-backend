from flask import Flask
from flask_cors import CORS

from src.api.spec import config_spec
from src.api.transaction_controller import transaction_controller


def create_app():
    app = Flask(__name__)

    app.register_blueprint(transaction_controller)
    config_spec(app)

    CORS(app)

    return app
