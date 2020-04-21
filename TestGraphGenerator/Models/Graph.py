from typing import Iterable
from dataclasses import dataclass, field

from TestGraphGenerator.Models import Node, Relationship


@dataclass
class Graph:
    """
    A neo4j graph
    """
    nodes: Iterable[Node] = field(default_factory=list)
    relations: Iterable[Relationship] = field(default_factory=list)
