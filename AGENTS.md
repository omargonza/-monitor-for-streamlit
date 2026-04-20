# AGENTS.md

## Proyecto
**SFL Monitor**  
Sistema interno de monitoreo competitivo, rentabilidad y apoyo a decisiones comerciales para el área de compras/pricing.

---

## Perfil de actuación obligatorio

A partir de este proyecto, actuar siempre como:

- **senior full stack developer**
- **especialista en internal tools**
- **diseñador de producto orientado a herramientas operativas**
- **ingeniero de software con criterio fuerte de calidad**
- **product thinker con foco en compras / pricing / rentabilidad**
- **constructor de software de negocio, no de demos**
- **responsable de UX honesta, consistente y verificable**

## Nivel de exigencia esperado

No construir soluciones que solo **parezcan** buenas.  
Priorizar siempre soluciones:

- reales
- usables
- verificadas
- mantenibles
- operativas
- consistentes con los datos reales
- alineadas con la operatoria de compras/comercial
- defendibles frente a un usuario de negocio

No agregar:

- features fake
- interacciones decorativas
- botones que no funcionen de verdad
- hacks frágiles
- ayuda contextual que describa funciones inexistentes
- mejoras visuales que oculten problemas funcionales
- sobreingeniería sin retorno operativo

Preferir siempre:

- menos features, pero bien resueltas
- UX honesta
- persistencia confiable
- lógica clara
- criterio comercial aplicado
- consistencia entre UI, datos y negocio
- validación real antes de dar algo por terminado

---

## Objetivo del sistema

La clienta selecciona manualmente qué productos quiere monitorear y carga manualmente el precio de la competencia.  
El sistema **NO** hace scraping.  
El sistema se encarga de:

- leer y persistir datos en Excel
- calcular métricas comerciales
- mostrar dashboard ejecutivo
- permitir operación desde UI
- priorizar revisión
- ayudar a decisiones de compras/pricing
- reducir trabajo manual repetitivo
- dar lectura comercial accionable, no solo mostrar datos

---

## Este sistema NO es

Esto **no** es:

- una demo visual
- una planilla maquillada
- un experimento de scraping
- una app académica
- una prueba técnica
- una landing
- una UI “linda” sin valor operativo

Esto **sí** es:

- una herramienta operativa interna
- una internal tool de compras/comercial
- un sistema de apoyo a pricing y rentabilidad
- una app que debe ayudar a decidir más rápido y mejor

---

## Fuente de verdad

La fuente de verdad es el archivo Excel:

`reyes_monitoreo_base_v1.xlsx`

Hojas relevantes:

- `PRODUCTOS_REYES`
- `MONITOREO_ACTIVO`
- `CONFIG`

## Regla crítica de integración

**Nunca asumir columnas teóricas si el Excel real usa otros nombres.**  
Antes de tocar lectura, escritura, cálculos o UI:

1. inspeccionar estructura real del Excel
2. validar nombres reales de columnas
3. adaptar el código a los datos reales
4. no inventar columnas ni renombrar arbitrariamente si no hace falta

---

## Enfoque descartado

Este proyecto **abandonó completamente** el scraping de competidores.

No reintroducir:

- requests a sitios de competidores
- login automatizado
- parsing HTML
- archivos de inspección
- matching por web
- automatización de captura desde páginas ajenas

Si una tarea futura intenta volver a eso:
- detenerse
- mantener el enfoque actual
- no reabrir scraping salvo instrucción explícita del usuario

---

## Criterio de producto esperado

Cada mejora debe responder al menos una de estas preguntas:

- ¿ayuda a decidir mejor?
- ¿ahorra tiempo operativo real?
- ¿reduce error humano?
- ¿hace más clara una acción importante?
- ¿mejora la lectura comercial de un producto?
- ¿facilita actualizar precios, márgenes o prioridades?
- ¿ayuda a detectar problemas antes?

Si la respuesta es **no**, no priorizar esa mejora.

## Criterio específico para compras/pricing

Pensar siempre como una persona que necesita:

- ver rápido qué revisar
- entender si está arriba o abajo de la competencia
- saber si su margen está sano o en riesgo
- saber si faltan datos
- decidir si mantener, revisar, subir o bajar precio
- actualizar información sin romper nada
- trabajar con rapidez y claridad

No diseñar pensando en “mostrar todos los datos”.
Diseñar pensando en **facilitar decisiones operativas**.

---

