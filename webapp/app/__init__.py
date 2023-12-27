from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
import time
from prometheus_flask_exporter import PrometheusMetrics
from .routes import configure_routes
from .config import Config


mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/myDatabase")
    #app.config.from_object(Config)
    mongo.init_app(app)
    print("Mongo initialized:", 'pymongo' in app.extensions)
    #print("App created, mongo initialized", mongo.db.command('ismaster'))
    metrics = PrometheusMetrics(app)  
    configure_routes(app)
    return app
