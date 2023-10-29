#!/usr/bin/python3
""" a module for app entry """
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
# Configure CORS to allow specific origins
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ teardown api"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """ a function that display an error page"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    if getenv('HBNB_API_HOST') or getenv('HBNB_API_PORT'):
        local = getenv('HBNB_API_HOST')
        ports = getenv('HBNB_API_PORT')
    else:
        ports = 5000
        local = '0.0.0.0'
    app.run(host=local, port=ports, threaded=True)
