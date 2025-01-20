from flask import jsonify, request, Blueprint
from models import db, Items

Items_bp = Blueprint('Items_bp', __name__)
# create
@Items_bp.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Items(name=data["name"], description=data["description"], price=data["price"])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@Items_bp.route('/items', methods=['GET'])
def get_items():
    items = Items.query.all()
    return jsonify([item.to_dict() for item in items]), 200

#update
@Items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Items.query.get(item_id)
    if item:
        data = request.json
        for key, value in data.items():
            setattr(item, key, value)
            db.session.commit()
            return jsonify(item.to_dict()), 200
        
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"error": "Item not found"}), 404

#delete
@Items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Items.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404
