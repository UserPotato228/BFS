from flask import Blueprint

bp = Blueprint("folder", __name__)
from app.folder import routes