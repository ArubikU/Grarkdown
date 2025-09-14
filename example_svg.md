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

### STYLESHEET example_styles.css

# {Customer} [cust]
### OPT DESC "A customer entity"
### OPT CLASS entity
### OPT CLUSTER Core [class=core, style=rounded, color=4A90E2, bgcolor=EAF2FF]
## VAR
- customer_id: int (PK)
- email: string
- name: string
## END VAR
## FUNC
## END FUNC
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
