from typing import AnyStr

from TestGraphGenerator.Models import Node, Relationship
from TestGraphGenerator.Models.Tranformations import node_query, relationship_nodes_query, relationship_query


def create_node_query(node: Node) -> AnyStr:
    return f"MERGE {node_query(node)}"


def delete_node_query(node: Node) -> AnyStr:
    return f"MATCH {node_query(node, 'n')} DELETE n"


def create_relationship_query(rel: Relationship) -> AnyStr:
    return f"MATCH {relationship_nodes_query(rel)} MERGE {relationship_query(rel)}"


def delete_relationship_query(rel: Relationship) -> AnyStr:
    return f"MATCH {relationship_nodes_query(rel)} {relationship_query(rel)} DELETE r"
