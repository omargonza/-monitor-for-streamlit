"""
Ayuda contextual para la clienta de pricing / compras.
Capa de interpretación comercial embebida en la app.
"""

# =============================================================================
# GLOSARIO DE CONCEPTOS
# =============================================================================
GLOSARIO_CONCEPTOS = {
    "costo_usd": {
        "titulo": "Costo en USD",
        "resumen": "Es lo que pagás por el producto al proveedor.",
        "explicacion": "Es el precio en dólares que acordaste con tu proveedor. Se usa como base para calcular el costo en pesos y definir el precio de venta.",
        "interpretacion": "Un costo mal cargado distorsiona todas las métricas de rentabilidad. Si ajustás el costo, recalculá el precio.",
    },
    "dolar_referencia": {
        "titulo": "Dólar de referencia",
        "resumen": "Es el tipo de cambio que se usa para convertir costos y definir precio.",
        "explicacion": "Tomás el dólar oficial o el blue según cómo financiás la operación. Se configura en la solapa Configuración.",
        "interpretacion": "Si financiás con dólar blue pero calculás con oficial, estás subestimando costos y sobreestimando márgenes.",
    },
    "costo_ars": {
        "titulo": "Costo en pesos",
        "resumen": "Es el costo del producto en pesos.",
        "explicacion": "Se calcula: costo USD × dólar de referencia. Es el piso de inversión para ese producto.",
        "interpretacion": "Es tu costo real. Todo precio de venta que esté debajo de este valor implica pérdida.",
    },
    "precio_reyes_ars": {
        "titulo": "Precio propio",
        "resumen": "Es el precio al que vendés vos.",
        "explicacion": "Es el precio de lista que manejó tu empresa para ese producto. Se compara contra el competidor y contra el mínimo rentable.",
        "interpretacion": "Si es muy superior al competidor, puede afectar competitividad. Si es muy cercano al costo, puede afectar rentabilidad.",
    },
    "ganancia_ars": {
        "titulo": "Ganancia en pesos",
        "resumen": "Es la ganancia bruta en pesos por unidad.",
        "explicacion": "Se calcula: precio de venta - costo en ARS. Representa la contribución del producto a cubrir gastos y generar resultado.",
        "interpretacion": "Ganancia alta no siempre es bueno si estás muy encima del competidor. Ganancia justa y competitividad sana es el objetivo.",
    },
    "margen_real_pct": {
        "titulo": "Margen actual",
        "resumen": "Es qué porcentaje ganás sobre el costo.",
        "explicacion": "Se calcula: ((precio / costo) - 1) × 100. Mide la rentabilidad porcentual del producto.",
        "interpretacion": "Un margen del 50% significa que ganás la mitad del costo. Si el margen es menor al mínimo que definiste, hay riesgo.",
    },
    "margen_minimo_pct": {
        "titulo": "Margen mínimo deseado",
        "resumen": "Es el piso de rentabilidad que definiste como aceptable.",
        "explicacion": "Es el umbral que marcás como línea roja para la rentabilidad. Si el margen real baja de este valor, el producto entra en alerta.",
        "interpretacion": "No es un objetivo, es un límite. Definilo según tu estructura de costos y gastos reales.",
    },
    "precio_minimo_rentable": {
        "titulo": "Precio mínimo rentable",
        "resumen": "Es el precio más bajo que podés poner sin perder plata.",
        "explicacion": "Se calcula: costo × (1 + margen mínimo). Si el competidor baja de este precio, competí solo si tenés estrategia de volumen clara.",
        "interpretacion": "Si tenés que igualar o bajar de este precio, preguntate si te conviene por volumen o si preferís perder esa venta.",
    },
    "diferencia_vs_competidor": {
        "titulo": "Dif. vs competidor",
        "resumen": "Es cuánto más caro o más barato estás vs la competencia.",
        "explicacion": "Se calcula: ((precio propio / precio competidor) - 1) × 100. Si es positivo, estás más caro. Si es negativo, estás más barato.",
        "interpretacion": "Ser el más barato no siempre conviene. Si mantenés margen y estás cerca del competidor, es mejor que romper precio.",
    },
    "variacion_competidor": {
        "titulo": "Variación del competidor",
        "resumen": "Es cuánto subió o bajó el precio del competidor desde la última carga.",
        "explicacion": "Se calcula comparando el precio actual vs el anterior del competidor. Indica tendencias de mercado.",
        "interpretacion": "Si el competidor subió, puede haber margen para ajustar tu precio arriba. Si bajó, evaluá competitividad.",
    },
    "accion_recomendada": {
        "titulo": "Qué revisar",
        "resumen": "Lectura orientativa sobre qué revisar comercialmente.",
        "explicacion": "Es una sugerencia automática basada en el estado del producto. No reemplaza tu criterio comercial.",
        "interpretacion": "Usalo como guía, pero siempre validá con tu conocimiento del negocio y del mercado.",
    },
}


