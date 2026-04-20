"""
Configuración centralizada del proyecto.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO_EXCEL = os.path.join(BASE_DIR, "reyes_monitoreo_base_v1.xlsx")

HOJAS = {
    "PRODUCTOS": "PRODUCTOS_REYES",
    "MONITOREO": "MONITOREO_ACTIVO",
    "CONFIG": "CONFIG",
    "HISTORIAL": "HISTORIAL",
}

COLUMNAS_REQUERIDAS = [
    "codigo_reyes",
    "descripcion_reyes",
    "competidor",
    "precio_reyes_ars",
    "precio_competidor_actual_ars",
    "precio_competidor_anterior_ars",
    "costo_usd",
    "margen_minimo_pct",
    "activo",
]

COLUMNAS_CONFIG = [
    "dolar_oficial",
    "dolar_blue",
    "dolar_modo",
]

ESTADO_COLORES = {
    "VERDE": "#22c55e",
    "AMARILLO": "#eab308",
    "ROJO": "#ef4444",
    "SIN_DATO": "#6b7280",
}

ESTADO_DESCRIPCIONES = {
    "VERDE": "Rentable y competitivo",
    "AMARILLO": "Rentable pero ajustado",
    "ROJO": "Margen bajo o muy fuera de mercado",
    "SIN_DATO": "Sin dato del competidor",
}