from flask import Flask, render_template, jsonify
from lifemap.graph.engine import GraphEngine

app = Flask(__name__)
graph_engine = GraphEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    nodes = graph_engine.get_nodes()
    return jsonify(nodes)

@app.route('/api/relationships', methods=['GET'])
def get_relationships():
    relationships = graph_engine.get_relationships()
    return jsonify(relationships)

@app.route('/api/add_node', methods=['POST'])
def add_node():
    # Logic to add a node
    pass

@app.route('/api/add_relationship', methods=['POST'])
def add_relationship():
    # Logic to add a relationship
    pass

if __name__ == '__main__':
    app.run(debug=True)