# =============================================================================
# TOOLTIPS PARA COLUMNAS DE TABLA (versiones cortas)
# =============================================================================
TOOLTIPS_COLUMNAS = {
    "costo_ars": "Costo del producto en pesos. Es la base real para medir rentabilidad.",
    "precio_reyes_ars": "Precio actual de venta propio.",
    "precio_competidor_actual_ars": "Último precio cargado del competidor. Se usa para calcular la diferencia.",
    "margen_real_pct": "Rentabilidad real actual del producto sobre el costo.",
    "margen_minimo_pct": "Piso de rentabilidad aceptable definido para este producto.",
    "diferencia_vs_competidor_pct": "Qué tan arriba o abajo estás frente al competidor.",
    "accion_recomendada": "Lectura orientativa sobre qué revisar comercialmente.",
}


# =============================================================================
# MEJORAS DE LABELS VISIBLES PARA TABLA
# =============================================================================
LABELS_TABLA = {
    "codigo_reyes": "Código",
    "descripcion_reyes": "Descripción",
    "competidor": "Competidor",
    "costo_ars": "Costo en pesos",
    "precio_reyes_ars": "Precio propio",
    "precio_competidor_actual_ars": "Precio competidor",
    "margen_real_pct": "Margen actual",
    "margen_minimo_pct": "Margen mínimo",
    "diferencia_vs_competidor_pct": "Dif. vs competidor",
    "variacion_competidor_pct": "Var. competidor",
    "precio_minimo_rentable_ars": "Mínimo rentable",
    "precio_sugerido_competitivo_ars": "Precio sugerido",
    "estado": "Estado",
    "accion_recomendada": "Qué revisar",
    "motivo_accion": "Por qué",
}


# =============================================================================
# INTERPRETACIÓN DE ESTADOS
# =============================================================================
INTERPRETACION_ESTADOS = {
    "VERDE": {
        "badge": "VERDE",
        "titulo": "Posición sana",
        "significado": "El producto tiene margen sano y está competitivo.",
        "que_implica": "No necesita intervención inmediata. Seguí monitoreando.",
        "cuando_actuar": "Igualdad con el competidor: podés evaluar subir un poco. Si el margen es alto, evaluá si hay espacio para ganar más competitividad sin romper rentabilidad.",
    },
    "AMARILLO": {
        "badge": "AMARILLO",
        "titulo": "Requiere mirada",
        "significado": "El producto es rentable pero ajustado en competitividad.",
        "que_implica": "Hay margen pero estás encima del competidor. Hay que revisar si conviene ajustar precio o aceptar la diferencia.",
        "cuando_actuar": "Revisá el precio mínimo rentable. Si el competidor está muy lejos y tenés margen, evaluá ajustar. Si la diferencia es manejable, mantené.",
    },
    "ROJO": {
        "badge": "ROJO",
        "titulo": "Riesgo inmediato",
        "significado": "El margen está por debajo del mínimo o estás muy encima del competidor.",
        "que_implica": "Hay riesgo de rentabilidad o de competitividad extrema. Requiere decisión comercial.",
        "cuando_actuar": "Si es margen bajo: evaluá subir precio o revisar costos. Si es precio muy arriba: evaluá ajustar.",
    },
    "SIN_DATO": {
        "badge": "SIN DATO",
        "titulo": "Sin precio competidor",
        "significado": "No hay precio del competidor cargado.",
        "que_implica": "No se puede calcular la diferencia ni clasificar el estado. Necesitás cargar el precio del competidor.",
        "cuando_actuar": "Es la primera carga después de dar de alta el producto. Si ya tenés un precio, cargalo para activar el monitoreo.",
    },
}


# =============================================================================
# TIPS COMERCIALES FIJOS CURADOS
# =============================================================================
TIPS_COMERCIALES_FIJOS = [
    "Empezá por los productos en rojo: ahí suele estar el mayor riesgo de rentabilidad.",
    "No tomes decisiones mirando solo el precio del competidor: validá siempre el impacto en margen.",
    "Si para igualar a la competencia tenés que perforar tu margen mínimo, no conviene competir solo por precio.",
    "Competir no siempre es igualar al más barato. Competir es sostener precio con rentabilidad.",
    "La prioridad no es ser el más barato: es sostener competitividad con rentabilidad.",
]


