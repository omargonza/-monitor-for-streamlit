"""
Datos preparados para el dashboard.
"""
import pandas as pd
from app import excel_service, calculations, config, data_quality


def obtener_config() -> dict:
    """Obtiene configuración."""
    return excel_service.cargar_config()


def obtener_dolar() -> float:
    """Obtiene dólar actual."""
    cfg = obtener_config()
    return calculations.obtener_dolar(cfg)


def obtener_productos() -> pd.DataFrame:
    """
    Obtiene productos procesados con todas las métricas.
    
    Mantiene compatibilidad: retorna solo DataFrame.
    Para quality metadata usar obtener_productos_con_calidad().
    """
    result = data_quality.cargar_productos_con_calidad(solo_activos=True)
    cfg = obtener_config()
    df = calculations.procesar_productos(result["df"], cfg)
    return df


def obtener_productos_con_calidad() -> tuple[pd.DataFrame, dict]:
    """
    Obtiene productos con metadata de calidad de datos.
    
    Returns:
        tuple: (df_procesado, quality_result con warnings, errors, stats)
    """
    result = data_quality.cargar_productos_con_calidad(solo_activos=True)
    cfg = obtener_config()
    df = calculations.procesar_productos(result["df"], cfg)
    return df, result


def obtener_todos_los_productos_con_calidad() -> tuple[pd.DataFrame, dict]:
    """
    Obtiene todos los productos (activos e inactivos) con metadata de calidad.
    
    Returns:
        tuple: (df_procesado, quality_result)
    """
    result = data_quality.cargar_productos_con_calidad(solo_activos=False)
    cfg = obtener_config()
    df = calculations.procesar_productos(result["df"], cfg)
    return df, result


def obtener_resumen() -> dict:
    """Obtiene resumen general del dashboard."""
    df = obtener_productos()
    cfg = obtener_config()
    dolar = calculations.obtener_dolar(cfg)
    dolar_modo = cfg.get("dolar_modo", "oficial").upper()
    
    total = len(df)
    rojos = len(df[df["estado"] == "ROJO"])
    amarillos = len(df[df["estado"] == "AMARILLO"])
    verdes = len(df[df["estado"] == "VERDE"])
    sin_dato = len(df[df["estado"] == "SIN_DATO"])
    
    return {
        "total_productos": total,
        "alertas_rojas": rojos,
        "alertas_amarillas": amarillos,
        "productos_verdes": verdes,
        "sin_dato": sin_dato,
        "dolar_actual": dolar,
        "dolar_modo": dolar_modo,
    }


def obtener_prioridades() -> pd.DataFrame:
    """Obtiene productos prioritarios para revisar."""
    df = obtener_productos()
    
    if df.empty:
        return df
    
    df = df.sort_values(by=["margen_real_pct", "diferencia_vs_competidor_pct"], ascending=[True, True])
    
    return df.head(10)


def obtener_productos_por_estado(estado: str) -> pd.DataFrame:
    """Obtiene productos por estado."""
    df = obtener_productos()
    return df[df["estado"] == estado]


def obtener_historial(limite: int = 10) -> pd.DataFrame:
    """Obtiene los últimos cambios registrados."""
    return excel_service.cargar_historial(limite)


def obtener_estadisticas_calidad() -> dict:
    """Obtiene estadísticas de calidad de datos para el tablero."""
    _, quality = obtener_productos_con_calidad()
    
    stats = {
        "warnings_activos": len(quality.get("warnings", [])),
        "filas_plantilla": quality.get("stats", {}).get("filas_plantilla", 0),
        "productos_sospechosos": 0,
        "problemas_costo": 0,
        "problemas_margen": 0,
    }
    
    if quality.get("warnings"):
        for w in quality["warnings"]:
            tipo = w.get("type", "")
            if "PRECIO" in tipo:
                stats["productos_sospechosos"] += 1
            elif "COSTO" in tipo:
                stats["problemas_costo"] += 1
            elif "MARGEN" in tipo:
                stats["problemas_margen"] += 1
    
    return stats