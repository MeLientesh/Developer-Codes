class GraphEngine:
    def __init__(self):
        self.nodes = {}
        self.relationships = {}

    def add_node(self, node_id, label, node_type):
        if node_id not in self.nodes:
            self.nodes[node_id] = {'label': label, 'type': node_type}
        else:
            raise ValueError("Node with this ID already exists.")

    def update_node(self, node_id, label=None, node_type=None):
        if node_id in self.nodes:
            if label is not None:
                self.nodes[node_id]['label'] = label
            if node_type is not None:
                self.nodes[node_id]['type'] = node_type
        else:
            raise ValueError("Node not found.")

    def add_relationship(self, source_id, target_id, strength):
        if source_id in self.nodes and target_id in self.nodes:
            relationship_id = f"{source_id}->{target_id}"
            self.relationships[relationship_id] = {'source': source_id, 'target': target_id, 'strength': strength}
        else:
            raise ValueError("One or both nodes not found.")

    def update_relationship(self, source_id, target_id, strength):
        relationship_id = f"{source_id}->{target_id}"
        if relationship_id in self.relationships:
            self.relationships[relationship_id]['strength'] = strength
        else:
            raise ValueError("Relationship not found.")

    def get_graph_data(self):
        return {
            'nodes': self.nodes,
            'relationships': self.relationships
        }