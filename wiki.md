# Grarkdown Wiki

Welcome to the official documentation for Grarkdown. This guide provides a comprehensive overvieYou can group related nodes into a visual container called a cluster. This is done with the `CLUSTER` option. To create nested clusters, use the `>` separator.

```markdown
### OPT CLUSTER ClusterName [style=rounded, class=my-cluster, color=4A90E2, bgcolor=EAF2FF]
### OPT CLUSTER L1>L2>L3 [style=dashed]
```
-   `ClusterName`: The name displayed as the cluster's title.
-   `L1>L2>L3`: Defines a `L3` cluster inside `L2`, which is inside `L1`. You can use as many levels as you need.
-   **Attributes**:
    -   `style`: `rounded`, `filled`, `dashed`.yntax and features for creating structured diagrams.

## Table of Contents
1.  [Introduction](#introduction)
2.  [Getting Started](#getting-started)
3.  [Core Concepts](#core-concepts)
    -   [Node Definition](#node-definition)
    -   [Node Options (`### OPT`)](#node-options-opt)
    -   [Variables (`## VAR`)](#variables-var)
    -   [Functions (`## FUNC`)](#functions-func)
    -   [Relationships (`## F_RELA`)](#relationships-f_rela)
4.  [Advanced Features](#advanced-features)
    -   [Clustering Nodes](#clustering-nodes)
    -   [Styling with CSS](#styling-with-css)
5.  [Full Syntax Example](#full-syntax-example)
6.  [Command-Line Usage](#command-line-usage)

---

## Introduction

Grarkdown is a tool that converts a custom, Markdown-like syntax into a Graphviz-powered SVG diagram. It's designed for developers, architects, and anyone who needs to create clear, structured, and visually appealing diagrams from a simple text-based format.

## Getting Started

To generate a diagram, you need Python and Graphviz installed. Then, run the main script with your input file.

```bash
python main.py <your_file.md> -o <output_name>
```
This will generate `<output_name>.svg`.

## Core Concepts

A Grarkdown file is composed of one or more node blocks. Each block defines an entity in your diagram.

### Node Definition

A node is the fundamental building block. It is defined with a header containing a display name and a unique key.

```markdown
# {DisplayName} [unique_key]
```
-   `{DisplayName}`: The name that appears at the top of the node. Can contain spaces and special characters.
-   `[unique_key]`: A short, unique identifier used to form relationships. Must not contain spaces.

### Node Options (`### OPT`)

Immediately after the node header, you can add an optional `### OPT` block to customize the node's appearance and metadata.

```markdown
# {My Node} [node1]
### OPT COLOR FFF3CD
### OPT SHAPE component
### OPT CLASS important
### OPT DESC "This node represents a critical component."
```

Available options:
-   `COLOR <hex>`: Sets the node's background fill color (e.g., `FFF3CD`).
-   `SHAPE <name>`: Sets the node's shape. Common Graphviz shapes like `box`, `ellipse`, `component`, `database` are supported. Defaults to `record`.
-   `IMAGE <url>`: Embeds an image in the node. The node's label will be minimal.
-   `CLASS <name>`: Assigns a CSS class to the node's SVG group (`<g>`) for styling.
-   `DESC "<text>"`: Adds a short description below the node's title. Quotes are optional but recommended for descriptions with special characters.

### Variables (`## VAR`)

The `## VAR` block lists the attributes or properties of the node. This block is optional.

```markdown
## VAR
- attribute_name: string
- item_count: int
## END VAR
```

### Functions (`## FUNC`)

The `## FUNC` block lists methods or functions. If this block is empty or omitted, it will not be rendered in the final diagram.

```markdown
## FUNC
- calculateTotal() -> float
- processItems(items: List)
## END FUNC
```

### Relationships (`## F_RELA`)

The `## F_RELA` block defines how the node connects to others. This block is optional.

```markdown
## F_RELA
- TO [target_key] {Label} [style=dashed, color=blue, class=edge-class]
- FROM [source_key] {Label}
- BI [other_key] {Label}
## END F_RELA
```
-   **Direction**:
    -   `TO`: Edge from this node to `target_key`.
    -   `FROM`: Edge from `source_key` to this node.
    -   `BI`: A bidirectional edge is created (rendered as two separate directed edges).
-   **Label**: `{Label}` is an optional text label for the edge.
-   **Attributes**: `[key=value, ...]` are optional Graphviz attributes for the edge.
    -   `style`: `dashed`, `bold`, `dotted`.
    -   `color`: Edge color (e.g., `red`, `#FF0000`).
    -   `class`: A CSS class for the edge's SVG group (`<g>`).
    -   `arrowhead`: Arrow shape at the head. Common values: `normal`, `inv`, `dot`, `invdot`, `odot`, `invodot`, `none`, `tee`, `empty`, `invempty`, `diamond`, `odiamond`, `ediamond`, `crow`, `box`, `obox`, `open`, `halfopen`, `vee`.
    -   `arrowtail`: Arrow shape at the tail. Uses the same value set as `arrowhead`. For `TO`/`FROM`, specifying `arrowtail` implies arrows on both ends.

Examples:

```markdown
- TO [B] {to B} [arrowhead=vee, color=#1976D2]
- FROM [A] {from A} [arrowhead=normal]
- BI [C] {sync} [arrowhead=normal, arrowtail=dot]
```

---

## Advanced Features

### Clustering Nodes

You can group related nodes into a visual container called a cluster. This is done with the `CLUSTER` option. To create nested clusters, use the `Parent>Child` syntax.

```markdown
### OPT CLUSTER ClusterName [style=rounded, class=my-cluster, color=4A90E2, bgcolor=EAF2FF]
### OPT CLUSTER ParentCluster>ChildCluster [style=dashed]
```
-   `ClusterName`: The name displayed as the cluster's title. The `` is optional.
-   `ParentCluster>ChildCluster`: Defines a `ChildCluster` inside a `ParentCluster`.
-   **Attributes**:
    -   `style`: `rounded`, `filled`, `dashed`.
    -   `class`: A CSS class for the cluster's SVG container.
    -   `color`: The border color of the cluster.
    -   `bgcolor`: The background fill color of the cluster.

All nodes that share the same `ClusterName` will be rendered inside the same container. The style attributes are taken from the *first* node that defines them for that cluster.

### Styling with CSS

Grarkdown's SVG output allows for powerful styling via CSS. You can provide styles in two ways:

1.  **External Stylesheet**: Link a CSS file at the top of your `.md` file. The path is resolved relative to your current directory.
    ```markdown
    ### STYLESHEET path/to/my-styles.css
    ```

2.  **Inline Stylesheet**: Embed CSS rules directly inside a `STYLESHEET` block.
    ```markdown
    ### STYLESHEET
    /* This CSS will be embedded in the SVG */
    .entity rect { fill: #e8f0ff; }
    .highlight path { stroke: #d9534f; stroke-width: 2.5px; }
    g.cluster.core > polygon { stroke: #4A90E2; fill: #EAF2FF; }
    ### END STYLESHEET
    ```

---

## Full Syntax Example

This example demonstrates clustering, styling, and various node options.

```markdown
### STYLESHEET
/* Inline styles for our diagram */
.entity rect { fill: #e6f0ff; stroke: #3070f0; stroke-width: 1.5px; }
.highlight path { stroke: #ff5722; stroke-width: 2px; }
.note text { font-style: italic; fill: #666; }
g.cluster.core > polygon { stroke-width: 2px; }
### END STYLESHEET

# {Customer} [cust]
### OPT DESC "A customer entity"
### OPT CLASS entity
### OPT CLUSTER Core [class=core, style=rounded, color=4A90E2, bgcolor=EAF2FF]
## VAR
- customer_id: int (PK)
- email: string
## END VAR
## F_RELA
- TO [order] {places} [style=bold, class=highlight]
## END F_RELA

# {Order} [order]
### OPT CLASS entity
### OPT CLUSTER Core
## VAR
- order_id: int (PK)
- total: decimal
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
- status: string
## END VAR
```

## Command-Line Usage

The script accepts the following arguments:

-   `file`: (Required) The path to the input `.md` file.
-   `-o`, `--output`: The desired name for the output SVG file (without the extension). Defaults to `output_diagram`.
-   `--rankdir`: Graph layout direction (`LR`, `TB`). Default: `LR`.
-   `--nodesep`: Node separation. Default: `0.6`.
-   `--ranksep`: Rank separation. Default: `0.7`.

**Example:**
```bash
python main.py example_svg.md -o my_awesome_diagram
```
This generates `my_awesome_diagram.svg`.