## Lógica funcional del producto

### Qué hace la clienta
- elige qué productos quiere seguir
- puede modificar esa selección cuando quiera
- carga o actualiza manualmente el precio competidor
- puede cambiar dólar oficial / blue / modo
- puede activar o desactivar productos

### Qué hace el sistema
- calcula costo en ARS
- calcula ganancia en ARS
- calcula ganancia en USD
- calcula margen real %
- calcula diferencia vs competidor %
- calcula variación del competidor %
- calcula precio mínimo rentable
- calcula precio sugerido competitivo
- clasifica estado
- muestra alertas
- muestra prioridades
- sugiere lectura operativa
- guarda cambios en Excel

---

## Reglas de cálculo

### Dólar de referencia
Se toma desde `CONFIG`:

- `dolar_oficial`
- `dolar_blue`
- `dolar_modo`

Regla:
- si `dolar_modo = oficial` usar `dolar_oficial`
- si `dolar_modo = blue` usar `dolar_blue`

**Nunca hardcodear valores de dólar.**

### Fórmulas base
- `costo_ars = costo_usd * dolar_referencia`
- `ganancia_ars = precio_reyes_ars - costo_ars`
- `ganancia_usd = ganancia_ars / dolar_referencia`
- `margen_real_pct = ((precio_reyes_ars / costo_ars) - 1) * 100`
- `diferencia_vs_competidor_pct = ((precio_reyes_ars / precio_competidor_actual_ars) - 1) * 100`
- `variacion_competidor_pct = ((precio_competidor_actual_ars / precio_competidor_anterior_ars) - 1) * 100`
- `precio_minimo_rentable_ars = costo_ars * (1 + margen_minimo_pct / 100)`

### Precio sugerido competitivo
Regla esperada:
- si no hay precio competidor, usar el mínimo rentable
- si el precio competidor está por debajo del mínimo rentable, **no perforar** el mínimo rentable
- si el precio competidor permite competir sin romper rentabilidad, sugerir un valor levemente por debajo del competidor

Toda implementación debe ser:
- explícita
- consistente con README
- consistente con UI
- fácil de explicar

---

## Estados del sistema

Estados válidos:

- `VERDE`
- `AMARILLO`
- `ROJO`
- `SIN_DATO_COMPETIDOR`

### Lógica esperada
- `SIN_DATO_COMPETIDOR`: no hay `precio_competidor_actual_ars`
- `ROJO`: margen por debajo del mínimo o muy fuera de mercado
- `AMARILLO`: rentable pero ajustado
- `VERDE`: rentable y competitivo

## Regla UX crítica
Si no hay precio competidor:
- **no** clasificar como verde/amarillo/rojo normal
- usar siempre `SIN_DATO_COMPETIDOR`

---

## Valor operativo adicional esperado

Siempre que sume valor real, priorizar agregar lectura de negocio como:

- `accion_recomendada`
- `motivo_accion`
- `riesgo_comercial`
- `oportunidad_comercial`
- `necesita_dato_competidor`
- `margen_sano`
- `fuera_de_rango`

Ejemplos válidos de `accion_recomendada`:

- `Cargar dato competidor`
- `Mantener`
- `Revisar`
- `Bajar precio`
- `Subir precio`

No inventar recomendaciones arbitrarias.
Toda recomendación debe salir de una lógica clara y defendible.

---

## Persistencia en Excel

### Regla crítica de escritura
Al escribir en Excel:

- cargar la hoja real completa
- preservar todas las filas
- preservar todas las columnas existentes
- actualizar solo las celdas necesarias
- no perder productos inactivos
- no guardar usando un DataFrame filtrado como si fuera la hoja completa

### Separación obligatoria
Diferenciar siempre:

- lectura procesada para dashboard
- lectura cruda para persistencia

### Operaciones que deben ser seguras
- actualizar CONFIG
- insertar producto
- editar producto
- actualización rápida de precio competidor
- activar/desactivar producto

### Resultado esperado del guardado
Toda función de guardado debe devolver resultado explícito:

- `True` si guardó bien
- `False` o error controlado si falló

Nunca dejar retorno ambiguo.

### Regla de integridad
Antes de cerrar cualquier cambio que escriba Excel, verificar:

- que no se pierdan filas
- que no se pierdan columnas
- que no se dupliquen registros sin control
- que no se rompa la estructura real de `MONITOREO_ACTIVO`
- que la UI muestre éxito solo si guardó realmente

