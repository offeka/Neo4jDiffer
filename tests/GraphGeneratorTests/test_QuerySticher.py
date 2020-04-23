import pytest

from GraphModeler.Models import Node, Relationship
from GraphModeler.DbTranformations.QuerySticher import create_node_query, delete_node_query, create_relationship_query, \
    delete_relationship_query


@pytest.fixture()
def test_node() -> Node:
    return Node("TestType", {"prop1": "value1"}, "1")


@pytest.fixture()
def test_relationship() -> Relationship:
    return Relationship(Node("TestTypeA", {"prop1": "value1"}, "1"),
                        "Knows",
                        Node("TestTypeB", {"prop2": "value2"}, "2"))


def test_create_node_query_sanity(test_node):
    # Arrange
    expected = "MERGE (n:TestType {prop1: 'value1', node_id: '1'})"
    # Act
    result = create_node_query(test_node)
    # Assert
    assert result == expected


def test_delete_node_query_sanity(test_node):
    # Arrange
    expected = "MATCH (n:TestType {prop1: 'value1', node_id: '1'}) DELETE n"
    # Act
    result = delete_node_query(test_node)
    # Assert
    assert result == expected


def test_create_relationship_query_sanity(test_relationship):
    # Arrange
    expected = "MATCH (nodeA:TestTypeA {prop1: 'value1', node_id: '1'}), " \
               "(nodeB:TestTypeB {prop2: 'value2', node_id: '2'}) " \
               "MERGE (nodeA)-[r:Knows]-(nodeB)"
    # Act
    result = create_relationship_query(test_relationship)
    # Assert
    assert result == expected


def test_delete_relationship_query_sanity(test_relationship):
    # Arrange
    expected = "MATCH (nodeA:TestTypeA {prop1: 'value1', node_id: '1'}), " \
               "(nodeB:TestTypeB {prop2: 'value2', node_id: '2'}) " \
               "(nodeA)-[r:Knows]-(nodeB) DELETE r"
    # Act
    result = delete_relationship_query(test_relationship)
    # Assert
    assert result == expected
