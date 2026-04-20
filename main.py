import pandas as pd
import sys

ARCHIVO_EXCEL = "reyes_monitoreo_base_v1.xlsx"
HOJA_MONITOREO = "MONITOREO_ACTIVO"
HOJA_CONFIG = "CONFIG"

COLUMNAS_REQUERIDAS = [
    "codigo_reyes",
    "descripcion_reyes",
    "costo_usd",
    "precio_reyes_ars",
    "margen_minimo_pct",
    "activo"
]

COLUMNAS_OPCIONALES = [
    "competidor",
    "url_categoria_competidor",
    "referencia_manual_competidor"
]


def obtener_dolar_referencia(df_config):
    try:
        dolar_modo = df_config.loc[df_config["clave"] == "dolar_modo", "valor"].iloc[0]
    except (KeyError, IndexError):
        print("Error: No se encontró 'dolar_modo' en CONFIG")
        sys.exit(1)

    try:
        dolar_oficial = float(df_config.loc[df_config["clave"] == "dolar_oficial", "valor"].iloc[0])
    except (KeyError, IndexError, ValueError):
        print("Error: No se encontró 'dolar_oficial' válido en CONFIG")
        sys.exit(1)

    try:
        dolar_blue = float(df_config.loc[df_config["clave"] == "dolar_blue", "valor"].iloc[0])
    except (KeyError, IndexError, ValueError):
        print("Error: No se encontró 'dolar_blue' válido en CONFIG")
        sys.exit(1)

    dolar_modo = dolar_modo.lower()
    if dolar_modo == "blue":
        return dolar_blue
    elif dolar_modo == "oficial":
        return dolar_oficial
    else:
        print(f"Error: dolar_modo '{dolar_modo}' no válido (usar 'oficial' o 'blue')")
        sys.exit(1)


def validar_columnas(df, columnas_req, columnas_opc):
    faltantes = [col for col in columnas_req if col not in df.columns]
    if faltantes:
        print(f"Error: Faltan columnas requeridas: {faltantes}")
        sys.exit(1)

    opcionales_faltantes = [col for col in columnas_opc if col not in df.columns]
    if opcionales_faltantes:
        print(f"Advertencia: Columnas opcionales no encontradas: {opcionales_faltantes}")


def calcular_metricas(row, dolar_ref):
    try:
        costo_usd = float(row["costo_usd"])
    except (ValueError, TypeError):
        costo_usd = 0.0

    try:
        precio_reyes_ars = float(row["precio_reyes_ars"])
    except (ValueError, TypeError):
        precio_reyes_ars = 0.0

    try:
        margen_minimo_pct = float(row["margen_minimo_pct"])
    except (ValueError, TypeError):
        margen_minimo_pct = 0.0

    costo_ars = costo_usd * dolar_ref
    ganancia_ars = precio_reyes_ars - costo_ars
    ganancia_usd = ganancia_ars / dolar_ref
    margen_real_pct = ((precio_reyes_ars / costo_ars) - 1) * 100
    precio_minimo_rentable_ars = costo_ars * (1 + margen_minimo_pct / 100)

    return {
        "costo_ars": costo_ars,
        "ganancia_ars": ganancia_ars,
        "ganancia_usd": ganancia_usd,
        "margen_real_pct": margen_real_pct,
        "precio_minimo_rentable_ars": precio_minimo_rentable_ars
    }


def formatear_moneda(valor):
    return f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatear_pct(valor):
    return f"{valor:.2f}%".replace(".", ",")


def main():
    try:
        df_config = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA_CONFIG)
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA_MONITOREO)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ARCHIVO_EXCEL}'")
        sys.exit(1)
    except ValueError as e:
        if "sheet" in str(e).lower():
            print(f"Error: Una de las hojas '{HOJA_MONITOREO}' o '{HOJA_CONFIG}' no existe")
            sys.exit(1)
        raise

    validar_columnas(df, COLUMNAS_REQUERIDAS, COLUMNAS_OPCIONALES)

    df = df[df["activo"].str.upper().isin(["SI", "NO"])]
    for col in ["costo_usd", "precio_reyes_ars", "margen_minimo_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    dolar_ref = obtener_dolar_referencia(df_config)
    print(f"\nDólar de referencia: {formatear_moneda(dolar_ref)} (modo: {df_config.loc[df_config['clave'] == 'dolar_modo', 'valor'].iloc[0]})\n")

    df_activos = df[df["activo"].str.upper() == "SI"].copy()
    print(f"Productos activos: {len(df_activos)}\n")
    print("=" * 100)

    for idx, row in df_activos.iterrows():
        metricas = calcular_metricas(row, dolar_ref)

        print(f"Código:         {row['codigo_reyes']}")
        print(f"Descripción:    {row['descripcion_reyes']}")
        print(f"Costo USD:      {formatear_moneda(row['costo_usd'])}")
        print(f"Costo ARS:      {formatear_moneda(metricas['costo_ars'])}")
        print(f"Precio Reyes:   {formatear_moneda(row['precio_reyes_ars'])}")
        print(f"Ganancia ARS:   {formatear_moneda(metricas['ganancia_ars'])}")
        print(f"Ganancia USD:   {formatear_moneda(metricas['ganancia_usd'])}")
        print(f"Margen real:    {formatear_pct(metricas['margen_real_pct'])}")
        print(f"Mín. rentable:  {formatear_moneda(metricas['precio_minimo_rentable_ars'])} (margen mín: {formatear_pct(row['margen_minimo_pct'])})")

        if "competidor" in row.index and pd.notna(row.get("competidor")):
            print(f"Competidor:     {row['competidor']}")
        if "referencia_manual_competidor" in row.index and pd.notna(row.get("referencia_manual_competidor")):
            print(f"Ref. competidor: {row['referencia_manual_competidor']}")

        print("=" * 100)


if __name__ == "__main__":
    main()