from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, posts, gets, article, forms, applicants
