import unittest
from lifemap.graph.engine import GraphEngine
from lifemap.models.node import Node
from lifemap.models.relationship import Relationship

class TestGraphEngine(unittest.TestCase):

    def setUp(self):
        self.graph_engine = GraphEngine()
        self.node1 = Node(id=1, label='Knowledge', type='skill')
        self.node2 = Node(id=2, label='Goal', type='aspiration')
        self.graph_engine.add_node(self.node1)
        self.graph_engine.add_node(self.node2)

    def test_add_node(self):
        self.assertIn(self.node1, self.graph_engine.nodes)
        self.assertIn(self.node2, self.graph_engine.nodes)

    def test_add_relationship(self):
        relationship = Relationship(source_node=self.node1, target_node=self.node2, strength=5)
        self.graph_engine.add_relationship(relationship)
        self.assertIn(relationship, self.graph_engine.relationships)

    def test_update_node(self):
        self.node1.label = 'Updated Knowledge'
        self.graph_engine.update_node(self.node1)
        updated_node = self.graph_engine.get_node(self.node1.id)
        self.assertEqual(updated_node.label, 'Updated Knowledge')

    def test_dynamic_graph_update(self):
        self.graph_engine.update_graph()
        self.assertTrue(self.graph_engine.is_updated)

if __name__ == '__main__':
    unittest.main()