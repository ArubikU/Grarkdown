import os
from pathlib import Path
import graphviz
from src.domain.diagram import Diagram
import requests
import tempfile

def download_temp_image(url: str) -> str:
    """Descarga una imagen y la guarda en un archivo temporal.
       Retorna el path local para usar en Graphviz."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    suffix = os.path.splitext(url)[1] or ".png"  # adivinar extensión
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_file.write(response.content)
    tmp_file.close()
    # Normalizar path → usar "/" para que Graphviz lo acepte
    path = os.path.abspath(tmp_file.name)
    return path.replace("\\", "/")

def get_width_height(image_path: str):
    #read as url and obtaine params
    url = image_path
    from urllib.parse import urlparse, parse_qs
    parsed_url = urlparse(url)
    width = parse_qs(parsed_url.query).get("width", [None])[0]
    height = parse_qs(parsed_url.query).get("height", [None])[0]
    newurl = url.split('?')[0]
    return width, height, newurl

import os
import base64
import re
from graphviz import Digraph

def render_diagram(diagram: "Diagram", output_file: str = "output_diagram", options=None) -> str:
    dot = get_dot(diagram, options)

    # Generar SVG como texto
    svg_bytes = dot.pipe(format="svg")
    svg_text = svg_bytes.decode("utf-8")

    # Reemplazar rutas locales de <image> por base64
    def inline_image(match):
        href = match.group(1)
        if os.path.isfile(href):
            with open(href, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f'<image xlink:href="data:image/png;base64,{b64}"'
        else:
            # Si no existe el archivo, dejar la ruta original
            return match.group(0)

    svg_text = re.sub(r'<image[^>]+xlink:href="([^"]+)"', inline_image, svg_text)

    # Inline stylesheet block injection
    if getattr(diagram, "inline_stylesheet", None):
        css_text = str(diagram.inline_stylesheet)
        style_tag = "<style type=\"text/css\">\n" + css_text + "\n</style>\n"
        # Insertar después del <svg ...>
        start = svg_text.find("<svg")
        if start != -1:
            insert_pos = svg_text.find(">", start)
            if insert_pos != -1:
                svg_text = svg_text[: insert_pos + 1] + "\n" + style_tag + svg_text[insert_pos + 1 :]

    # Guardar SVG final
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
                    node_kwargs = {"fillcolor": color, "label": node.to_graphviz()}
                    if node.shape: node_kwargs["shape"] = node.shape
                    if node.css_class: node_kwargs["class"] = node.css_class
                    if node.image:
                        width, height, url = get_width_height(node.image)
                        local_image_path = download_temp_image(url)
                        node_kwargs["image"] = local_image_path
                        node_kwargs["labelloc"] = "b"
                        node_kwargs["fixedsize"] = "true"
                        node_kwargs["width"] = width if width else "1.0"
                        node_kwargs["height"] = height if height else "1.0"
                        del node_kwargs["label"]
                        node_kwargs["shape"] = "box"
                    sub.node(node.key, **node_kwargs)

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
            if node.image:
                width, height, url = get_width_height(node.image)
                local_image_path = download_temp_image(url)
                node_kwargs["image"] = local_image_path
                node_kwargs["labelloc"] = "b"
                node_kwargs["fixedsize"] = "true"
                node_kwargs["width"] = width if width else "1.0"
                node_kwargs["height"] = height if height else "1.0"
                del node_kwargs["label"]
                node_kwargs["shape"] = "box"
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