import argparse
import os
from src.parser.markdown_parser import parse_markdown
from src.renderer.graphviz_renderer import render_diagram, get_dot

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Graphviz Diagram")

    parser.add_argument("file", help="Markdown file to process")
    parser.add_argument("--output", "-o", default="output_diagram", help="Output file name without extension (default: output_diagram)")
    parser.add_argument("--format", "-f", choices=["svg", "dot"], default="svg", help="Output format (default: svg)")
    parser.add_argument("--rankdir", default="LR", help="Graph rank direction (default: LR)")
    parser.add_argument("--nodesep", default="0.6", help="Node separation (default: 0.6)")
    parser.add_argument("--ranksep", default="0.7", help="Rank separation (default: 0.7)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: The file '{args.file}' does not exist.")
        return
    options = {
        'rankdir': args.rankdir,
        'nodesep': args.nodesep,
        'ranksep': args.ranksep
    }
    with open(args.file, "r", encoding="utf-8") as f:
        markdown_text = f.read()
    output_file = args.output or "output_diagram"
    diagram = parse_markdown(markdown_text)
    # Ajuste según el formato
    if args.format == "dot":
        diagram_path = f"{output_file}.dot"
        with open(diagram_path, "w", encoding="utf-8") as dot_file:
            dot_file.write(get_dot(diagram).source)  # exporta el DOT directamente
    else:
        diagram_path = render_diagram(diagram, output_file=output_file, options=options)
    print(f"Diagram generated at: {diagram_path}")
if __name__ == "__main__":
    main()
