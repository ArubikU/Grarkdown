import argparse
import os
import re

import graphviz

os.environ["PATH"] += os.pathsep + 'C:/Users/ejane/scoop/apps/graphviz/12.2.1/bin'
selfpath = os.path.abspath(os.path.dirname(__file__))

def markdown_to_graphviz_advanced(markdown_text, output_file="output_diagram", options=None):
    """
    Convierte un formato markdown custom avanzado a un diagrama Graphviz con secciones diferenciadas,
    relaciones automáticas basadas en el tipo de retorno de funciones y colores de nodo personalizados.
    
    Args:
        markdown_text (str): El texto markdown a convertir.
        output_file (str): Nombre del archivo de salida (sin extensión).
        options (dict): Opciones adicionales para el diagrama (rankdir, nodesep, ranksep).
    
    Returns:
        str: La ruta al archivo generado.
    """
    if options is None:
        options = {}

    class Node:
        def __init__(self, name, key):
            self.name = name
            self.key = key
            self.variables = []
            self.functions = []
            self.color = None

        def add_variable(self, variable):
            self.variables.append(variable)

        def add_function(self, function):
            self.functions.append(function)

        def to_graphviz(self):
            var_section = "\\n".join(self.variables).replace("<", "\\<").replace(">", "\\>") if self.variables else "(Ninguna)"
            func_section = "\\n".join(self.functions).replace("<", "\\<").replace(">", "\\>") if self.functions else "(Ninguna)"
            return f"{{ {self.name} [{self.key}] | {{ Variables:\\n|{var_section} }} | {{ Funciones:\\n|{func_section} }} }}"

    class Diagram:
        def __init__(self):
            self.nodes = {}
            self.relations = []

        def add_node(self, node):
            self.nodes[node.key] = node
            print(f"Added node: {node.key}")  # Debug print

        def add_relation(self, source_key, target_key, label):
            self.relations.append((source_key, target_key, label))
            print(f"Added relation: {source_key} -> {target_key} ({label})")  # Debug print

        def render(self, output_file):
            diagram = graphviz.Digraph(format="png", engine="dot")
            
            # Set graph options
            if 'rankdir' in options:
                diagram.attr(rankdir=options['rankdir'])
            if 'nodesep' in options:
                diagram.attr(nodesep=options['nodesep'])
            if 'ranksep' in options:
                diagram.attr(ranksep=options['ranksep'])
            
            diagram.attr('node', shape='record', style='filled')

            # Add nodes
            for node in self.nodes.values():
                print(f"Rendering node: {node.key}")  # Debug print
                color = node.color or "lightblue"
                diagram.node(node.key, node.to_graphviz(), fillcolor=color)

            # Add relations
            for source, target, label in self.relations:
                print(f"Rendering relation: {source} -> {target} ({label})")  # Debug print
                diagram.edge(source, target, label=label)

            # Render diagram
            diagram_path = f"{selfpath}\\{output_file}"
            diagram.render(diagram_path, format="png", cleanup=True)
            return diagram_path + ".png"

    # Parse markdown
    diagram = Diagram()
    blocks = re.findall(
        r"#\s*{(\w+)}\s+\[(\w+)\]\n"
        r"(### OPT COLOR\s+([A-Fa-f0-9]{6})\n)?"
        r"## VAR(.*?)## END VAR\n"
        r"## FUNC(.*?)## END FUNC\n"
        r"(## F_RELA.*?## END F_RELA)?",
        markdown_text,
        re.DOTALL,
    )

    for block in blocks:
        name = block[0]
        key = block[1]
        variables = str(block[4]).strip().split("\n")
        functions = str(block[5]).strip().split("\n")
        node = Node(name, key)

        # Extract color
        color_match = block[3]
        if color_match:
            node.color = f"#{color_match}"
        # Add variables
        for var in variables:
            node.add_variable(var.strip("- ").strip())
            print(f"Added variable: {var.strip('- ').strip()}")  # Debug print

        # Add functions
        for func in functions:
            node.add_function(func.strip("- ").strip())
            print(f"Added functions: {func.strip('- ').strip()}")  # Debug print

        diagram.add_node(node)

        # Add explicit relations from F_RELA
        rela_block = re.search(r"## F_RELA(.*?)## END F_RELA", block[6], re.DOTALL)
        if rela_block:
            relations_block = rela_block.group(1)
            for line in relations_block.strip().split("\n"):
                if line.strip():
                    optional_label = re.search(r"\{(.*?)\}", line).group(1) if "{" in line else None
                    if line.startswith("- TO"):
                        target_key = re.search(r"\[(\w+)\]", line).group(1)
                        if not optional_label:
                            optional_label = "TO"
                        diagram.add_relation(key, target_key, label=optional_label)
                    elif line.startswith("- FROM"):
                        source_key = re.search(r"\[(\w+)\]", line).group(1)
                        if not optional_label:
                            optional_label = "FROM"
                        diagram.add_relation(source_key, key, label=optional_label)
                    elif line.startswith("- BI"):
                        bi_key = re.search(r"\[(\w+)\]", line).group(1)
                        if not optional_label:
                            optional_label = "BI"   
                        diagram.add_relation(key, bi_key, label=optional_label)
                        diagram.add_relation(bi_key, key, label=optional_label)
    return diagram.render(output_file)

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Graphviz Diagram")
    parser.add_argument("file", nargs="?", help="Markdown file to process")
    parser.add_argument("--rankdir", default="LR", help="Graph rank direction (default: LR)")
    parser.add_argument("--nodesep", default="0.6", help="Node separation (default: 0.6)")
    parser.add_argument("--ranksep", default="0.7", help="Rank separation (default: 0.7)")

    args = parser.parse_args()

    if not args.file:
        args.file = input("Introduce el nombre del archivo Markdown: ").strip()

    if not os.path.exists(args.file):
        print("El archivo no existe.")
        return

    options = {
        'rankdir': args.rankdir,
        'nodesep': args.nodesep,
        'ranksep': args.ranksep
    }

    with open(args.file, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    output_file = input("Introduce el nombre del archivo de salida (sin extensión, por defecto 'output_diagram'): ").strip()
    if not output_file:
        output_file = "output_diagram"

    diagram_path = markdown_to_graphviz_advanced(markdown_text, output_file=output_file, options=options)
    print(f"Diagrama generado en: {diagram_path}")

if __name__ == "__main__":
    main()
