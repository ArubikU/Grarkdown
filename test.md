# {User} [user]
### OPT CLASS entity
### OPT DESC "A user interacts with the system"
### OPT CLUSTER Actors [style=rounded, color=4A90E2, bgcolor=EAF2FF]
## VAR
- id: int (PK)
- name: string
## END VAR
## F_RELA
- TO [s1] {uses} [style=bold, color=#1976D2, arrowhead=vee]
- TO [s2] {uses} [style=bold, color=#1976D2, arrowhead=vee]
## END F_RELA

# {Server1} [s1]
### OPT CLASS entity
### OPT IMAGE https://cdn2.iconfinder.com/data/icons/whcompare-isometric-web-hosting-servers/50/value-server-512.png?width=1&height=1
### OPT CLUSTER Core [class=core, style=dashed, color=FF5722, bgcolor=FFF3CD]
# {Server2} [s2]
### OPT CLASS entity
### OPT IMAGE https://cdn2.iconfinder.com/data/icons/whcompare-isometric-web-hosting-servers/50/value-server-512.png?width=1&height=1
### OPT CLUSTER Core 
