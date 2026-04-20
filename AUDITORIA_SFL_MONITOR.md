# INFORME DE AUDITORÍA FUNCIONAL - SFL MONITOR

**Fecha de auditoría:** 18 de abril de 2026  
**Auditor:** QA Engineer / Senior Full Stack Developer  
**Versión analizada:** Sistema completo con Dashboard, Operaciones y Configuración

---

## 1. RESUMEN EJECUTIVO

### Estado general del sistema
El sistema se encuentra en un **estado funcional pero con debilidades importantes**. La arquitectura es correcta, la persistencia funciona, pero hay varios puntos de fricción que afectan la experiencia operativa.

### Nivel de madurez
- **Funcionalidad core:** ✅ Operativa
- **Persistencia:** ✅ Funciona correctamente
- **UX/UI:** ⚠️ Necesita refinamiento
- **Lógica comercial:** ⚠️ Inconsistencias en datos de prueba
- **Robustez:** ⚠️某些 puntos frágiles

### Principales riesgos
1. **Datos de prueba irrealistas** - Los precioscompetidor están mal cargados (6 pesos, 20.000 pesos), lo que genera estados y recomendaciones incorrectas
2. **Falta de validación** - No hay validación de rango en precios
3. **UX confusa** - La experiencia tiene puntos de fricción

---

## 2. RECORRIDO COMO USUARIO

### Dashboard
**Acciones realizadas:**
- Abrí la app y vi el hero con chips de métricas
- Los KPIs muestran: productos activos (2), dólar modo (OFICIAL), referencia ($ 1.430)
- Probé filtros: competidor, estado, ordenar por, búsqueda
- La búsqueda funciona bien (encuentra por código, descripción, competidor)
- La tabla muestra 2 productos activos con acción y motivo
- Las alertas muestran productos en rojo
- Las prioridades muestran productos a revisar

**Observaciones:**
- ✅ La tabla es clara con columnas de acción y motivo
- ✅ La búsqueda filtra correctamente
- ⚠️ Los productos tienen estados ROJO pero no está claro por qué (los datos de prueba están mal)
- ⚠️ La diferencia de 499.733% para el producto 67890 es absurda (precio competidor = 6 pesos)

### Operaciones

**1. Actualización Rápida**
- Seleccioné producto 12345||REDLENIC
- El selector muestra productos activos e inactivos ✅
- Pude actualizar precio de 15.000 a 20.000 ✅
- El sistema movió el anterior a "anterior" correctamente ✅
- Guardó y persistió correctamente ✅

**2. Alta de Producto**
- Intenté crear un producto nuevo con código duplicado
- Mostró warning "El producto ya existe" ✅
- Los campos se ven bien

**3. Editar Producto**
- Seleccioné un producto
- Pude modificar precio Reyes, costo USD, precio competidor, margen mínimo
- Guardó correctamente ✅

**4. Activar/Desactivar**
- Desactivé el producto 12345
- Guardó correctamente (ahora activo = NO) ✅
- Lo reactivé ✅
- El filtro "Todos/Activos/Inactivos" funciona ✅

### Configuración
- Los valores actuales se leen correctamente
- Cambié dólar modo de "oficial" a "blue" ✅
- Cambió correctamente ✅
- Volví a "oficial" ✅

---

## 3. LO QUE FUNCIONA BIEN

| Funcionalidad | Estado | Detalle |
|--------------|--------|---------|
| Carga de datos | ✅ Bien | Excel se lee correctamente |
| Persistencia | ✅ Bien | Los cambios se guardan en Excel |
| Filtros de dashboard | ✅ Bien | Competidor, estado, búsqueda funcionan |
| Búsqueda | ✅ Bien | Filtra por código, descripción, competidor |
| Actualización rápida | ✅ Bien | Guarda correctamente, mueve anterior |
| Cambio de estado | ✅ Bien | Activa/desactiva correctamente |
| Activar/Desactivar | ✅ Bien | Filtros funcionan, persistencia OK |
| Configuración | ✅ Bien | Cambia y persiste correctamente |
| Exportar CSV | ✅ Bien | Descarga los datos visibles |
| Vista ampliada | ✅ Bien | Alterna filas 10/15 |
| Clave operativa | ✅ Bien | Formato codigo\|\|competidor es robusto |

---

## 4. PROBLEMAS ENCONTRADOS

### PROBLEMA 1: Datos de prueba irrealistas

**Título:** Precios de competidor no tienen validación ni coherencia comercial

**Descripción:** Los precios de competidor en el Excel están mal cargados:
- Producto 12345: precio competidor = 20.000 (vs precio Reyes = 45.995)
- Producto 67890: precio competidor = 6 (vs precio Reyes = 29.990)

Esto genera:
- Diferencia del 130% y 499.733% (absurdo comercialmente)
- Estados ROJO constantes aunque el negocio puede ser rentable
- Acciones recomendadas "Revisar precio" cuando el problema es el dato

**Cómo reproducirlo:** Abrir dashboard y ver los estados

**Área afectada:** Datos en Excel / Lógica de cálculos

**Severidad:** ALTA

**Impacto de negocio:** La clienta puede tomar decisiones basadas en datos incorrectos. Si los datos de prueba pasan a producción sin limpieza, todo el análisis queda invalinado.

**Causa probable:** El Excel se populó con datos de prueba sin validación.

**Recomendación:** 
- Limpiar los datos de prueba en el Excel antes de uso real
- Agregar validación de rango en precios (no permitir precios de competidor menores al 10% del precio Reyes sin warning)

---

### PROBLEMA 2: Acción recomendada confusa cuando el dato está mal

