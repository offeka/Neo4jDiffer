import pytest

from TestGraphGenerator.Models import Relationship, Node
from TestGraphGenerator.Models.Tranformations import relationship_query, relationship_nodes_query, node_query


@pytest.fixture()
def test_relationship():
    return Relationship(Node("TestTypeA", {"prop1": "value1"}), "Test", Node("TestTypeB", {"prop2": "value2"}))


def test_relationship_query_sanity(test_relationship):
    # Arrange
    expected = "(nodeA)-[r:Test]-(nodeB)"
    # Act
    result = relationship_query(test_relationship)
    # Assert
    assert result == expected


def test_relationship_nodes_query_sanity(test_relationship):
    # Arrange
    expected = "(nodeA:TestTypeA {prop1: 'value1'}), (nodeB:TestTypeB {prop2: 'value2'})"
    # Act
    result = relationship_nodes_query(test_relationship)
    # Assert
    assert result == expected


def test_node_query_sanity():
    # Arrange
    expected = "(n:TestType {prop1: 'value1'})"
    test_node = Node("TestType", {"prop1": "value1"})
    # Act
    result = node_query(test_node)
    # Asset
    assert result == expected
