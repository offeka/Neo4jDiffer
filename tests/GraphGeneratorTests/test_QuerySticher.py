import pytest

from TestGraphGenerator.Models import Node
from TestGraphGenerator.QuerySticher import create_node_query, delete_node_query


@pytest.fixture()
def test_node() -> Node:
    return Node("TestType", properties={"prop1": "value1"})


def test_create_node_query_sanity(test_node):
    # Arrange
    expected = "MERGE (n:TestType {prop1: 'value1'})"
    # Act
    result = create_node_query(test_node)
    # Assert
    assert result == expected


def test_delete_node_query_sanity(test_node):
    # Arrange
    expected = "MATCH (n:TestType {prop1: 'value1'}) DELETE n"
    # Act
    result = delete_node_query(test_node)
    # Assert
    assert result == expected
