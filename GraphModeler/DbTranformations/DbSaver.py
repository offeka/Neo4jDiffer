import asyncio
from typing import Dict, Iterable, List, Any, Callable, AnyStr

from DbInterface import Neo4jStream
from DbInterface.Neo4jStreamAsync import Neo4jStreamAsync
from GraphModeler.DbTranformations.QuerySticher import create_node_query, create_relationship_query

from GraphModeler.Models import Node, Relationship
from GraphModeler.Models.Database import Database
from GraphModeler.Models.Graph import Graph


def chunks(chunks_source, chunk_size):
    """
    Splits a list into even sized chunks
    :param chunks_source: the list to split
    :param chunk_size: the chunk size
    :return: an iterable of chunks
    """
    for i in range(0, len(chunks_source), chunk_size):
        yield chunks_source[i:i + chunk_size]


def export_node_json(node: Node) -> Dict:
    """
    Converts a node to json for serialization
    :param node: the node to convert
    :return: a dict representing the node
    """
    return {"node_types": node.node_types, "properties": node.properties}


def export_relationship_json(rel: Relationship) -> Dict:
    """
    Converts a relationship to json using the nodes ids
    :param rel: the relationship to convert
    :return: a dict representing the relationship
    """
    return {"node_a": rel.node_a.node_id, "relationship_type": rel.relationship_type, "node_b": rel.node_b.node_id,
            "properties": rel.properties}


def export_graph_json(graph: Graph) -> Dict:
    """
    Converts a graph to json
    :param graph: the graph to serialize
    :return: a dict representing the graph
    """
    return {"nodes": [export_node_json(node) for node in graph.nodes],
            "relationships": [export_relationship_json(rel) for rel in graph.relationships]}


def export_database_json(database: Database) -> Dict:
    """
    Converts a database to json for saving and loading.
    This is not a replacement for neo4j dump feature this is used in context of a single db.
    For example to use :dbs in neo4j and load different ones in the same instance.
    :param database:
    :return: a dict representing the database
    """
    return {"name": database.name, "graph": export_graph_json(database.graph)}


def export_database_neo4j(database: Database, stream: Neo4jStream, commit_size: int) -> None:
    """
    Loads a database from an object into neo4j
    :param database: the database to load
    :param stream: the neo4j interface to use
    :param commit_size: how many nodes or relationships to write to the database before commiting
    """
    export_objects_to_graph(database.graph.nodes, stream, commit_size, create_node_query)
    export_objects_to_graph(database.graph.relationships, stream, commit_size, create_relationship_query)


async def export_database_neo4j_async(database: Database, stream: Neo4jStreamAsync, commit_size: int) -> None:
    """
    Exports a database object to neo4j in an async manner
    :param database: the database to export
    :param stream: the stream to export to
    :param commit_size: the size of each commit to the database
    """
    await export_objects_to_graph_async(database.graph.nodes, stream, commit_size, create_node_query)
    await export_objects_to_graph_async(database.graph.relationships, stream, commit_size, create_relationship_query)


async def export_objects_to_graph_async(items: List[Any], stream: Neo4jStreamAsync, commit_size: int,
                                        query_function: Callable[[Any], AnyStr]) -> None:
    """
    Exports a list of object to the graph in an async manner
    :param items: the items to export
    :param stream: the graph to export to
    :param commit_size: the size of each commit to the graph
    :param query_function: the query function to convert the object to a neo4j query
    """
    for chunk in chunks(items, commit_size):
        async with stream.transaction() as transaction:
            for item in chunk:
                await transaction.run(query_function(item))


def export_objects_to_graph(objects: List[Any], stream: Neo4jStream, commit_size: int,
                            query_function: Callable[[Any], AnyStr]) -> None:
    """
    Writes an object to a neo4j stream converting it to a neo4j query using the supplied function
    :param objects: the source objects to write to neo4j
    :param stream: the neo4j stream to write to
    :param commit_size: the size of each objects commit
    :param query_function: the function to convert the object to a neo4j query
    """
    for chunk in chunks(objects, commit_size):
        with stream.transaction() as transaction:
            for item in chunk:
                transaction.run(query_function(item))


def delete_database_neo4j(stream: Neo4jStream):
    """
    Deletes a neo4j database
    WARNING! THIS WILL DELETE THE DATABASE IN NEO4J PERMANENTLY
    :param stream:
    :return:
    """
    stream.write("MATCH (n) DETACH DELETE n")


async def delete_database_neo4j_async(stream: Neo4jStreamAsync) -> None:
    """
    Deletes a neo4j database in an async manner
    WARNING! THIS WILL DELETE THE NEO4J CONTENTS PERMANENTLY
    :param stream: the stream to delete the database from
    """
    await stream.write_async("MATCH (n) DETACH DELETE n")
