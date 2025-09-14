from typing import List, Dict, Optional
from src.domain.node import Node
from src.domain.relation import Relation

class Diagram:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.relations: List[Relation] = []
        self.stylesheet: Optional[str] = None
        self.inline_stylesheet: Optional[str] = None

    def add_node(self, node: Node):
        self.nodes[node.key] = node

    def add_relation(self, relation: Relation):
        self.relations.append(relation)



