from itertools import chain
from typing import AnyStr, Dict, Optional, List

import neo4j

from DbInterface.Neo4jStream import Neo4jStream
from TestGraphGenerator.Models import Node, Relationship
from TestGraphGenerator.Models.Database import Database
from TestGraphGenerator.Models.Graph import Graph


def delete_database_neo4j(stream: Neo4jStream):
    """
    Deletes a neo4j database
    WARNING! THIS WILL DELETE THE DATABASE IN NEO4J PERMANENTLY
    :param stream:
    :return:
    """
    stream.write("MATCH (n) DETACH DELETE n")


def import_neo4j_database(stream: Neo4jStream, name: AnyStr) -> Database:
    """
    Loads a graph from neo4j as a python object
    :param stream: the neo4j interface to load from
    :param name: the name of the database
    :return: the database object
    """
    nodes = [Node(result.labels[0], result.items()) for result in stream.read("MATCH (n) RETURN n")]
    nodes_by_ids = {node.node_id: node for node in nodes}
    relationships = import_relationships_neo4j(stream, nodes_by_ids)
    return Database(Graph(nodes, relationships), name)


def import_relationships_neo4j(stream: Neo4jStream, nodes_by_id: Dict[AnyStr, Node]) -> List[Relationship]:
    """
    Loads all relationships from a neo4j result
    :param stream: the neo4j stream to load the relationships from
    :param nodes_by_id: a dict containing nodes mapped by their internal id
    :return: the relationships
    """
    query_result = stream.read("MATCH (n)-[r]-(m) RETURN n, r, m")
    relationships_raw = {result for result in chain.from_iterable(query_result)
                         if isinstance(result, neo4j.types.graph.Relationship)}
    relationships = []
    for relationship in relationships_raw:
        node_a, node_b = relationship.nodes
        new_relationship = Relationship(nodes_by_id[node_a["node_id"]], str(relationship.type),
                                        nodes_by_id[node_b["node_id"]])
        relationships.append(new_relationship)
    return relationships


def import_database_json(database_raw: Dict) -> Database:
    """
    Loads a database from a json object to a python one
    :param database_raw: the database json
    :return: the database object
    """
    return Database(import_graph_json(database_raw["graph"]), database_raw["name"])


def import_node_json(node_raw: Dict) -> Node:
    """
    Loads a node from raw json
    :param node_raw: the json to load from
    :return: the node object
    """
    return Node(node_raw["node_type"], node_raw["properties"])


def import_relationship_json(relationship_raw: Dict, nodes: Dict[AnyStr, Node]) -> Relationship:
    """
    Loads a relationship from a json
    :param relationship_raw: the relationship to load
    :param nodes: a dict containing all the nodes by id to load the correct nodes
    :return: the relationship object
    """
    return Relationship(nodes[relationship_raw["node_a"]], relationship_raw["relationship_type"],
                        nodes[relationship_raw["node_b"]])


def import_graph_json(graph_raw: Dict) -> Optional[Graph]:
    """
    Loads a graph object from a json object
    :param graph_raw: the graph to load
    :return: the graph object
    """
    try:
        graph = Graph()
        graph.nodes = [import_node_json(node_raw) for node_raw in graph_raw["nodes"]]
        nodes_by_ids = {node.node_id: node for node in graph.nodes}
        graph.relationships = [import_relationship_json(rel_raw, nodes_by_ids) for rel_raw in
                               graph_raw["relationships"]]
        return graph
    except KeyError as e:
        raise ValueError(f"Failed loading graph with error {e}")
