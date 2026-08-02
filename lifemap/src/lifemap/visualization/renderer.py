from matplotlib import pyplot as plt
import networkx as nx

class GraphRenderer:
    def __init__(self, graph):
        self.graph = graph

    def draw_graph(self):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Life Map Visualization")
        plt.show()

    def update_graph(self, new_data):
        # Update the graph with new data
        for node in new_data['nodes']:
            self.graph.add_node(node['id'], label=node['label'], type=node['type'])
        for relationship in new_data['relationships']:
            self.graph.add_edge(relationship['source'], relationship['target'], strength=relationship['strength'])

        self.draw_graph()