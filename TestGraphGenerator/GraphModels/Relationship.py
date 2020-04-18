from dataclasses import dataclass
from typing import AnyStr
from TestGraphGenerator.GraphModels.Node import Node


@dataclass
class Relationship:
    node_a: Node
    relationship_type: AnyStr
    node_b: Node

    def __post_init__(self):
        self.relationship_type = self.relationship_type.capitalize()

    def relationship_query(self) -> AnyStr:
        return self.__create_match_query() + f"MERGE (nodeA)-[r:{self.relationship_type}]-(nodeB)"

    def delete_relationship_query(self) -> AnyStr:
        return self.__create_match_query() + f"DELETE r"

    def __create_match_query(self) -> AnyStr:
        return f"MATCH {self.node_a.as_query('nodeA')}, {self.node_b.as_query('nodeB')} "
