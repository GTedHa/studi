from flask import request, jsonify, Response
from flask_restful import Api, Resource

from studi import app

api = Api(app)
