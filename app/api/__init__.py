from flask import Blueprint

blueprint = Blueprint('api', __name__)

from app.api import api_routes

