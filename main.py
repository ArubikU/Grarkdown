import argparse
import os
from src.parser.markdown_parser import parse_markdown
from src.renderer.graphviz_renderer import render_diagram

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Graphviz Diagram")
    parser.add_argument("file", nargs="?", help="Markdown file to process")
    parser.add_argument("--output", "-o", default="output_diagram", help="Output file name without extension (default: output_diagram)")
    parser.add_argument("--rankdir", default="LR", help="Graph rank direction (default: LR)")
    parser.add_argument("--nodesep", default="0.6", help="Node separation (default: 0.6)")
    parser.add_argument("--ranksep", default="0.7", help="Rank separation (default: 0.7)")

    args = parser.parse_args()

    if not args.file:
        try:
            args.file = input("Enter the Markdown file name: ").strip()
        except EOFError:
            print("\nNo input file provided. Exiting.")
            return

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
    diagram_path = render_diagram(diagram, output_file=output_file, options=options)
    print(f"Diagram generated at: {diagram_path}")

if __name__ == "__main__":
    main()
