from typing import AnyStr, Tuple, Dict, Optional, Iterable

from DbInterface.Neo4jWriter import Neo4jWriter
from TestGraphGenerator.Models import Node, Relationship, relationship_query
from TestGraphGenerator.Models.Database import Database
from TestGraphGenerator.Models.Graph import Graph
from TestGraphGenerator.QuerySticher import create_node_query


def load_db(database: Database, writer: Neo4jWriter) -> None:
    """
    Loads a database from an object into neo4j
    :param database: the database to load
    :param writer: the neo4j interface to use
    """
    writer.write(f"CREATE OR REPLACE DATABASE {database.name}")


def flush_nodes_to_graph(nodes: Iterable[Node], writer: Neo4jWriter) -> None:
    """
    Creates a list of nodes in the neo4j graph.
    :param nodes: the nodes to create in the db
    :param writer: a neo4j interface to send queries to
    """
    for node in nodes:
        writer.write(create_node_query(node))


def flush_relationships_to_graph(relationships: Iterable[Relationship], writer: Neo4jWriter) -> None:
    """
    Writes relationships to the neo4j database.
    :param relationships: the relationships to create in the db
    :param writer: a neo4j interface to send queries to
    """
    for relationship in relationships:
        writer.write(relationship_query(relationship))


def load_node(node_raw: Tuple[AnyStr, Dict]) -> Node:
    """
    Loads a node from raw json
    :param node_raw: the json to load from
    :return: the node object
    """
    node_id, node_data = node_raw
    return Node(node_data["node_type"], node_data["properties"], node_id)


def load_relationship(relationship_raw: Dict, nodes: Dict[AnyStr, Node]) -> Relationship:
    """
    Loads a relationship from a json
    :param relationship_raw: the relationship to load
    :param nodes: a dict containing all the nodes by id to load the correct nodes
    :return: the relationship object
    """
    return Relationship(nodes[relationship_raw["node_a"]], relationship_raw["relationship_type"],
                        nodes[relationship_raw["node_b"]])


def load_graph(graph_raw: Dict) -> Optional[Graph]:
    """
    Loads a graph object from a json object
    :param graph_raw: the graph to load
    :return: the graph object
    """
    try:
        graph = Graph()
        graph.nodes = [load_node(node_raw) for node_raw in graph_raw["nodes"].items()]
        nodes_by_ids = {node.node_id: node for node in graph.nodes}
        graph.relationships = [load_relationship(rel_raw, nodes_by_ids) for rel_raw in graph_raw["relationships"]]
        return graph
    except KeyError as e:
        raise ValueError(f"Failed loading graph with error {e}")
