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
