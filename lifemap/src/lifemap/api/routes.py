from flask import Blueprint, jsonify, request
from lifemap.models.node import Node
from lifemap.models.relationship import Relationship
from lifemap.data.storage import Storage

api = Blueprint('api', __name__)
storage = Storage()

@api.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = storage.load_nodes()
    return jsonify(nodes), 200

@api.route('/nodes', methods=['POST'])
def create_node():
    data = request.json
    node = Node(id=data['id'], label=data['label'], type=data['type'])
    storage.save_node(node)
    return jsonify(node), 201

@api.route('/relationships', methods=['GET'])
def get_relationships():
    relationships = storage.load_relationships()
    return jsonify(relationships), 200

@api.route('/relationships', methods=['POST'])
def create_relationship():
    data = request.json
    relationship = Relationship(source_node=data['source_node'], target_node=data['target_node'], strength=data['strength'])
    storage.save_relationship(relationship)
    return jsonify(relationship), 201