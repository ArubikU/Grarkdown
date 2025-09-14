from typing import Optional


class Relation:
    def __init__(self, source_key: str, target_key: str, label: str):
        self.source_key = source_key
        self.target_key = target_key
        self.label = label
        self.style: Optional[str] = None
        self.color: Optional[str] = None
        self.css_class: Optional[str] = None
        self.arrowhead: Optional[str] = None
        self.arrowtail: Optional[str] = None
        # Graphviz direction attribute: forward | back | both | none
        self.dir: Optional[str] = None
