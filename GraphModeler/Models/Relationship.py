from dataclasses import dataclass
from typing import AnyStr
from GraphModeler.Models.Node import Node


@dataclass
class Relationship:
    """
    A neo4j relationship between 2 nodes
    sometimes called a vertex
    """
    node_a: Node
    relationship_type: AnyStr
    node_b: Node

    def __getitem__(self, item):
        return (self.node_a, self.node_b)[item]

    def __eq__(self, other):
        return self.relationship_type == other.relationship_type \
               and self.node_a == other.node_a \
               and self.node_b == other.node_b
