from typing import AnyStr

from TestGraphGenerator.Models import Node, Relationship


def relationship_query(rel: Relationship, node_names: tuple = ("nodeA", "nodeB")) -> AnyStr:
    """
    Transforms a relationship object to a literal neo4j query of the same relationship
    without changing the original object
    IMPORTANT! this function only generates a partial query string and shouldn't be used alone
    :param rel: the relationship to transform
    :param node_names: the names of the nodes in the query. useful for multi query strings
    :return: a string of the query
    """
    node_a, node_b = node_names
    return f"({node_a})-[r:{rel.relationship_type}]-({node_b})"


def relationship_nodes_query(rel, node_names: tuple = ("nodeA", "nodeB")) -> AnyStr:
    """
    Generates a query representation of the nodes in a relationship
    :param rel: the relationship to transform
    :param node_names: the name of the nodes in the query. useful for multi query strings
    :return: a string of the query
    """
    node_a, node_b = node_names
    return f"{node_query(rel.node_a, node_a)}, {node_query(rel.node_b, node_b)}"


def generate_properties(node: Node) -> AnyStr:
    """
    Generates a neo4j properties of a node transforms the properties dict from {"key": "value"} to {key: 'value'}
    :param node: the node to transform
    :return: the properties as a neo4j query string
    """
    properties = "{"
    if not node.properties:
        raise ValueError("Missing node properties")
    for key, value in node.properties.items():
        properties += f"{key}: '{value}', "
    properties = properties[:-2]
    properties += "}"
    return properties


def node_query(node: Node, node_name="n") -> AnyStr:
    """
    Creates a query representation of a single node
    :param node: the node to transform
    :param node_name: the name of the node in the query. useful for multi query strings
    :return: a string of the query
    """
    return f"({node_name}:{node.node_type} {generate_properties(node)})"