---

## UI / Dashboard

### Dirección visual obligatoria
La referencia visual es una **internal tool premium** estilo Retool:

- sobria
- clara
- ejecutiva
- moderna
- utilitaria
- con jerarquía visual fuerte

### No hacer
- UI default de Streamlit sin trabajar
- páginas largas llenas de bloques sueltos
- exceso de emojis
- colores gritones
- formularios improvisados
- dataframe crudo como experiencia principal
- acciones ambiguas
- tooltips que expliquen cosas inexistentes
- “features” falsas con JS frágil

### Sí hacer
- sidebar clara
- header superior sólido
- KPI cards con buena jerarquía
- filtros visibles
- tabla central fuerte
- estados como badges/chips
- panel operativo separado del dashboard
- configuración separada
- spacing y padding cuidados
- affordance visual clara
- hover / focus / active states consistentes

### Estructura esperada
#### Dashboard
- resumen general
- filtros
- tabla principal
- alertas
- prioridades

#### Operaciones
- alta de producto
- edición de producto
- actualización rápida de precio competidor
- activar/desactivar

#### Configuración
- dólar oficial
- dólar blue
- modo de dólar

---

## Criterio UX obligatorio

### Regla de UX honesta
No agregar acciones, botones, ayudas o explicaciones para funciones que no existan o no funcionen de verdad.

No usar:
- interacciones fake
- botones decorativos
- hacks frágiles
- ayudas que describan cosas inexistentes
- affordances falsas

Toda acción visible debe:
- funcionar realmente
- tener sentido operativo
- estar alineada con los datos reales
- estar explicada con claridad si no es obvia

### Microayuda contextual
Agregar ayuda contextual cuando sume valor real, especialmente en:

- botones de guardar
- actualización rápida
- dólar oficial / blue / modo
- campos sensibles
- acciones de tabla
- alta / edición

La ayuda debe ser:
- breve
- clara
- no técnica
- orientada a negocio

### Affordance visual
Todo lo accionable debe sentirse accionable:
- cursor pointer
- hover real
- foco visible
- active state claro
- consistencia en interacción

---

## Tabla central: criterio obligatorio

La tabla central debe responder esta pregunta:

**“¿Cómo está este producto frente a competencia y rentabilidad, y qué conviene hacer?”**

### Debe priorizar
- código
- descripción
- competidor
- precio Reyes
- precio competidor
- diferencia %
- margen %
- ganancia
- mínimo rentable
- sugerido
- estado
- acción recomendada si existe

### No hacer con la tabla
- depender de iconos ambiguos como experiencia principal
- agregar acciones falsas con HTML/JS frágil
- explicar funciones inexistentes
- mostrar columnas irrelevantes primero

### Sí hacer con la tabla
- búsqueda real
- vista ampliada real si existe
- exportar CSV real
- ayuda alineada con acciones reales
- filtros honestos
- ordenar por campos coherentes con la tabla

---

## Convenciones de datos

### Clave operativa sugerida
Usar como clave del producto monitoreado:

`codigo_reyes + competidor`

No asumir que `codigo_reyes` solo es suficiente si hay varias comparaciones por competidor.

### Columnas reales importantes detectadas
Ejemplos de nombres reales usados en este proyecto:
- `precio_reyes_ars`
- `precio_competidor_actual_ars`
- `precio_competidor_anterior_ars`
- `costo_usd`
- `margen_minimo_pct`
- `margen_real_pct`
- `precio_minimo_rentable_ars`
- `precio_sugerido_competitivo_ars`

No reemplazar arbitrariamente `_ars` por nombres genéricos.

---

## Prioridades de desarrollo

### Antes de agregar features nuevas
1. confiabilidad de persistencia
2. coherencia de cálculos
3. consistencia de estados
4. UX/UI premium y clara
5. validaciones y mensajes de error
6. criterio comercial útil
7. operatoria sólida

### Orden recomendado de evolución
1. endurecer persistencia Excel
2. pulir edición/alta
3. historial visible
4. mejores filtros y acciones por fila
5. lectura comercial / recomendaciones
6. exportación / reportes
7. carga masiva si el usuario la pide

---

## Regla de validación antes de cerrar una tarea

Antes de dar una mejora por terminada, verificar siempre:

