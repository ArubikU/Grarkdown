import graphviz
import os

selfpath = os.path.abspath(os.path.dirname(__file__))

class Diagram:
    def __init__(self, options=None):
        if options is None:
            options = {}
        self.nodes = {}
        self.relations = []
        self.options = options

    def add_node(self, node):
        self.nodes[node.key] = node
        print(f"Added node: {node.key}")

    def add_relation(self, source_key, target_key, label):
        self.relations.append((source_key, target_key, label))
        print(f"Added relation: {source_key} -> {target_key} ({label})")

    def render(self, output_file):
        diagram = graphviz.Digraph(format="png", engine="dot")
        
        if 'rankdir' in self.options:
            diagram.attr(rankdir=self.options['rankdir'])
        if 'nodesep' in self.options:
            diagram.attr(nodesep=self.options['nodesep'])
        if 'ranksep' in self.options:
            diagram.attr(ranksep=self.options['ranksep'])
        
        diagram.attr('node', shape='record', style='filled')

        for node in self.nodes.values():
            print(f"Rendering node: {node.key}")
            color = node.color or "lightblue"
            diagram.node(node.key, node.to_graphviz(), fillcolor=color)

        for source, target, label in self.relations:
            print(f"Rendering relation: {source} -> {target} ({label})")
            diagram.edge(source, target, label=label)

        diagram_path = f"{selfpath}\\{output_file}"
        diagram.render(diagram_path, format="png", cleanup=True)
        return diagram_path + ".png"
