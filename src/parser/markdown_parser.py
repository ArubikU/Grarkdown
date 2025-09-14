import re
from src.domain.node import Node
from src.domain.diagram import Diagram
from src.domain.relation import Relation

def parse_attributes(line: str) -> dict:
    """Parses attributes like [key=value, key2=value2]"""
    attrs = {}
    matches = re.findall(r"(\w+)\s*=\s*([\w\.\/:\-]+)", line)
    for key, value in matches:
        attrs[key] = value
    return attrs

def parse_markdown(markdown_text: str) -> Diagram:
    diagram = Diagram()

    # Global stylesheet file
    stylesheet_match = re.search(r"^### STYLESHEET\s+(.+)$", markdown_text, re.MULTILINE)
    if stylesheet_match:
        diagram.stylesheet = stylesheet_match.group(1).strip()

    # Inline stylesheet block
    inline_stylesheet_match = re.search(r"### STYLESHEET\n(.*?)\n### END STYLESHEET", markdown_text, re.DOTALL)
    if inline_stylesheet_match:
        diagram.inline_stylesheet = inline_stylesheet_match.group(1).strip()


    # Node blocks with optional sections (VAR, FUNC, F_RELA). Name accepts any chars until '}'.
    blocks = re.findall(
        r"#\s*{([^}]+)}\s+\[(\w+)\]\s*\n"
        r"((?:### OPT .*?\n)*)?"  # optional options lines
        r"(?:## VAR(.*?)## END VAR\n)?"  # optional VAR block
        r"(?:## FUNC(.*?)## END FUNC\n)?"  # optional FUNC block
        r"(?:## F_RELA(.*?)## END F_RELA)?",  # optional relations block (capture inner only)
        markdown_text,
        re.DOTALL,
    )

    for block in blocks:
        name, key, opts_block, var_block, func_block, rela_block_full = block
        node = Node(name, key)

        if opts_block:
            opts = opts_block.strip().split('\n')
            for opt in opts:
                if 'COLOR' in opt:
                    color_match = re.search(r"COLOR\s+([A-Fa-f0-9]{6})", opt)
                    if color_match:
                        node.color = f"#{color_match.group(1)}"
                elif 'IMAGE' in opt:
                    image_match = re.search(r"IMAGE\s+(https?://[^\s]+)", opt)
                    if image_match:
                        node.image = image_match.group(1)
                elif 'SHAPE' in opt:
                    shape_match = re.search(r"SHAPE\s+(\w+)", opt)
                    if shape_match:
                        node.shape = shape_match.group(1)
                elif 'CLASS' in opt:
                    class_match = re.search(r"CLASS\s+(\w+)", opt)
                    if class_match:
                        node.css_class = class_match.group(1)
                elif 'DESC' in opt:
                    # Everything after DESC is considered the description (trim quotes if provided)
                    desc_match = re.search(r"DESC\s+(.+)$", opt)
                    if desc_match:
                        desc = desc_match.group(1).strip()
                        if (desc.startswith('"') and desc.endswith('"')) or (desc.startswith("'") and desc.endswith("'")):
                            desc = desc[1:-1]
                        node.description = desc
                elif 'CLUSTER' in opt:
                    # Syntax: CLUSTER <name> or CLUSTER <A>B>C> [attributes...]
                    cluster_name_match = re.search(r"CLUSTER\s+([^\[]+)", opt)
                    if cluster_name_match:
                        full_cluster_name = cluster_name_match.group(1).strip()
                        parts = [p.strip() for p in full_cluster_name.split('>')]
                        if len(parts) > 1:
                            node.cluster_path = parts[:-1]
                            node.cluster = parts[-1]
                        else:
                            node.cluster = parts[0]

                    # parse inline [k=v,...]
                    cluster_attrs = parse_attributes(opt)
                    if 'class' in cluster_attrs:
                        node.cluster_class = cluster_attrs.get('class')
                    if 'style' in cluster_attrs:
                        node.cluster_style = cluster_attrs.get('style')
                    if 'color' in cluster_attrs:
                        node.cluster_color = cluster_attrs.get('color')
                    if 'bgcolor' in cluster_attrs:
                        node.cluster_bgcolor = cluster_attrs.get('bgcolor')

        if var_block:
            for var in var_block.strip().split("\n"):
                if var.strip():
                    node.add_variable(var.strip("- ").strip())

        if func_block:
            for func in func_block.strip().split("\n"):
                if func.strip():
                    node.add_function(func.strip("- ").strip())

        diagram.add_node(node)

        rela_block_content = None
        if rela_block_full:
            # In the new pattern we already capture only the inner content
            rela_block_content = rela_block_full

        if rela_block_content:
            relations_block = rela_block_content
            for line in relations_block.strip().split("\n"):
                if not line.strip():
                    continue

                label_match = re.search(r"\{(.*?)\}", line)
                label = label_match.group(1) if label_match else ""

                target_key_match = re.search(r"\[(\w+)\]", line)
                if not target_key_match:
                    continue

                target_key = target_key_match.group(1)

                attrs = parse_attributes(line)

                relation = None
                if line.strip().startswith("- TO"):
                    relation = Relation(key, target_key, label)
                elif line.strip().startswith("- FROM"):
                    relation = Relation(target_key, key, label)
                elif line.strip().startswith("- BI"):
                    relation1 = Relation(key, target_key, label)
                    relation2 = Relation(target_key, key, label)
                    relation1.style = attrs.get('style')
                    relation1.color = attrs.get('color')
                    relation1.css_class = attrs.get('class')
                    relation2.style = attrs.get('style')
                    relation2.color = attrs.get('color')
                    relation2.css_class = attrs.get('class')
                    diagram.add_relation(relation1)
                    diagram.add_relation(relation2)
                    continue

                if relation:
                    relation.style = attrs.get('style')
                    relation.color = attrs.get('color')
                    relation.css_class = attrs.get('class')
                    diagram.add_relation(relation)
                    
                    if(attrs.get('arrowhead')):
                        if line.strip().startswith("- TO"):
                            relation.arrowhead = attrs.get('arrowhead')
                        elif line.strip().startswith("- FROM"):
                            relation.arrowtail = attrs.get('arrowhead')
                    if(attrs.get('arrowtail')):
                        if line.strip().startswith("- TO"):
                            relation.arrowtail = attrs.get('arrowtail')
                        elif line.strip().startswith("- FROM"):
                            relation.arrowhead = attrs.get('arrowtail')
                        
                        
    return diagram



