from flask import Flask
from flask.ext.restful import Api

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, course, student, user, admin

