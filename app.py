#!/usr/bin/env python
"""REST API"""

from flask import Flask, request, jsonify, abort
from config import Config
from models import db, Item

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or not 'name' in data:
        abort(400, description=data.get('description'))
    item = Item(name=data['name'], description=data.get('description'))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    if not data or not 'name' in data:
        abort(400, description='Name is required')
    item.name = data['name']
    item.description = data.get('description')
    db.session.commit()
    return jsonify(item.to_dict()), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204 
    
if __name__ == '__main__':
    app.run(debug=True)