- que funcione de verdad
- que la UI coincida con la lógica real
- que no haya acciones ambiguas
- que los textos de ayuda describan funciones existentes
- que filtros, ordenamientos y columnas estén alineados
- que no se haya roto persistencia ni estructura del Excel
- que no se haya agregado humo visual sin valor operativo
- que la mejora aporte algo concreto a compras/comercial

---

## Guardrails para OpenCode

### Siempre hacer
- revisar estructura real antes de asumir
- mantener enfoque sin scraping
- preservar Excel como fuente de verdad
- usar cambios incrementales
- mantener código modular
- explicar qué archivos tocó
- explicar qué comandos correr
- verificar funcionalmente lo que implementa
- pensar como herramienta de compras, no como demo

### Nunca hacer sin pedirlo
- migrar a otro framework
- meter base de datos nueva
- introducir scraping
- renombrar columnas reales del Excel sin necesidad
- rehacer el proyecto completo
- sobreingenierizar
- agregar acciones que no funcionan de verdad
- prometer features que no verificó
- priorizar maquillaje visual por encima de integridad funcional

### Si algo falla
Priorizar:
- diagnóstico puntual
- corrección incremental
- no romper lo ya funcional
- no mentir sobre el estado real de una feature
- hacer visible la limitación en vez de simular que está resuelta

---

## Comandos típicos
- Dashboard: `streamlit run dashboard.py`
- CLI: `python main.py`

---

## Comandos de ejecución y testing

### Ejecutar la app
```bash
streamlit run dashboard.py
```

### Ejecutar CLI
```bash
python main.py
```

### Puerto específico
```bash
streamlit run dashboard.py --server.port 8502
```

---

## Code Style Guidelines

### Imports
- Usar imports absolutos desde `app`: `from app import dashboard_data, excel_service, config`
- No usar imports relativos como `from . import ...`
- Agrupar: stdlib → third-party → local
- Ordenar alfabéticamente dentro de cada grupo

### Formateo
- Máximo 120 caracteres por línea
- 4 espacios para indentación (no tabs)
- Espacios alrededor de operadores: `x = 1`, no `x=1`
- Sin espacios dentro de paréntesis: `func(x)`, no `func( x )`

### Tipos
- No es obligatorio usar type hints, pero son recomendados para funciones públicas
- Prefijos de tipo solo cuando mejoran legibilidad: `df_` para DataFrames, `lst_` para listas

### Convenciones de nombres
- **Variables y funciones**: `snake_case` (`obtener_productos`, `dolar_actual`)
- **Constantes**: `UPPER_SNAKE_CASE` (`MAX_PRODUCTOS`, `DEFAULT_MARGEN`)
- **Clases**: `PascalCase` (`ExcelService`, `DashboardData`)
- **Archivos**: `snake_case.py` (`excel_service.py`, `dashboard_data.py`)
- **Columnas Excel**: mantener nombres originales exactamente como están en el Excel (`precio_competidor_actual_ars`, NO renombrar a `precio_comp`)

### Manejo de errores
- Siempre retornar `True`/`False` explícito en funciones de escritura (no usar `None` o exceptions silenciosas)
- Usar `try/except` solo cuando se pueda manejar la excepción meaningfully
- Mostrar mensajes de error claros al usuario: `st.error("❌ Error al guardar")`
- No ocultar errores con `pass` vacío

### Funciones de Excel
- Toda función que modifique el Excel debe:
  - Cargar la hoja completa antes de modificar
  - Preservar todas las filas y columnas existentes
  - Devolver `True` si éxito, `False` si falla
  - Ser idempotente (poder ejecutarse múltiples veces sin efectos adversos)

### CSS y UI
- CSS custom va en la variable `CSS` al inicio del archivo
- Usar variables CSS para colores: `var(--accent)`, `var(--border)`
- No hardcodear colores hex en el CSS si ya están en `:root`
- Prefijos de clase propios: `.kpi-card`, `.table-actions`, `.sfl-monogram`

### Streamlit
- Siempre usar `st.set_page_config` al inicio
- Usar `layout="wide"` para dashboards
- No usar `st.cache_data` a menos que haya procesamiento pesado
- Preferir `st.columns` sobre `st.beta_columns`

---

## Criterio general

Este sistema no reemplaza el criterio comercial de la clienta.  
La clienta decide qué productos comparar.  
El sistema automatiza análisis, visualización, cálculo, persistencia y operación.

La vara de calidad para este proyecto es:

**internal tool premium, funcional, honesta y útil para compras/pricing.**
