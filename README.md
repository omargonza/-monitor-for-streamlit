# Monitoréo de Precios Reyes

Sistema asistido de comparación competitiva y rentabilidad.

## Estados

| Estado | Condición |
|--------|-----------|
| 🟢 VERDE | Rentable y competitivo (margen >= min y dif <= 5%) |
| 🟡 AMARILLO | Rentable pero ajustado (margen >= min y 5% < dif <= 15%) |
| 🔴 ROJO | Margen bajo o muy fuera de mercado |
| ⚪ SIN_DATO | Sin precio del competidor |

## Uso

```bash
# Dashboard
streamlit run dashboard.py

# CLI
python main.py
```

## Configuración

Editar en hoja `CONFIG` del Excel:
- dolar_oficial
- dolar_blue  
- dolar_modo (oficial/blue)