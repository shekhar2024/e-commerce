from flask_restful import Resource, Api, reqparse
from .models import *
from .utils import *
from flask_jwt_extended import jwt_required

api = Api()

class CategoryResource(Resource):

    @jwt_required()
    def get(self):
        categories_json = []

        categories = Category.query.all()

        for category in categories:
            category_json = category.to_dict()
            categories_json.append(category_json)

        if categories_json:
            return categories_json

        return {'message': 'No categories found'}, 404

    @jwt_required()
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the category is required')
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        if args['name'] == "":
            return {'message': 'Name of the category is required'}, 400

        new_cat = Category(name=args['name'], description=args['description'])
        db.session.add(new_cat)
        db.session.commit()
        return {'message': 'Category created successfully', 'category': new_cat.to_dict()}, 201

    @jwt_required()
    @admin_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the category is required')
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        if args['name'] == "":
            return {'message': 'Name of the category is required'}, 400

        category = Category.query.get(id)
        if not category:
            return {'message': 'Category not found'}, 404

        category.name = args['name']
        category.description = args['description']
        db.session.commit()

        return {'message': 'Category updated successfully', 'subject': category.to_dict()}
    
    @jwt_required()
    @admin_required
    def delete(self, id):
        cat = Category.query.get(id)
        if not cat:
            return {'message': 'Category not found'}, 404

        db.session.delete(cat)
        db.session.commit()

        return {'message': 'Category deleted successfully'}
    
class ItemResource(Resource):

    @jwt_required()
    def get(self):
        items_json = []

        items = Item.query.all()

        for item in items:
            item_json = item.to_dict()
            items_json.append(item_json)

        if items_json:
            return items_json

        return {'message': 'No items found'}, 404

    @jwt_required()
    @admin_required
    def post(self, cat_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the item is required')
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float, required=True, help='Price of the item is required')
        parser.add_argument('stock', type=int, required=True, help='Stock of the item is required')
        args = parser.parse_args()

        if args['name'] == "":
            return {'message': 'Name of the item is required'}, 400

        if args['price'] is None or args['price'] < 0:
            return {'message': 'Valid price of the item is required'}, 400

        if args['stock'] is None or args['stock'] < 0:
            return {'message': 'Valid stock of the item is required'}, 400

        category = Category.query.get(cat_id)
        if not category:
            return {'message': 'Category not found'}, 404

        new_item = Item(
            category_id=cat_id,
            name=args['name'],
            description=args['description'],
            price=args['price'],
            stock=args['stock']
        )
        db.session.add(new_item)
        db.session.commit()
        return {'message': 'Item created successfully', 'item': new_item.to_dict()}, 201

    @jwt_required()
    @admin_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the item is required')
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float, required=True, help='Price of the item is required')
        parser.add_argument('stock', type=int, required=True, help='Stock of the item is required')

        args = parser.parse_args()

        if args['name'] == "":
            return {'message': 'Name of the item is required'}, 400
        
        if args['price'] is None or args['price'] < 0:
            return {'message': 'Valid price of the item is required'}, 400
        
        if args['stock'] is None or args['stock'] < 0:
            return {'message': 'Valid stock of the item is required'}, 400
        
        item = Item.query.get(id)

        if not item:
            return {'message': 'Item not found'}, 404
        
        item.name = args['name']
        item.description = args['description']
        item.price = args['price']
        item.stock = args['stock']

        db.session.commit()

        return {'message': 'Item updated successfully', 'item': item.to_dict()}
    
    @jwt_required()
    @admin_required
    def delete(self, id):
        item = Item.query.get(id)
        if not item:
            return {'message': 'Item not found'}, 404

        db.session.delete(item)
        db.session.commit()

        return {'message': 'Item deleted successfully'} 
    
api.add_resource(CategoryResource, '/api/categories', '/api/categories/<int:id>')
api.add_resource(ItemResource, '/api/items', '/api/items/<int:id>')
