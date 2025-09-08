from flask import current_app as app, request, jsonify, render_template
from applications.database import db
from applications.models import User, Item, Category, Cart, CartItem
from flask_jwt_extended import jwt_required
from .utils import *

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
