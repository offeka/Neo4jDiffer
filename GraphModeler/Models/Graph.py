from typing import List
from dataclasses import dataclass, field

from GraphModeler.Models import Node, Relationship


@dataclass
class Graph:
    """
    A neo4j graph
    """
    nodes: List[Node] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
