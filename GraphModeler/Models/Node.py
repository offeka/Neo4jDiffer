import uuid
from dataclasses import dataclass, InitVar
from typing import Dict, AnyStr, Union


@dataclass
class Node:
    """
    A neo4j node
    sometimes called an edge
    """
    node_type: AnyStr
    properties: Dict[AnyStr, AnyStr] = None
    given_id: InitVar[Union[uuid.UUID, str]] = None

    def __post_init__(self, given_id):
        if not self.properties:
            self.properties = {}
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
        return self.node_type == other.node_type and self.properties == other.properties
