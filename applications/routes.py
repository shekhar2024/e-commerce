from flask import current_app as app, request, jsonify
from applications.database import db
from applications.models import User, Item, Category, Cart, CartItem
from flask_jwt_extended import jwt_required

@app.route('/api/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200