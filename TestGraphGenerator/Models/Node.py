from dataclasses import dataclass, field
from typing import Dict, AnyStr


@dataclass
class Node:
    """
    A neo4j node
    sometimes called an edge
    """
    node_type: AnyStr
    properties: Dict[AnyStr, AnyStr] = None

    def __post_init__(self):
        if not self.properties:
            self.properties = {}

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __eq__(self, other):
        return self.node_type == other.node_type and self.properties == other.properties
