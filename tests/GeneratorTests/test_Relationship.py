from TestGraphGenerator.GraphModels.Node import Node
from TestGraphGenerator.GraphModels.Relationship import Relationship


def test_creating_relationship():
    # Arrange
    a = Node(node_type="person")
    a['test'] = 'value'
    b = Node(node_type="person", properties={"name": "test"})
    rel = Relationship(a, "knows", b)
    expected = "MATCH (nodeA:Person {test: 'value'}), (nodeB:Person {name: 'test'}) MERGE (nodeA)-[r:Knows]-(nodeB)"

    # Act
    result = rel.relationship_query()

    # Assert
    assert result == expected


def test_deleting_relationship():
    # Arrange
    a = Node(node_type="person")
    a['test'] = 'value'
    b = Node(node_type="person", properties={"name": "test"})
    rel = Relationship(a, "knows", b)
    expected = "MATCH (nodeA:Person {test: 'value'}), (nodeB:Person {name: 'test'}) DELETE r"
    # Act
    result = rel.delete_relationship_query()
    # Assert
    assert result == expected
