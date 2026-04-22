"""
Configuración centralizada del proyecto.
"""
import os

# Cargar .env en local (solo si existe el archivo)
from pathlib import Path
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(_env_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO_EXCEL = os.path.join(BASE_DIR, "reyes_monitoreo_base_v1.xlsx")


def obtener_credenciales() -> tuple[str, str]:
    """
    Obtiene credenciales de autenticación.
    
    Prioridad:
    1. st.secrets (producción)
    2. variables de entorno .env (local)
    
    Returns:
        tuple: (usuario, password)
    
    Raises:
        ValueError: Si no se encuentran credenciales configuradas
    """
    import streamlit as st
    
    usuario = None
    password = None
    
    # 1. Intentar desde st.secrets
    try:
        if hasattr(st, 'secrets'):
            usuario = st.secrets.get("AUTH_USUARIO")
            password = st.secrets.get("AUTH_PASSWORD")
    except Exception:
        pass
    
    # 2. Si no están en secrets, intentar desde .env
    if not usuario or not password:
        usuario = os.environ.get("AUTH_USUARIO")
        password = os.environ.get("AUTH_PASSWORD")
    
    # 3. Si no están en ninguno, error
    if not usuario or not password:
        raise ValueError("Falta configuración de acceso. Configurá AUTH_USUARIO y AUTH_PASSWORD en .env (local) o st.secrets (producción).")
    
    return usuario, password


# Rutas assets
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BRANDING_DIR = os.path.join(ASSETS_DIR, "branding")
LOGO_CONURBADEV = os.path.join(BRANDING_DIR, "logo-conurbadev-footer.png")

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