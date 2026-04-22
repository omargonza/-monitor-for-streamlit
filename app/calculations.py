"""
Lógica de cálculos comerciales.
"""
import pandas as pd


def obtener_dolar(config_dict: dict) -> float:
    """Obtiene el dólar de referencia según configuracion en Excel."""
    try:
        dolar_modo = str(config_dict.get("dolar_modo", "oficial")).lower()
    except Exception:
        dolar_modo = "oficial"
    
    try:
        dolar_oficial = float(config_dict.get("dolar_oficial", 0))
    except Exception:
        dolar_oficial = 0
    
    try:
        dolar_blue = float(config_dict.get("dolar_blue", 0))
    except Exception:
        dolar_blue = 0
    
    if dolar_modo == "blue" and dolar_blue > 0:
        return dolar_blue
    return dolar_oficial


def calcular_costo_ars(costo_usd: float, dolar_ref: float) -> float:
    """Costo en ARS = costo USD × dólar."""
    return costo_usd * dolar_ref


def calcular_ganancia_ars(precio_ars: float, costo_ars: float) -> float:
    """Ganancia en ARS = precio - costo."""
    return precio_ars - costo_ars


def calcular_ganancia_usd(ganancia_ars: float, dolar_ref: float) -> float:
    """Ganancia en USD = ganancia ARS / dólar."""
    if dolar_ref <= 0:
        return 0
    return ganancia_ars / dolar_ref


def calcular_margen_real_pct(precio_ars: float, costo_ars: float) -> float:
    """Margen real % = ((precio / costo) - 1) × 100."""
    if costo_ars <= 0:
        return 0
    return ((precio_ars / costo_ars) - 1) * 100


def calcular_diferencia_vs_competidor(precio_reyes: float, precio_comp: float) -> float:
    """Diferencia % = ((precio_reyes / precio_comp) - 1) × 100."""
    if precio_comp <= 0:
        return 0
    return ((precio_reyes / precio_comp) - 1) * 100


def calcular_variacion_competidor(precio_actual: float, precio_anterior: float) -> float:
    """Variación % del competidor = ((precio_actual / precio_anterior) - 1) × 100."""
    if precio_anterior <= 0:
        return 0
    return ((precio_actual / precio_anterior) - 1) * 100


def calcular_precio_minimo_rentable(costo_ars: float, margen_minimo_pct: float) -> float:
    """Precio mínimo rentable = costo × (1 + margen_minimo/100)."""
    return costo_ars * (1 + margen_minimo_pct / 100)


def calcular_precio_sugerido_competitivo(precio_comp: float, costo_ars: float, margen_minimo_pct: float) -> float:
    """
    Calcula el precio sugerido competitivo.
    
    Regla:
    - Si precio_comp <= 0: devuelve precio_minimo_rentable
    - Si precio_comp < precio_minimo: el sugerido es precio_minimo (no se perfora el mínimo)
    - Si precio_comp >= precio_minimo: el sugerido es precio_comp - 1% (competir levemente debajo)
    """
    precio_minimo = calcular_precio_minimo_rentable(costo_ars, margen_minimo_pct)
    
    if precio_comp <= 0:
        return precio_minimo
    
    if precio_comp < precio_minimo:
        return precio_minimo
    
    return precio_comp * 0.99


def clasificar_estado(margen_real_pct: float, diferencia_vs_comp: float, margen_minimo_pct: float, precio_comp: float = None) -> str:
    """
    Clasifica el estado del producto según reglas:
    
    - SIN_DATO: no hay precio del competidor (vacío, 0 o null)
    - ROJO: margen_real < margen_minimo (no es rentable) O diferencia > 15% (muy encima de la competencia)
    - AMARILLO: margen_real >= margen_minimo Y 5% < diferencia <= 15% (ajustado)
    - VERDE: margen_real >= margen_minimo Y diferencia <= 5% (competitivo y rentable)
    """
    if precio_comp is None or precio_comp == 0 or (isinstance(precio_comp, float) and precio_comp != precio_comp):
        return "SIN_DATO"
    
    if margen_real_pct < margen_minimo_pct:
        return "ROJO"
    
    if diferencia_vs_comp > 15:
        return "ROJO"
    
    if diferencia_vs_comp <= 5:
        return "VERDE"
    
    return "AMARILLO"


