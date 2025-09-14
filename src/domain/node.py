from typing import List, Optional

class Node:
    def __init__(self, name: str, key: str):
        self.name = name
        self.key = key
        self.variables: List[str] = []
        self.functions: List[str] = []
        self.color: Optional[str] = None
        self.image: Optional[str] = None
        self.shape: Optional[str] = "record"
        self.css_class: Optional[str] = None
        self.description: Optional[str] = None
        # Cluster metadata
        self.cluster: Optional[str] = None           # Cluster name/label
        self.cluster_path: List[str] = []            # Parent cluster path
        self.cluster_class: Optional[str] = None     # CSS class for the cluster container
        self.cluster_color: Optional[str] = None     # Border color
        self.cluster_style: Optional[str] = None     # e.g., rounded, filled
        self.cluster_bgcolor: Optional[str] = None   # Background color (SVG: maps to bgcolor)

    def add_variable(self, variable: str):
        self.variables.append(variable)

    def add_function(self, function: str):
        self.functions.append(function)

    def to_graphviz(self) -> str:
        # If an image is present, the label is just the name, as the image will be the main content.
        if self.image:
            return self.name

        # Build title cell (include optional description on a new line)
        title = f"{self.name} [{self.key}]"
        if self.description:
            safe_desc = self.description.replace("<", "\\<").replace(">", "\\>")
            title = f"{title}\\n{safe_desc}"

        var_section = "\\n".join(self.variables).replace("<", "\\<").replace(">", "\\>") if self.variables else "(None)"
        parts = [f"{title}", f"{{ Variables:\n|{var_section} }}"]

        # Only include Functions section if there are functions
        if self.functions:
            func_section = "\\n".join(self.functions).replace("<", "\\<").replace(">", "\\>")
            parts.append(f"{{ Functions:\n|{func_section} }}")

        return "{ " + " | ".join(parts) + " }"

