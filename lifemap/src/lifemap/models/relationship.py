class Relationship:
    def __init__(self, source_node, target_node, strength=1):
        self.source_node = source_node
        self.target_node = target_node
        self.strength = strength

    def update_strength(self, new_strength):
        self.strength = new_strength

    def __repr__(self):
        return f"Relationship({self.source_node} -> {self.target_node}, strength={self.strength})"