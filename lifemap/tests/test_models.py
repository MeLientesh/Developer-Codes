import unittest
from lifemap.models.node import Node
from lifemap.models.relationship import Relationship

class TestNode(unittest.TestCase):
    def setUp(self):
        self.node = Node(id=1, label="Skill", type="Knowledge")

    def test_node_initialization(self):
        self.assertEqual(self.node.id, 1)
        self.assertEqual(self.node.label, "Skill")
        self.assertEqual(self.node.type, "Knowledge")

    def test_update_node(self):
        self.node.label = "Updated Skill"
        self.assertEqual(self.node.label, "Updated Skill")

class TestRelationship(unittest.TestCase):
    def setUp(self):
        self.source_node = Node(id=1, label="Skill", type="Knowledge")
        self.target_node = Node(id=2, label="Goal", type="Aspirations")
        self.relationship = Relationship(source_node=self.source_node, target_node=self.target_node, strength=5)

    def test_relationship_initialization(self):
        self.assertEqual(self.relationship.source_node, self.source_node)
        self.assertEqual(self.relationship.target_node, self.target_node)
        self.assertEqual(self.relationship.strength, 5)

    def test_update_relationship_strength(self):
        self.relationship.strength = 10
        self.assertEqual(self.relationship.strength, 10)

if __name__ == '__main__':
    unittest.main()