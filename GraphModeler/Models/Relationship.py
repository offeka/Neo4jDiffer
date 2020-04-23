from dataclasses import dataclass, field
from typing import AnyStr, Dict
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
    properties: Dict[AnyStr, AnyStr] = field(default_factory=dict)

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __eq__(self, other):
        return self.relationship_type == other.relationship_type \
               and self.node_a == other.node_a \
               and self.node_b == other.node_b

    def __hash__(self):
        return hash((self.relationship_type, self.node_a, self.node_b))
