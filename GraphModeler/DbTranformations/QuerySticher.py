from typing import AnyStr

from GraphModeler.Models import Node, Relationship
from GraphModeler.Models.QueryConverter import node_query, relationship_nodes_query, relationship_query, \
    generate_properties


def create_node_query(node: Node) -> AnyStr:
    """
    Takes a node and convert it to a query for generating a node in neo4j
    :param node: the node to convert
    :return: the query string for creating the node
    """
    return f"MERGE {node_query(node)}"


def delete_node_query(node: Node) -> AnyStr:
    """
    Takes a node and converts it to a query to delete it in neo4j
    :param node: the node to delete
    :return: the query string for deleting the node
    """
    return f"MATCH {node_query(node, 'n')} DETACH DELETE n"


def create_relationship_query(rel: Relationship) -> AnyStr:
    """
    Takes a relationship and converts it to a neo4j query representing the same
    :param rel: the relationship to convert
    :return: the query string for creating the relationship
    """
    return f"MATCH {relationship_nodes_query(rel)} MERGE {relationship_query(rel)}"


def delete_relationship_query(rel: Relationship) -> AnyStr:
    """
    Takes a relationship and converts it to a neo4j query deleting it
    :param rel: the relationship to delete
    :return: the query string for deleting the relationship
    """
    return f"MATCH ({node_query(rel.node_a, 'a')})-[r:{rel.relationship_type} {generate_properties(rel)}]-({node_query(rel.node_b, 'b')}) DELETE r"

