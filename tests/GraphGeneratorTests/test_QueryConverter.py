import pytest

from GraphModeler.Models import Relationship, Node
from GraphModeler.Models.QueryConverter import relationship_query, relationship_nodes_query, node_query


@pytest.fixture()
def test_relationship():
    return Relationship(Node("TestTypeA", {"prop1": "value1"}, "1"),
                        "Test",
                        Node("TestTypeB", {"prop2": "value2"}, "2"))


def test_relationship_query_sanity(test_relationship):
    # Arrange
    expected = "(nodeA)-[r:Test]-(nodeB)"
    # Act
    result = relationship_query(test_relationship)
    # Assert
    assert result == expected


def test_relationship_nodes_query_sanity(test_relationship):
    # Arrange
    expected = "(nodeA:TestTypeA {prop1: 'value1', node_id: '1'}), (nodeB:TestTypeB {prop2: 'value2', node_id: '2'})"
    # Act
    result = relationship_nodes_query(test_relationship)
    # Assert
    assert result == expected


def test_node_query_sanity():
    # Arrange
    expected = "(n:TestType {prop1: 'value1', node_id: '1'})"
    test_node = Node("TestType", {"prop1": "value1"}, "1")
    # Act
    result = node_query(test_node)
    # Assert
    assert result == expected
