# Grarkdown

Grarkdown is a lightweight tool to generate beautiful, structured diagrams from a simple, Markdown-like syntax. It leverages the power of Graphviz to render complex entity-relationship diagrams, system architectures, or flowcharts directly into SVG format, with full support for CSS styling.

## Key Features

- **Markdown-based Syntax:** Define nodes, attributes, and relationships using an intuitive, text-based format.
- **SVG Output:** Generates clean, scalable SVG diagrams ready for the web.
- **CSS Styling:** Apply custom styles using external or inline stylesheets. Assign CSS classes to nodes, edges, and clusters.
- **Node Clustering:** Group related nodes into visual clusters with their own styles, including nested clusters.
- **Rich Node Content:** Nodes can include descriptions, variables, and functions.
- **Flexible Options:** Customize node colors, shapes, arrow types, and even embed images.

## Gallery

### Example 1: Styled Entity Relationship Diagram
![Entity Relationship Diagram](https://raw.githubusercontent.com/ArubikU/Grarkdown/main/example_svg.svg)

<details>
<summary>View Grarkdown source code</summary>

```markdown
### STYLESHEET
/* Inline CSS to style nodes and edges in the SVG */
.entity rect {
  fill: #e6f0ff;
  stroke: #3070f0;
  stroke-width: 1.5px;
}
.highlight path {
  stroke: #ff5722;
  stroke-width: 2px;
}
.note text {
  font-style: italic;
  fill: #666;
}
### END STYLESHEET

# {Customer} [cust]
### OPT DESC "A customer entity"
### OPT CLASS entity
### OPT CLUSTER Core [class=core, style=rounded, color=4A90E2, bgcolor=EAF2FF]
## VAR
- customer_id: int (PK)
- email: string
- name: string
## END VAR
## F_RELA
- TO [order] {places} [style=bold, class=highlight]
## END F_RELA

# {Order} [order]
### OPT CLASS entity
### OPT CLUSTER Core
## VAR
- order_id: int (PK)
- customer_id: int (FK)
- total: decimal
- created_at: datetime
## END VAR
## F_RELA
- FROM [cust] {by}
- TO [payment] {paid with} [style=dashed]
## END F_RELA

# {Payment} [payment]
### OPT CLASS note
### OPT COLOR FFF3CD
### OPT CLUSTER Billing [class=billing, style=dashed, color=FFA000]
## VAR
- payment_id: int (PK)
- order_id: int (FK)
- method: string
- amount: decimal
- status: string
## END VAR
```
</details>

### Example 2: Nested Clusters
![Nested Clusters Diagram](https://raw.githubusercontent.com/ArubikU/Grarkdown/main/nested_diagram.svg)

<details>
<summary>View Grarkdown source code</summary>

```markdown
### STYLESHEET
.cluster.parent > polygon {
  stroke: #FF5722;
  fill: #FFF3E0;
  stroke-width: 2px;
  stroke-dasharray: 8, 4;
}
.cluster.child > polygon {
  stroke: #4CAF50;
  fill: #E8F5E9;
  stroke-width: 1.5px;
}
### END STYLESHEET

# {Component A} [compA]
### OPT CLUSTER ParentCluster [class=parent]

# {Component B} [compB]
### OPT CLUSTER ParentCluster>ChildCluster [class=child]

# {Component C} [compC]
### OPT CLUSTER ParentCluster>ChildCluster

# {Component D} [compD]
### OPT CLUSTER OtherCluster

## F_RELA
- TO [compB] {connects to}
## END F_RELA
```
</details>

### Example 3: Deep Nested Architecture
![Deep Nested Architecture](https://raw.githubusercontent.com/ArubikU/Grarkdown/main/deep_nested_diagram.svg)

<details>
<summary>View Grarkdown source code</summary>

```markdown
# {Service A} [serviceA]
### OPT CLUSTER Services>Core

# {Service B} [serviceB]
### OPT CLUSTER Services>Core>Database [style=dashed, color=blue]

# {Service C} [serviceC]
### OPT CLUSTER Services>API

# {External Service} [ext]
### OPT CLUSTER External

## F_RELA
- TO [serviceB]
## END F_RELA
```
</details>

### Example 4: Arrowheads and Tails
![Arrowheads and Tails](https://raw.githubusercontent.com/ArubikU/Grarkdown/main/example_arrows.svg)

<details>
<summary>View Grarkdown source code</summary>

```markdown
# {Client} [cli]
### OPT CLUSTER Network

# {Gateway} [gw]
### OPT CLUSTER Network

# {Service} [svc]
### OPT CLUSTER Compute
## F_RELA
- TO [gw] {request} [style=bold, color=#1976D2, arrowhead=vee]
- TO [svc] {forward} [style=dashed, arrowhead=diamond]
- BI [cli] {callback} [color=#2E7D32, arrowhead=normal, arrowtail=dot]
## END F_RELA
```
</details>

## Getting Started

### Prerequisites

- Python 3.x
- Graphviz: You must have the Graphviz command-line tools installed on your system. You can download it from the [official Graphviz website](https://graphviz.org/download/).

### Usage

Run the script from your terminal, providing an input Grarkdown file and an output file name.

```bash
# Generate a diagram from a .md file
python main.py <input_file.md> -o <output_file_name>
```

**Example:**

```bash
# This will generate demo.svg in your current directory
python main.py example_svg.md -o demo
```

## Basic Syntax Example

```markdown
# {User} [user]
### OPT CLASS entity
### OPT CLUSTER Authentication
## VAR
- user_id: int
- email: string
## END VAR
## F_RELA
- TO [session] {creates} [class=highlight]
## END F_RELA

# {Session} [session]
### OPT CLASS volatile
### OPT CLUSTER Authentication
## VAR
- session_token: string
- expires_at: datetime
## END VAR
```

This simple example defines two nodes, `User` and `Session`, groups them in an "Authentication" cluster, and creates a relationship between them.

## Full Documentation

For a complete guide to the Grarkdown syntax, including clustering, styling with CSS, and all available options, please refer to the **[Grarkdown Wiki](wiki.md)**.
