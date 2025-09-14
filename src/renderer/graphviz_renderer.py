import os
from pathlib import Path
import graphviz
from src.domain.diagram import Diagram


def render_diagram(diagram: Diagram, output_file: str = "output_diagram", options=None) -> str:
    if options is None:
        options = {}

    # Configure for SVG output
    dot = graphviz.Digraph(format="svg", engine="dot")

    # Graph attributes
    dot.attr(rankdir=options.get("rankdir", "LR"))
    dot.attr(nodesep=options.get("nodesep", "0.6"))
    dot.attr(ranksep=options.get("ranksep", "0.7"))
    dot.attr("node", shape="record", style="filled")

    # External stylesheet for SVG (if provided)
    if getattr(diagram, "stylesheet", None):
        try:
            # Use file URI to be robust across OSes
            href = Path(str(diagram.stylesheet))
            if not href.is_absolute():
                # Resolve relative to current working dir
                href = (Path(os.getcwd()) / href).resolve()
            dot.attr("graph", stylesheet=href.as_uri())
        except (ValueError, OSError, TypeError):
            # Fallback: pass through the raw value
            dot.attr("graph", stylesheet=str(diagram.stylesheet))

    # --- Cluster Processing ---
    # A nested dictionary to hold cluster hierarchy
    # e.g., { "parent": { "nodes": [], "subclusters": { "child": { ... } } } }
    cluster_hierarchy = {}

    def find_or_create_cluster_path(path):
        """Navigates or creates a path in the hierarchy, returning the final level."""
        level = cluster_hierarchy
        for part in path:
            if part not in level:
                level[part] = {"nodes": [], "subclusters": {}}
            level = level[part]["subclusters"]
        return level

    # Populate the hierarchy
    for node in diagram.nodes.values():
        if node.cluster:
            full_path = node.cluster_path + [node.cluster]
            
            # Get the immediate parent level for this node's cluster
            parent_path = node.cluster_path
            parent_level = cluster_hierarchy
            if parent_path:
                parent_level = find_or_create_cluster_path(parent_path)

            # Ensure the node's own cluster exists at that level
            if node.cluster not in parent_level:
                 parent_level[node.cluster] = {"nodes": [], "subclusters": {}, "metadata_node": node}
            
            # Add node to its direct cluster
            parent_level[node.cluster]["nodes"].append(node)
            
            # Store the first node that defines metadata for this cluster
            if "metadata_node" not in parent_level[node.cluster]:
                parent_level[node.cluster]["metadata_node"] = node


    def render_cluster_recursively(subgraph_container, cluster_dict, cluster_id_prefix="c"):
        """Recursively renders clusters and their nodes."""
        for i, (name, data) in enumerate(cluster_dict.items()):
            cluster_id = f"{cluster_id_prefix}_{i}"
            # Use the metadata_node to get style attributes
            metadata_node = data.get("metadata_node")

            with subgraph_container.subgraph(name=f"cluster_{cluster_id}") as sub:
                sub.attr(label=name)
                if metadata_node:
                    if metadata_node.cluster_class:
                        sub.attr("graph", _attributes={"class": metadata_node.cluster_class})
                    if metadata_node.cluster_style:
                        sub.attr(style=metadata_node.cluster_style)
                    if metadata_node.cluster_color:
                        sub.attr(color=f"#{metadata_node.cluster_color}" if not metadata_node.cluster_color.startswith('#') else metadata_node.cluster_color)
                    if metadata_node.cluster_bgcolor:
                        sub.attr(bgcolor=f"#{metadata_node.cluster_bgcolor}" if not metadata_node.cluster_bgcolor.startswith('#') else metadata_node.cluster_bgcolor)

                # Render nodes within this cluster
                for node in data["nodes"]:
                    color = getattr(node, "color", None) or "lightblue"
                    node_kwargs = {"fillcolor": color}
                    if node.shape: node_kwargs["shape"] = node.shape
                    if node.css_class: node_kwargs["class"] = node.css_class
                    if node.image: node_kwargs["image"] = node.image
                    sub.node(node.key, node.to_graphviz(), **node_kwargs)

                # Render subclusters
                if data["subclusters"]:
                    render_cluster_recursively(sub, data["subclusters"], cluster_id)

    # Start rendering from the top level of the hierarchy
    render_cluster_recursively(dot, cluster_hierarchy)
    # --- End Cluster Processing ---

    # Render nodes not in any cluster
    for node in diagram.nodes.values():
        if node.cluster:
            continue
        color = getattr(node, "color", None) or "lightblue"
        node_kwargs = {"fillcolor": color}
        if getattr(node, "shape", None):
            node_kwargs["shape"] = node.shape
        if getattr(node, "css_class", None):
            node_kwargs["class"] = node.css_class
        if getattr(node, "image", None):
            node_kwargs["image"] = node.image
        dot.node(node.key, node.to_graphviz(), **node_kwargs)

    # Add relations
    for rel in diagram.relations:
        edge_kwargs = {}
        if getattr(rel, "style", None):
            edge_kwargs["style"] = rel.style
        if getattr(rel, "color", None):
            edge_kwargs["color"] = rel.color
        if getattr(rel, "css_class", None):
            edge_kwargs["class"] = rel.css_class
        if getattr(rel, "arrowhead", None):
            edge_kwargs["arrowhead"] = rel.arrowhead
        if getattr(rel, "arrowtail", None):
            edge_kwargs["arrowtail"] = rel.arrowtail
        if getattr(rel, "dir", None):
            edge_kwargs["dir"] = rel.dir
        dot.edge(rel.source_key, rel.target_key, label=rel.label or "", **edge_kwargs)

    # Produce SVG content
    svg_bytes = dot.pipe(format="svg")
    svg_text = svg_bytes.decode("utf-8")

    # Inline stylesheet block injection
    if getattr(diagram, "inline_stylesheet", None):
        css_text = str(diagram.inline_stylesheet)
        style_tag = "<style type=\"text/css\">\n" + css_text + "\n</style>\n"
        # Insert right after the opening <svg ...>
        start = svg_text.find("<svg")
        if start != -1:
            insert_pos = svg_text.find(">", start)
            if insert_pos != -1:
                svg_text = svg_text[: insert_pos + 1] + "\n" + style_tag + svg_text[insert_pos + 1 :]

    # Write SVG file
    output_path = os.path.join(os.getcwd(), f"{output_file}.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_text)

    return output_path


def get_dot(diagram: Diagram,  options=None) :
    if options is None:
        options = {}

    # Configure for SVG output
    dot = graphviz.Digraph(format="svg", engine="dot")

    # Graph attributes
    dot.attr(rankdir=options.get("rankdir", "LR"))
    dot.attr(nodesep=options.get("nodesep", "0.6"))
    dot.attr(ranksep=options.get("ranksep", "0.7"))
    dot.attr("node", shape="record", style="filled")

    # External stylesheet for SVG (if provided)
    if getattr(diagram, "stylesheet", None):
        try:
            # Use file URI to be robust across OSes
            href = Path(str(diagram.stylesheet))
            if not href.is_absolute():
                # Resolve relative to current working dir
                href = (Path(os.getcwd()) / href).resolve()
            dot.attr("graph", stylesheet=href.as_uri())
        except (ValueError, OSError, TypeError):
            # Fallback: pass through the raw value
            dot.attr("graph", stylesheet=str(diagram.stylesheet))

    # --- Cluster Processing ---
    # A nested dictionary to hold cluster hierarchy
    # e.g., { "parent": { "nodes": [], "subclusters": { "child": { ... } } } }
    cluster_hierarchy = {}

    def find_or_create_cluster_path(path):
        """Navigates or creates a path in the hierarchy, returning the final level."""
        level = cluster_hierarchy
        for part in path:
            if part not in level:
                level[part] = {"nodes": [], "subclusters": {}}
            level = level[part]["subclusters"]
        return level

    # Populate the hierarchy
    for node in diagram.nodes.values():
        if node.cluster:
            full_path = node.cluster_path + [node.cluster]
            
            # Get the immediate parent level for this node's cluster
            parent_path = node.cluster_path
            parent_level = cluster_hierarchy
            if parent_path:
                parent_level = find_or_create_cluster_path(parent_path)

            # Ensure the node's own cluster exists at that level
            if node.cluster not in parent_level:
                 parent_level[node.cluster] = {"nodes": [], "subclusters": {}, "metadata_node": node}
            
            # Add node to its direct cluster
            parent_level[node.cluster]["nodes"].append(node)
            
            # Store the first node that defines metadata for this cluster
            if "metadata_node" not in parent_level[node.cluster]:
                parent_level[node.cluster]["metadata_node"] = node


    def render_cluster_recursively(subgraph_container, cluster_dict, cluster_id_prefix="c"):
        """Recursively renders clusters and their nodes."""
        for i, (name, data) in enumerate(cluster_dict.items()):
            cluster_id = f"{cluster_id_prefix}_{i}"
            # Use the metadata_node to get style attributes
            metadata_node = data.get("metadata_node")

            with subgraph_container.subgraph(name=f"cluster_{cluster_id}") as sub:
                sub.attr(label=name)
                if metadata_node:
                    if metadata_node.cluster_class:
                        sub.attr("graph", _attributes={"class": metadata_node.cluster_class})
                    if metadata_node.cluster_style:
                        sub.attr(style=metadata_node.cluster_style)
                    if metadata_node.cluster_color:
                        sub.attr(color=f"#{metadata_node.cluster_color}" if not metadata_node.cluster_color.startswith('#') else metadata_node.cluster_color)
                    if metadata_node.cluster_bgcolor:
                        sub.attr(bgcolor=f"#{metadata_node.cluster_bgcolor}" if not metadata_node.cluster_bgcolor.startswith('#') else metadata_node.cluster_bgcolor)

                # Render nodes within this cluster
                for node in data["nodes"]:
                    color = getattr(node, "color", None) or "lightblue"
                    node_kwargs = {"fillcolor": color}
                    if node.shape: node_kwargs["shape"] = node.shape
                    if node.css_class: node_kwargs["class"] = node.css_class
                    if node.image: node_kwargs["image"] = node.image
                    sub.node(node.key, node.to_graphviz(), **node_kwargs)

                # Render subclusters
                if data["subclusters"]:
                    render_cluster_recursively(sub, data["subclusters"], cluster_id)

    # Start rendering from the top level of the hierarchy
    render_cluster_recursively(dot, cluster_hierarchy)
    # --- End Cluster Processing ---

    # Render nodes not in any cluster
    for node in diagram.nodes.values():
        if node.cluster:
            continue
        color = getattr(node, "color", None) or "lightblue"
        node_kwargs = {"fillcolor": color}
        if getattr(node, "shape", None):
            node_kwargs["shape"] = node.shape
        if getattr(node, "css_class", None):
            node_kwargs["class"] = node.css_class
        if getattr(node, "image", None):
            node_kwargs["image"] = node.image
        dot.node(node.key, node.to_graphviz(), **node_kwargs)

    # Add relations
    for rel in diagram.relations:
        edge_kwargs = {}
        if getattr(rel, "style", None):
            edge_kwargs["style"] = rel.style
        if getattr(rel, "color", None):
            edge_kwargs["color"] = rel.color
        if getattr(rel, "css_class", None):
            edge_kwargs["class"] = rel.css_class
        if getattr(rel, "arrowhead", None):
            edge_kwargs["arrowhead"] = rel.arrowhead
        if getattr(rel, "arrowtail", None):
            edge_kwargs["arrowtail"] = rel.arrowtail
        if getattr(rel, "dir", None):
            edge_kwargs["dir"] = rel.dir
        dot.edge(rel.source_key, rel.target_key, label=rel.label or "", **edge_kwargs)
        
    return dot