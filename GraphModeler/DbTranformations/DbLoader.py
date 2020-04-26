from itertools import chain
from typing import AnyStr, Dict, Optional, List, Coroutine, Awaitable

import neo4j

from DbInterface.Neo4jStream import Neo4jStream
from DbInterface.Neo4jStreamAsync import Neo4jStreamAsync
from GraphModeler.Models import Node, Relationship
from GraphModeler.Models.Database import Database
from GraphModeler.Models.Graph import Graph


def import_neo4j_database(stream: Neo4jStream, name: AnyStr) -> Database:
    """
    Loads a graph from neo4j as a python object
    :param stream: the neo4j interface to load from
    :param name: the name of the database
    :return: the database object representing the neo4j graph
    """
    nodes = [import_node_neo4j(result) for result in stream.read("MATCH (n) RETURN n")]
    nodes_by_ids = {node.node_id: node for node in nodes}
    relationships = import_relationships_neo4j(stream, nodes_by_ids)
    return Database(Graph(nodes, relationships), name)


async def import_neo4j_database_async(stream: Neo4jStreamAsync, name: AnyStr) -> Database:
    """
    Imports a neo4j database in an async manner for performance
    :param stream: the neo4j stream
    :param name: the name of the database
    :return: the database object representing the neo4j graph
    """
    nodes = [import_node_neo4j(result) for result in await stream.read_async("MATCH (n) RETURN n")]
    nodes_index = nodes_by_ids_async(nodes)
    relationships = import_relationships_neo4j_async(stream, nodes_index)
    return Database(Graph(nodes, relationships), name)


async def nodes_by_ids_async(nodes: List[Node]) -> Dict[AnyStr, Node]:
    """
    Takes a list of nodes and indexes them by id
    :param nodes: the nodes to index
    :return: the index
    """
    return {node.node_id: node for node in nodes}


def import_relationships_neo4j_async(stream: Neo4jStreamAsync, nodes_by_id: Awaitable[Dict[AnyStr, Node]]) -> \
        List[Relationship]:
    """
    Loads relationships from neo4j graph into python object
    :param stream: the neo4j stream
    :param nodes_by_id: the nodes indexed by id
    :return: an Awaitable for the relationships
    """
    query_result = stream.read_async("MATCH (n)-[r]-(m) RETURN n, r, n")
    result_relationships = {result for result in chain.from_iterable(query_result)
                            if issubclass(type(result), neo4j.types.graph.Relationship)}
    nodes_index = await nodes_by_id
    relationships = []
    for relationship in result_relationships:
        relationships.append(import_neo4j_relationship(nodes_index, relationship))
    return relationships


def import_node_neo4j(result: neo4j.Record) -> Node:
    """
    Takes a neo4j result and converts it to a use able node object
    :param result: the neo4j result
    :return: the node created from the result
    """
    return Node(list(result[0].labels), {key: value for key, value in result[0].items()})


def import_relationships_neo4j(stream: Neo4jStream, nodes_by_id: Dict[AnyStr, Node]) -> List[Relationship]:
    """
    Loads all relationships from a neo4j result
    :param stream: the neo4j stream to load the relationships from
    :param nodes_by_id: a dict containing nodes mapped by their internal id
    :return: the relationships
    """
    query_result = stream.read("MATCH (n)-[r]-(m) RETURN n, r, m")
    relationships_raw = {result for result in chain.from_iterable(query_result)
                         if isinstance(result, neo4j.Relationship)}
    relationships = []
    for relationship in relationships_raw:
        new_relationship = import_neo4j_relationship(nodes_by_id, relationship)
        relationships.append(new_relationship)
    return relationships


def import_neo4j_relationship(nodes_by_id: Dict[AnyStr, Node], relationship_record: neo4j.Relationship) -> Relationship:
    """
    Imports a neo4j relationship record to a loader relationship type
    :param nodes_by_id: the nodes index
    :param relationship_record: the record from neo4j
    :return: the new relationship
    """
    node_a, node_b = relationship_record.nodes
    new_relationship = Relationship(nodes_by_id[node_a["node_id"]], str(relationship_record.type),
                                    nodes_by_id[node_b["node_id"]],
                                    {key: value for key, value in relationship_record.items()})
    return new_relationship


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
    return Node(node_raw["node_types"], node_raw["properties"])


def import_relationship_json(relationship_raw: Dict, nodes: Dict[AnyStr, Node]) -> Relationship:
    """
    Loads a relationship from a json
    :param relationship_raw: the relationship to load
    :param nodes: a dict containing all the nodes by id to load the correct nodes
    :return: the relationship object
    """
    return Relationship(nodes[relationship_raw["node_a"]], relationship_raw["relationship_type"],
                        nodes[relationship_raw["node_b"]], relationship_raw["properties"])


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
        raise ValueError(f"Failed loading graph with error cannot find key {e}")