# =============================================================================
# AYUDA PARA DASHBOARD
# =============================================================================
AYUDA_DASHBOARD = {
    "titulo_bloque": "Cómo leer esta pantalla",
    "orden_lectura": "1. KPIs → 2. Alertas → 3. Prioridades → 4. Tabla",
    "resumen_estados": {
        "VERDE": "Rentable y competitivo",
        "AMARILLO": "Rentable pero encima del competidor",
        "ROJO": "Margen bajo o muy encima",
        "SIN_DATO": "Sin precio del competidor",
    },
    "aclARATORIA": "No siempre conviene igualar al más barato. La prioridad es sostener competitividad con rentabilidad.",
}


# =============================================================================
# AYUDA PARA OPERACIONES
# =============================================================================
AYUDA_OPERACIONES = {
    "actualizacion_rapida": {
        "titulo": "Actualización rápida",
        "ayuda": "Usá esta opción para actualizar rápido precios del competidor sin modificar el resto del producto. Es ideal para el seguimiento diario.",
    },
    "alta_producto": {
        "titulo": "Alta de producto",
        "ayuda": "Los datos indispensables son: código, descripción, competidor, costo USD y precio propio. Sin el margen mínimo correcto la lectura de la app pierde valor.",
    },
    "editar_producto": {
        "titulo": "Editar producto",
        "ayuda": "Conviene editar cuando cambia el costo, el precio propio o el margen mínimo. Modificar estos datos cambia la lectura comercial del producto.",
    },
    "activar_desactivar": {
        "titulo": "Activar / Desactivar",
        "ayuda": "Un producto desactivado sale del monitoreo operativo. No conviene desactivar solo porque esté en rojo: primero revisá la causa.",
    },
}


# =============================================================================
# AYUDA PARA CONFIGURACIÓN
# =============================================================================
AYUDA_CONFIGURACION = {
    "dolar_oficial": {
        "titulo": "Dólar oficial",
        "ayuda": "Usalo si tus costos o financiamiento están en dólar oficial.",
    },
    "dolar_blue": {
        "titulo": "Dólar blue",
        "ayuda": "Usalo si tus costos o financiamiento están en dólar paralelo.",
    },
    "dolar_modo": {
        "titulo": "Dólar de referencia",
        "ayuda": "El dólar de referencia se usa para convertir costos a pesos. Si este valor no refleja cómo realmente financiás la operación, la rentabilidad mostrada puede quedar distorsionada.",
    },
}


# =============================================================================
# AYUDA PARA KPIs
# =============================================================================
AYUDA_KPIS = {
    "productos_activos": "Cantidad de productos que se están monitoreando actualmente.",
    "competitivos": "Productos con estado Verde: margen sano y competitivos.",
    "ajustados": "Productos con estado Amarillo: requieren revisión por estar encima del competidor.",
    "alertas_rojas": "Productos con estado Rojo: requieren revisión por riesgo de rentabilidad o precio muy encima del competidor.",
    "sin_dato": "Productos sin precio del competidor cargado. No se pueden evaluar correctamente.",
}


# =============================================================================
# FUNCIONES DE RENDERIZADO
# =============================================================================

def obtener_tip_fijo(index: int = None) -> str:
    """Retorna un tip fijo o aleatorio."""
    import random
    if index is not None and 0 <= index < len(TIPS_COMERCIALES_FIJOS):
        return TIPS_COMERCIALES_FIJOS[index]
    return random.choice(TIPS_COMERCIALES_FIJOS)


def obtener_todos_tips_fijos() -> list:
    """Retorna todos los tips comerciales fijos."""
    return TIPS_COMERCIALES_FIJOS


def obtener_tooltip_columna(col_key: str) -> str:
    """Retorna el tooltip para una columna."""
    return TOOLTIPS_COLUMNAS.get(col_key, "")


def obtener_label_tabla(col_key: str) -> str:
    """Retorna el label visible para una columna."""
    return LABELS_TABLA.get(col_key, col_key)


def obtener_interpretacion_estado(estado: str) -> dict:
    """Retorna la interpretación de un estado."""
    return INTERPRETACION_ESTADOS.get(estado, {})


def obtener_ayuda_dashboard() -> dict:
    """Retorna la ayuda para el dashboard."""
    return AYUDA_DASHBOARD


def obtener_ayuda_operaciones(seccion: str) -> str:
    """Retorna la ayuda para una sección de operaciones."""
    return AYUDA_OPERACIONES.get(seccion, {}).get("ayuda", "")


def obtener_ayuda_configuracion(campo: str) -> str:
    """Retorna la ayuda para un campo de configuración."""
    return AYUDA_CONFIGURACION.get(campo, {}).get("ayuda", "")


def obtener_ayuda_kpi(kpi_key: str) -> str:
    """Retorna la ayuda para un KPI."""
    return AYUDA_KPIS.get(kpi_key, "")
