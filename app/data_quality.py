"""
Capa de calidad de datos para SFL Monitor.
Encargada de normalizar y validar datos antes de su uso en la app.
"""
import pandas as pd
from typing import TypedDict


class DataQualityResult(TypedDict):
    """Resultado del procesamiento de calidad de datos."""
    df: pd.DataFrame
    warnings: list[dict]
    errors: list[dict]
    stats: dict


PATRONES_PLANTILLA = [
    "copiar desde",
    "productos_reyes",
    "redlenic o",
    "impotekno o",
]

CAMPOS_OBLIGATORIOS = [
    "codigo_reyes",
    "competidor",
]

CAMPOS_NUMERICOS = [
    "costo_usd",
    "precio_reyes_ars",
    "margen_minimo_pct",
    "precio_competidor_actual_ars",
    "precio_competidor_anterior_ars",
]


def normalizar_dataframe_monitoreo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza el DataFrame de monitoreo.
    
    Realiza:
    - Trim de strings
    - Normalización de mayúsculas/minúsculas
    - Normalización de valores de activo (SI/NO, TRUE/FALSE, 1/0)
    - Conversión numérica segura
    - Tratamiento de valores vacíos
    - Corrección básica de encoding
    - Unificación de formatos
    """
    df = df.copy()
    
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(["nan", "None", ""], pd.NA)
    
    if "codigo_reyes" in df.columns:
        df["codigo_reyes"] = df["codigo_reyes"].astype(str).str.strip()
    
    if "competidor" in df.columns:
        df["competidor"] = df["competidor"].astype(str).str.strip().str.upper()
    
    if "descripcion_reyes" in df.columns:
        df["descripcion_reyes"] = df["descripcion_reyes"].astype(str).str.strip()
        df["descripcion_reyes"] = df["descripcion_reyes"].str.replace("el�ctrica", "eléctrica", regex=False)
        df["descripcion_reyes"] = df["descripcion_reyes"].str.replace("pava el�ctrica", "pava eléctrica", regex=False)
    
    if "activo" in df.columns:
        df["activo"] = df["activo"].astype(str).str.upper().str.strip()
        df["activo"] = df["activo"].replace({
            "YES": "SI",
            "TRUE": "SI",
            "1": "SI",
            "NO": "NO",
            "FALSE": "NO",
            "0": "NO",
            "SI/NO": "NO",
            "NAN": "NO",
            "NONE": "NO",
            "": "NO",
        })
        df.loc[~df["activo"].isin(["SI", "NO"]), "activo"] = "NO"
    
    for col in CAMPOS_NUMERICOS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    if "margen_minimo_pct" in df.columns:
        df["margen_minimo_pct"] = df["margen_minimo_pct"].fillna(20.0)
    
    return df


def validar_dataframe_monitoreo(df: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    """
    Valida el DataFrame de monitoreo.
    
    Retorna:
    - warnings: Lista de advertencias (datos potencialmente问题áticos pero operativos)
    - errors: Lista de errores (datos que impiden el uso normal)
    """
    warnings = []
    errors = []
    
    for idx, row in df.iterrows():
        codigo = str(row.get("codigo_reyes", ""))
        
        if not codigo or codigo == "nan":
            errors.append({
                "row": idx,
                "type": "CAMPO_VACIO",
                "field": "codigo_reyes",
                "message": f"Fila {idx}: Código vacío",
            })
            continue
        
        for campo in CAMPOS_OBLIGATORIOS:
            valor = row.get(campo)
            if pd.isna(valor) or str(valor).strip() in ["", "nan", "None"]:
                warnings.append({
                    "row": idx,
                    "codigo": codigo,
                    "type": "CAMPO_VACIO",
                    "field": campo,
                    "message": f"{codigo}: Campo '{campo}' vacío",
                })
        
        precio_reyes = row.get("precio_reyes_ars", 0) or 0
        precio_comp = row.get("precio_competidor_actual_ars", 0) or 0
        
        if pd.notna(precio_comp) and precio_comp > 0 and pd.notna(precio_reyes) and precio_reyes > 0:
            if precio_comp < precio_reyes * 0.05:
                warnings.append({
                    "row": idx,
                    "codigo": codigo,
                    "competidor": row.get("competidor", ""),
                    "type": "PRECIO_COMPETIDOR_BAJO",
                    "field": "precio_competidor_actual_ars",
                    "message": f"{codigo}: Precio competidor ({precio_comp:.0f}) muy bajo vs Reyes ({precio_reyes:.0f})",
                    "precio_reyes": precio_reyes,
                    "precio_comp": precio_comp,
                    "diferencia_pct": ((precio_reyes / precio_comp) - 1) * 100 if precio_comp > 0 else 0,
                })
            
            if precio_comp > precio_reyes * 5:
                warnings.append({
                    "row": idx,
                    "codigo": codigo,
                    "competidor": row.get("competidor", ""),
                    "type": "PRECIO_COMPETIDOR_ALTO",
                    "field": "precio_competidor_actual_ars",
                    "message": f"{codigo}: Precio competidor ({precio_comp:.0f}) muy alto vs Reyes ({precio_reyes:.0f})",
                    "precio_reyes": precio_reyes,
                    "precio_comp": precio_comp,
                    "diferencia_pct": ((precio_comp / precio_reyes) - 1) * 100 if precio_reyes > 0 else 0,
                })
        
        costo_usd = row.get("costo_usd", 0) or 0
        if costo_usd <= 0:
            warnings.append({
                "row": idx,
                "codigo": codigo,
                "type": "COSTO_CERO",
                "field": "costo_usd",
                "message": f"{codigo}: Costo USD es cero o negativo",
            })
        
        margen_min = row.get("margen_minimo_pct", 0) or 0
        if margen_min <= 0:
            warnings.append({
                "row": idx,
                "codigo": codigo,
                "type": "MARGEN_CERO",
                "field": "margen_minimo_pct",
                "message": f"{codigo}: Margen mínimo es cero o negativo",
            })
    
    return warnings, errors


def marcar_filas_plantilla(df: pd.DataFrame) -> pd.DataFrame:
    """Marca filas que parecen ser plantilla o instructivas."""
    df = df.copy()
    df["_es_plantilla"] = False
    
    if "codigo_reyes" in df.columns and "competidor" in df.columns:
        codigo_str = df["codigo_reyes"].astype(str).str.lower()
        competidor_str = df["competidor"].astype(str).str.lower()
        
        patron = "|".join(PATRONES_PLANTILLA)
        mask = codigo_str.str.contains(patron, na=False) | competidor_str.str.contains(patron, na=False)
        df.loc[mask, "_es_plantilla"] = True
    
    return df


def procesar_calidad_datos(df: pd.DataFrame, incluir_plantillas: bool = False) -> DataQualityResult:
    """
    Procesa un DataFrame con la capa de calidad completa.
    
    Args:
        df: DataFrame raw del Excel
        incluir_plantillas: Si True, incluye plantillas en el resultado (marcadas)
    
    Returns:
        DataQualityResult con df normalizado, warnings, errors y stats
    """
    df_original_len = len(df)
    
    df = marcar_filas_plantilla(df)
    
    plantillas_count = df["_es_plantilla"].sum()
    
    df = normalizar_dataframe_monitoreo(df)
    
    warnings, errors = validar_dataframe_monitoreo(df)
    
    if not incluir_plantillas:
        df = df[~df["_es_plantilla"]].copy()
    
    df = df.drop(columns=["_es_plantilla"], errors="ignore")
    
    df = df[df["codigo_reyes"].astype(str).str.strip() != ""]
    df = df[df["codigo_reyes"].astype(str).str.lower() != "nan"]
    
    stats = {
        "filas_originales": df_original_len,
        "filas_plantilla": plantillas_count,
        "filas_procesadas": len(df),
        "warnings_count": len(warnings),
        "errors_count": len(errors),
    }
    
    return DataQualityResult(
        df=df,
        warnings=warnings,
        errors=errors,
        stats=stats,
    )


def cargar_productos_con_calidad( solo_activos: bool = True, incluir_plantillas: bool = False) -> DataQualityResult:
    """
    Carga productos desde Excel con procesamiento de calidad.
    
    Args:
        solo_activos: Si True, filtra solo activos
        incluir_plantillas: Si True, incluye plantillas en el resultado
    
    Returns:
        DataQualityResult con datos normalizados y validados
    """
    from app import config
    
    df = pd.read_excel(config.ARCHIVO_EXCEL, sheet_name=config.HOJAS["MONITOREO"])
    
    result = procesar_calidad_datos(df, incluir_plantillas=incluir_plantillas)
    
    if solo_activos and "activo" in result["df"].columns:
        result["df"] = result["df"][result["df"]["activo"] == "SI"]
        result["stats"]["filas_activas"] = len(result["df"])
    
    return result