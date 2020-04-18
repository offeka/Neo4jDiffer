from dataclasses import dataclass, field
from typing import Dict, AnyStr


@dataclass
class Node:
    node_type: AnyStr
    properties: Dict[AnyStr, AnyStr] = None

    def __post_init__(self):
        if not self.properties:
            self.properties = {}
        self.node_type = self.node_type.capitalize()

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __eq__(self, other):
        return self.node_type == other.node_type and self.properties == other.properties

    def __generate_properties(self) -> AnyStr:
        properties = "{"
        if not self.properties:
            raise ValueError("Missing node properties")
        for key, value in self.properties.items():
            properties += f"{key}: '{value}', "
        properties = properties[:-2]
        properties += "}"
        return properties

    def as_query(self, node_name="n") -> AnyStr:
        return f"({node_name}:{self.node_type} {self.__generate_properties()})"
