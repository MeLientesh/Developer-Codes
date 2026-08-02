from typing import List, Tuple

class GraphLayout:
    def __init__(self, nodes: List[Tuple[int, str]], relationships: List[Tuple[int, int]]):
        self.nodes = nodes
        self.relationships = relationships

    def circular_layout(self):
        layout = {}
        num_nodes = len(self.nodes)
        for index, (node_id, label) in enumerate(self.nodes):
            angle = 2 * 3.14159 * index / num_nodes
            layout[node_id] = (cos(angle), sin(angle))
        return layout

    def hierarchical_layout(self):
        layout = {}
        levels = {}
        for node_id, label in self.nodes:
            level = self._determine_level(node_id)
            if level not in levels:
                levels[level] = []
            levels[level].append(node_id)

        for level, node_ids in levels.items():
            for index, node_id in enumerate(node_ids):
                layout[node_id] = (index, level)
        return layout

    def _determine_level(self, node_id: int) -> int:
        # Placeholder for logic to determine the level of a node
        return 0

    def update_layout(self, new_nodes: List[Tuple[int, str]], new_relationships: List[Tuple[int, int]]):
        self.nodes.extend(new_nodes)
        self.relationships.extend(new_relationships)
        # Recalculate layout if necessary
        return self.circular_layout()  # or self.hierarchical_layout() based on preference
