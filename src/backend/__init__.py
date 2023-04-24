from amazon import AmazonService
from flask import Flask,Blueprint
from flask_cors import CORS
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    CORS(app)
    api_blueprint = Blueprint('api',__name__)
    CORS(api_blueprint)
    api = Api(api_blueprint)
    CORS(api.app)
    api.add_resource(AmazonService,'/amazon/<url>')
    app.register_blueprint(api_blueprint)
    return app


