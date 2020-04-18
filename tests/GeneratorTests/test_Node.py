from TestGraphGenerator.GraphModels.Node import Node
import pytest


def test_generate_query():
    # Arrange
    test_node = Node("test", properties={"prop1": "value"})
    expected = "(n:Test {prop1: 'value'})"

    # Act
    result = test_node.as_query()

    # Assert
    assert result == expected


def test_fluent_properties():
    # Arrange
    test_node = Node("test")
    expected = Node("test", properties={"prop1": "value"})

    # Act
    test_node["prop1"] = "value"

    # Assert
    assert test_node == expected


def test_no_properties_error():
    # Arrange
    test_node = Node("test")
    # Act
    with pytest.raises(ValueError):
        test_node.as_query()
