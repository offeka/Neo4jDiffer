from typing import AnyStr

from TestGraphGenerator.Models import Node
from TestGraphGenerator.Models.Tranformations import node_query


def create_node_query(node: Node) -> AnyStr:
    return f"MERGE {node_query(node)}"


def delete_node_query(node: Node) -> AnyStr:
    return f"MATCH {node_query(node, 'n')} DELETE n"
