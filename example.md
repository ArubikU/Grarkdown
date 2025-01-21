# {Producto} [PR]
## VAR
- uuid string
- nombre string
- precio float
- stock int
## END VAR
## FUNC
- calcularStock void
- obtenerPrecio float
## END FUNC
## F_RELA
- TO [BE] {Clasificación}
- TO [AL] {Clasificación}
## END F_RELA

# {Bebida} [BE]
## VAR
- gasificada boolean
- mililitros int
## END VAR
## FUNC
- verificarGasificada boolean
- obtenerCantidad int
## END FUNC
## F_RELA
- FROM [PR] {Generalización}
## END F_RELA

# {Alimento} [AL]
## VAR
- calorías int
- tiempoVencimiento int
## END VAR
## FUNC
- calcularCalorías void
- verificarVencimiento boolean
## END FUNC
## F_RELA
- FROM [PR] {Generalización}
- TO [SA] {Sándwich}
## END F_RELA

# {Sándwich} [SA]
### OPT COLOR FFC0CB
## VAR
- componentes List<String>
## END VAR
## FUNC
- agregarComponente void
- obtenerComponentes List<String>
## END FUNC
## F_RELA
- FROM [AL] {Generalización}
## END F_RELA

# {Vendedora} [VN]
### OPT COLOR BAFFC9
## VAR
- codigo string
- nombres string
- direccion string
- horario string
- ventas List<Venta>
## END VAR
## FUNC
- registrarVenta void
- calcularTotalVentas float
## END FUNC
## F_RELA
- TO [VN] {Asocia ventas}
## END F_RELA

# {Venta} [VE]
## VAR
- codigo string
- fecha Date
- vendedora Vendedora
- productos List<Producto>
- total float
## END VAR
## FUNC
- calcularTotal float
- agregarProducto void
## END FUNC
## F_RELA
- FROM [VN] {Pertenece a}
- TO [PR] {Incluye}
## END F_RELA
