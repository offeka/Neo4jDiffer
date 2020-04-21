import pytest

from TestGraphGenerator.DbManager.DbLoader import load_node, load_relationship, load_graph
from TestGraphGenerator.Models import Node, Relationship
from TestGraphGenerator.Models.Graph import Graph


@pytest.fixture
def relationship_nodes():
    return {"1": Node("TypeA", given_id="1"), "2": Node("TypeB", given_id="2")}


def test_load_node():
    # Arrange
    expected = Node("TestType", given_id="1")
    # Act
    result = load_node({"node_type": "TestType", "properties": {"node_id": "1"}})
    # Assert
    assert result == expected


def test_load_relationship(relationship_nodes):
    # Arrange
    expected = Relationship(relationship_nodes["1"], "Rel", relationship_nodes["2"])
    # Act
    result = load_relationship({"node_a": "1", "relationship_type": "Rel", "node_b": "2"}, relationship_nodes)
    # Assert
    assert result == expected


def test_load_graph(relationship_nodes):
    # Arrange
    expected = Graph([Node("TypeA", given_id="1"), Node("TypeB", given_id="2")],
                     [Relationship(relationship_nodes["1"], "Rel", relationship_nodes["2"])])
    # Act
    result = load_graph({
        "nodes":
            [
                {"node_type": "TypeA", "properties": {"node_id": "1"}},
                {"node_type": "TypeB", "properties": {"node_id": "2"}}
            ],
        "relationships":
            [
                {"node_a": "1", "relationship_type": "Rel", "node_b": "2"}
            ]
    })
    # Assert
    assert result == expected
