from dataclasses import dataclass
from typing import AnyStr

from TestGraphGenerator.GraphModels.BaseModels.BaseDbItem import BaseDbItem
from TestGraphGenerator.GraphModels.BaseModels.Node import Node


@dataclass
class BaseRelationship(BaseDbItem):
    node_a: Node
    relationship_type: AnyStr
    node_b: Node

    def generate_query_str(self) -> AnyStr:
        return f"MATCH (NodeA:{self.node_a.node_type} )"
