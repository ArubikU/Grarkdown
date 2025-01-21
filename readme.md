# Grarkdown: Formato Markdown Avanzado para Diagramas

Grarkdown es un formato personalizado de Markdown diseñado para estructurar y generar diagramas avanzados usando Graphviz. Este formato es ideal para representar clases, relaciones y diagramas jerárquicos de manera sencilla, estructurada y estilizada.

---

## **Estructura del Formato Grarkdown**

Cada elemento del diagrama sigue una estructura organizada. A continuación, se describen las secciones disponibles:

### **Cabecera de Elemento**

```markdown
# {NombreClase} [ClaveUnica]
```
- `{NombreClase}`: Nombre de la clase o nodo.
- `[ClaveUnica]`: Identificador único que conecta este nodo con otros.

---

### **Atributos o Variables**

```markdown
## VAR
- nombreTipoAtributo tipoDato
## END VAR
```
- `nombreTipoAtributo`: Nombre del atributo.
- `tipoDato`: Tipo de dato asociado (e.g., `int`, `string`, etc.).

---

### **Funciones o Métodos**

```markdown
## FUNC
- nombreFuncion(parametros) tipoRetorno
## END FUNC
```
- `nombreFuncion`: Nombre de la función.
- `parametros`: Parámetros de entrada, incluyendo su tipo.
- `tipoRetorno`: Tipo de dato que devuelve la función.

---

### **Relaciones**

```markdown
## F_RELA
- TIPO [ClaveUnicaDestino] {Etiqueta}
## END F_RELA
```
- `TIPO`: Tipo de relación:
  - `TO`: Relación hacia otro nodo.
  - `FROM`: Relación desde otro nodo.
  - `BI`: Relación bidireccional entre dos nodos.
- `[ClaveUnicaDestino]`: Clave única del nodo relacionado.
- `{Etiqueta}`: Descripción opcional de la relación.

---

### **Parametros Opcionales**

```markdown
### OPT COLOR FFFFFF
```
- `FFFFFF`: Código hexadecimal del color para personalizar el nodo.

---

## **Ejemplo Completo**

```markdown
# {Producto} [PR]
## VAR
- uuid string
- nombre string
- precio float
## END VAR
## FUNC
- calcularStock void
- obtenerPrecio float
## END FUNC
## F_RELA
- TO [BE] {Clasificación}
- TO [AL] {Clasificación}
## END F_RELA
```

Este ejemplo define una clase `Producto` con atributos, funciones y relaciones hacia `Bebida` (`[BE]`) y `Alimento` (`[AL]`).

---

## **Cómo Utilizar Grarkdown**

1. **Escribir el Formato**:
   - Escribe el contenido en un archivo de texto con la extensión `.md`.
   - Sigue las estructuras definidas para las cabeceras, variables, funciones y relaciones.

2. **Procesar el Archivo**:
   - Usa el script de Python asociado al repositorio para convertir el contenido en un diagrama de Graphviz.

   ```bash
   python grarkdown_processor.py --input archivo.md --output diagrama.png
   ```

3. **Opciones Avanzadas**:
   - Personaliza el diseño del diagrama con opciones adicionales como:
     - `rankdir`: Direccionamiento del grafo (`TB`, `LR`).
     - `nodesep`: Separación entre nodos.
     - `ranksep`: Separación entre niveles.

   ```bash
   python grarkdown_processor.py --input archivo.md --output diagrama.png --rankdir LR --nodesep 0.5 --ranksep 1.0
   ```

4. **Visualización**:
   - El diagrama generado estará disponible como archivo `.png` en el directorio especificado.

## **Contribuciones**

¡Grarkdown está en constante evolución! Si deseas contribuir con ideas, mejoras o reportar errores:
- Crea un Issue o Pull Request en el repositorio de GitHub: [Grarkdown en GitHub](https://github.com/ArubikU/Grarkdown)

---

## **Licencia**

Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo y modificarlo según tus necesidades.

---

Con Grarkdown, estructurar y visualizar información jerárquica nunca fue tan sencillo. ¡Empieza a diagramar ahora! 🚀

