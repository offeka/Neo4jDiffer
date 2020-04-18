from dataclasses import dataclass, field
from typing import Dict, AnyStr

from TestGraphGenerator.GraphModels.BaseModels.BaseDbItem import BaseDbItem


@dataclass
class Node(BaseDbItem):
    node_type: AnyStr
    properties: Dict[AnyStr, AnyStr] = field(init=False)

    def __post_init__(self):
        self.properties = {}
        self.node_type = self.node_type.capitalize()

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def generate_query_str(self) -> AnyStr:
        properties = "{"
        if not self.properties:
            raise ValueError("Missing node properties")
        for key, value in self.properties.items():
            properties += f"{key}: '{value}', "
        properties = properties[:-2]
        properties += "}"
        return f"MERGE (p:{self.node_type} {properties})"