def calcular_metrica(producto: pd.Series, dolar_ref: float) -> dict:
    """Calcula todas las métricas para un producto."""
    costo_usd = producto.get("costo_usd", 0) or 0
    precio_reyes = producto.get("precio_reyes_ars", 0) or 0
    precio_comp = producto.get("precio_competidor_actual_ars", 0) or 0
    precio_comp_anterior = producto.get("precio_competidor_anterior_ars", 0) or 0
    margen_minimo = producto.get("margen_minimo_pct", 0) or 0
    
    costo_ars = calcular_costo_ars(costo_usd, dolar_ref)
    ganancia_ars = calcular_ganancia_ars(precio_reyes, costo_ars)
    ganancia_usd = calcular_ganancia_usd(ganancia_ars, dolar_ref)
    margen_real = calcular_margen_real_pct(precio_reyes, costo_ars)
    diferencia_comp = calcular_diferencia_vs_competidor(precio_reyes, precio_comp)
    variacion_comp = calcular_variacion_competidor(precio_comp, precio_comp_anterior)
    precio_minimo = calcular_precio_minimo_rentable(costo_ars, margen_minimo)
    precio_sugerido = calcular_precio_sugerido_competitivo(precio_comp, costo_ars, margen_minimo)
    estado = clasificar_estado(margen_real, diferencia_comp, margen_minimo, precio_comp)
    
    accion, motivo = generar_accion_recomendada(estado, precio_comp, margen_real, margen_minimo, diferencia_comp, precio_reyes)
    
    return {
        "costo_ars": costo_ars,
        "ganancia_ars": ganancia_ars,
        "ganancia_usd": ganancia_usd,
        "margen_real_pct": margen_real,
        "diferencia_vs_competidor_pct": diferencia_comp,
        "variacion_competidor_pct": variacion_comp,
        "precio_minimo_rentable_ars": precio_minimo,
        "precio_sugerido_competitivo_ars": precio_sugerido,
        "estado": estado,
        "accion_recomendada": accion,
        "motivo_accion": motivo,
    }


def generar_accion_recomendada(estado: str, precio_comp: float, margen_real: float, margen_minimo: float, diferencia_comp: float, precio_reyes: float = 0) -> tuple:
    """
    Genera acción recomendada y motivo según reglas de negocio.
    
    Lógica:
    - SIN_DATO: cargar dato competidor
    - ROJO + margen bajo: bajar precio o revisar costos
    - ROJO + muy encima competencia: revisar precio
    - AMARILLO + margen sano: mantener
    - AMARILLO + margen ajustado: revisar
    - VERDE: mantener o subir si hay margen
    - Datos anómalos: verificar dato competidor
    """
    if estado == "SIN_DATO":
        return ("Cargar dato competidor", "Sin precio del competidor cargado")
    
    # Detectar datos anómalos del competidor
    if precio_comp and precio_comp > 0 and precio_reyes and precio_reyes > 0:
        if precio_comp < precio_reyes * 0.05:
            return ("Verificar dato competidor", f"Precio competidor ({precio_comp:.0f}) muy bajo vs Reyes ({precio_reyes:.0f})")
        if precio_comp > precio_reyes * 5:
            return ("Verificar dato competidor", f"Precio competidor ({precio_comp:.0f}) muy alto vs Reyes ({precio_reyes:.0f})")
    
    if estado == "ROJO":
        if margen_real < margen_minimo:
            return ("Bajar precio", f"Margen {margen_real:.1f}% debajo del mínimo {margen_minimo:.1f}%")
        else:
            return ("Revisar precio", f"Precio {diferencia_comp:.1f}% encima del competidor")
    
    if estado == "AMARILLO":
        if margen_real >= margen_minimo * 1.2:
            return ("Mantener", "Margen sano dentro de rango competitivo")
        else:
            return ("Revisar", "Margen ajustado, evaluar ajuste de precio")
    
    if estado == "VERDE":
        if diferencia_comp < 0:
            return ("Subir precio", "Por debajo del competidor con margen sano")
        else:
            return ("Mantener", "Precio competitivo y rentable")
    
    return ("Revisar", "Revisión manual requerida")


def procesar_productos(df: pd.DataFrame, config_dict: dict) -> pd.DataFrame:
    """Procesa todos los productos y agrega las métricas."""
    if df.empty:
        return pd.DataFrame(columns=[
            "codigo_reyes", "descripcion_reyes", "competidor", "costo_usd",
            "precio_reyes_ars", "precio_competidor_actual_ars", "margen_minimo_pct",
            "costo_ars", "ganancia_ars", "ganancia_usd", "margen_real_pct",
            "diferencia_vs_competidor_pct", "variacion_competidor_pct",
            "precio_minimo_rentable_ars", "precio_sugerido_competitivo_ars",
            "estado", "accion_recomendada", "motivo_accion", "riesgo_comercial",
            "oportunidad_comercial", "necesita_dato_competidor", "margen_sano",
            "fuera_de_rango", "activo"
        ])
    
    dolar_ref = obtener_dolar(config_dict)
    
    resultados = []
    for _, row in df.iterrows():
        producto = row.to_dict()
        metricas = calcular_metrica(row, dolar_ref)
        producto.update(metricas)
        resultados.append(producto)
    
    return pd.DataFrame(resultados)