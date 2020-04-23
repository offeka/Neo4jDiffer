import uuid
from dataclasses import dataclass, InitVar
from typing import Dict, AnyStr, Union, List


@dataclass
class Node:
    """
    A neo4j node
    sometimes called an edge
    """
    node_types: Union[List[AnyStr], AnyStr] = None
    properties: Dict[AnyStr, AnyStr] = None
    given_id: InitVar[Union[uuid.UUID, str]] = None

    def __post_init__(self, given_id):
        if not self.properties:
            self.properties = {}
        self.__init_node_types()
        self.__init_id(given_id)

    def __init_node_types(self):
        if not self.node_types:
            raise ValueError("Cannot create a node without one at least type")
        if not isinstance(self.node_types, list):
            self.node_types = [self.node_types]

    def __init_id(self, given_id):
        try:
            self.node_id = self.properties["node_id"]
        except KeyError:
            if given_id:
                self.node_id = given_id
            else:
                self.node_id = uuid.uuid4()

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    @property
    def node_id(self):
        return self.properties["node_id"]

    @node_id.setter
    def node_id(self, value: uuid.UUID):
        self.properties["node_id"] = str(value)

    def __eq__(self, other):
        return self.node_types == other.node_types and self.properties == other.properties

    def __hash__(self):
        return hash((frozenset(self.node_types), self.node_id))
