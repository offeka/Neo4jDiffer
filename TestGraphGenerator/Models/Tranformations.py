from typing import AnyStr


def relationship_query(rel, node_names: tuple = ("nodeA", "nodeB")) -> AnyStr:
    node_a, node_b = node_names
    return f"({node_a})-[r:{rel.relationship_type}]-({node_b})"


def relationship_nodes_query(rel, node_names: tuple = ("nodeA", "nodeB")) -> AnyStr:
    node_a, node_b = node_names
    return f"{node_query(rel.node_a, node_a)}, {node_query(rel.node_b, node_b)}"


def generate_properties(node) -> AnyStr:
    properties = "{"
    if not node.properties:
        raise ValueError("Missing node properties")
    for key, value in node.properties.items():
        properties += f"{key}: '{value}', "
    properties = properties[:-2]
    properties += "}"
    return properties


def node_query(node, node_name="n") -> AnyStr:
    return f"({node_name}:{node.node_type} {generate_properties(node)})"