**Título:** La acción recomendada dice "Revisar precio" pero el problema es el dato del competidor

**Descripción:** Para el producto 67890, el sistema recomienda "Revisar precio" con motivo "Precio 499733.3% encima del competidor". Pero esto no es un problema de pricing - es un problema de dato mal cargado (6 pesos vs 29.990).

**Cómo reproducirlo:** Ver producto 67890 en dashboard

**Área affected:** Lógica comercial en calculations.py

**Severidad:** MEDIA

**Impacto de negocio:** Mensajes confusos que no guían correctamente la acción

**Recomendación:** 
- Agregar validación de coherencia de datos
- Si precio competidor < precio Reyes * 0.1, mostrar "Verificar dato competidor" en lugar de "Revisar precio"

---

### PROBLEMA 3: No hay forma de ver el dato anterior del competidor

**Título:** El usuario no puede ver fácilmente qué precio tenía antes el competidor

**Descripción:** El campo precio_competidor_anterior_ars existe pero no se muestra en ningún lado de la UI. En actualización rápida hay un checkbox "Mover actual a anterior" pero no hay forma de ver el valor anterior.

**Cómo reproducirlo:** Ir a Operaciones > Actualización Rápida

**Área afectada:** UI / Operaciones

**Severidad:** MEDIA

**Impacto de negocio:** No se puede hacer seguimiento de la variación del competidor

**Recomendación:** Mostrar "Precio anterior" en el panel de actualización rápida

---

### PROBLEMA 4: El KPI "Sin dato" puede confundirse

**Título:** El filtro de "Sin Dato" en sidebar muestra "sin_dato" (minúsculas) como string literal

**Descripción:** En la línea del código hay un filtro que busca "sin_dato" pero el estado real es "SIN_DATO" (mayúsculas). Esto podría no filtrar correctamente.

**Cómo reproducirlo:** En sidebar hay un filtro que usa "sin_dato"

**Área affected:** Dashboard / Filtros

**Severidad:** BAJA

**Impacto de negocio:** Posible bug de filtro

**Recomendación:** Estandarizar el uso de estados en mayúsculas

---

### PROBLEMA 5: Descripción del producto tiene encoding raro

**Título:** Los caracteres especiales en descripciones se ven mal

**Descripción:** "Pava eléctrica" aparece como "Pava el�ctrica"

**Cómo reproducirlo:** Ver la tabla de productos

**Área afectada:** Datos en Excel / Encoding

**Severidad:** BAJA

**Impacto de negocio:** Legibilidad de descripciones comprometida

**Recomendación:** Revisar encoding del Excel o corregir las descripciones

---

### PROBLEMA 6: No hay diferenciación visual clara en la tabla para productos inactivos

**Título:** Los productos inactivos se ven igual que los activos en la tabla

**Descripción:** Cuando se muestra "todos los productos" en alguna vista futura, no hay forma de saber cuáles están activos/inactivos sin ir a la operación correspondiente.

**Cómo reproducirlo:** No es reproducible actualmente porque la tabla solo muestra activos

**Severidad:** BAJA

**Impacto de negocio:** Limitación para expansión futura

**Recomendación:** Agregar columna de estado en la tabla si se permite mostrar inactivos

---

## 5. RIESGOS DE PRODUCCIÓN

| Riesgo | Descripción | Severidad | Impacto |
|--------|-------------|-----------|---------|
| Datos mal populateados | Si el Excel se usa con datos de prueba sin limpiar, todo el análisis es incorrecto | ALTA | Crítico |
| Sin backup | Si el Excel se corrompe, no hay forma de recuperar | MEDIA | Alto |
| Persistencia bloqueante | Si el Excel está abierto, el write falla silenciosamente | MEDIA | Medio |
| Sin logs | No hay forma de auditar qué cambió y cuándo | BAJA | Bajo |

---

## 6. MEJORAS PRIORITARIAS

### PRIORIDAD 1: Limpiar datos de prueba del Excel
- Eliminar o corregir los precios de competidor irrealistas
- Dejar datos que representen un escenario real

### PRIORIDAD 2: Agregar validación de datos
- Warning si precio competidor < 10% de precio Reyes
- Warning si margen real > 200% (posible error de carga)

### PRIORIDAD 3: Mostrar precio anterior en actualización rápida
- Agregar visualización del valor anterior
- Facilitar seguimiento de variaciones

### PRIORIDAD 4: Mejorar mensaje de acción recomendada
- Distinguir entre "dato mal cargado" y "precio mal fijado"
- Mensajes más específicos y accionables

### PRIORIDAD 5: Agregar indicador de cambio en la tabla
- Columna con "variación" si hay cambio vs anterior

---

## 7. VEREDICTO FINAL

### Estado actual: **USO CONTROLADO**

La app está operativa para uso real, pero con estas condiciones:

✅ **Para usar ahora:**
- Dashboard funciona correctamente
- Filtros y búsquedas operan bien
- Operaciones de cambio funcionan
- Persistencia es confiable
- La lógica de acciones está correctamente implementada

⚠️ **Con precaución:**
- Limpiar datos de prueba antes de uso productivo
- Validar que los precios de competidor sean reales
- Explicar a la clienta que los estados/acciones dependen de datos correctos

⚠️ **Antes de producción:**
- Realizar limpieza del Excel
- Agregar validaciones de rango
- Considerar agregar logs de auditoría

### Recomendación final
**Aprobado para uso controlado** con la condición de que los datos del Excel sean真实的 y estén validados. La estructura del sistema es sólida; el riesgo principal es la calidad de los datos de entrada.

---

*Fin del informe de auditoría*