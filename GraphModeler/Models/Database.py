from dataclasses import dataclass
from typing import AnyStr

from GraphModeler.Models.Graph import Graph


@dataclass
class Database:
    """
    A neo4j database with its graph object
    """
    graph: Graph
    name: AnyStr

