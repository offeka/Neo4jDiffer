import pytest

from GraphModeler.DbTranformations.DbSaver import export_node_json, export_relationship_json, export_graph_json
from GraphModeler.Models import Node, Relationship
from GraphModeler.Models.Graph import Graph


@pytest.fixture()
def test_node() -> Node:
    return Node("TestType", given_id="1")


@pytest.fixture()
def test_relationship() -> Relationship:
    return Relationship(Node("TypeA", given_id="1"), "Rel", Node("TypeB", given_id="2"))


def test_node_json(test_node):
    # Arrange
    expected = {"node_type": "TestType", "properties": {"node_id": "1"}}
    # Act
    result = export_node_json(test_node)
    # Assert
    assert result == expected


def test_relationship_json(test_relationship):
    # Arrange
    expected = {"node_a": "1", "relationship_type": "Rel", "node_b": "2"}
    # Act
    result = export_relationship_json(test_relationship)
    # Assert
    assert result == expected


def test_graph_json(test_relationship, test_node):
    # Arrange
    expected = {
        "nodes":
            [
                {"node_type": "TestType", "properties": {"node_id": "1"}}
            ],
        "relationships":
            [
                {"node_a": "1", "relationship_type": "Rel", "node_b": "2"}
            ]
    }
    # Act
    test_graph = Graph([test_node], [test_relationship])
    result = export_graph_json(test_graph)
    # Assert
    assert result == expected
