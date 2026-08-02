class Node:
    def __init__(self, node_id, label, node_type):
        self.id = node_id
        self.label = label
        self.type = node_type

    def update_label(self, new_label):
        self.label = new_label

    def update_type(self, new_type):
        self.type = new_type

    def __repr__(self):
        return f"Node(id={self.id}, label={self.label}, type={self.type})"