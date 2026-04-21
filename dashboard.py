
"""
CSL Monitor - Dashboard UI refined
"""
import streamlit as st
import pandas as pd
from app import dashboard_data, excel_service, calculations

st.set_page_config(page_title="CSL Monitor", page_icon="◈", layout="wide")

CSS = """
<style>
:root{
  --bg:#f3f4f6;
  --bg-soft:#eef1f4;
  --surface:#ffffff;
  --surface-2:#f7f8fa;
  --ink:#111111;
  --muted:#5e6673;
  --muted-2:#7b8794;
  --line:#d6dae1;
  --line-2:#e6e9ee;
  --steel:#3e4a59;
  --steel-2:#546274;
  --charcoal:#1f2933;
  --champagne:#bfa67a;
  --green:#2e6f60;
  --amber:#a8843a;
  --red:#8a4b4b;
  --gray:#7b8794;
  --shadow:0 18px 48px rgba(31,41,51,.08);
  --shadow-soft:0 10px 26px rgba(31,41,51,.06);
  --radius-xl:24px;
  --radius-lg:18px;
  --radius-md:14px;
}

html, body, [class*="css"]{
  font-family: Inter, "Segoe UI", Arial, sans-serif;
}

.stApp{
  background:
    radial-gradient(circle at 92% 8%, rgba(191,166,122,.08) 0%, transparent 18%),
    linear-gradient(180deg, var(--bg) 0%, var(--bg-soft) 100%);
  color: var(--ink);
}

.block-container{
  max-width: 1500px;
  padding-top: 1.25rem;
  padding-bottom: 2rem;
}

section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, #eef1f4 0%, #e6eaef 100%);
  border-right: 1px solid var(--line);
}

section[data-testid="stSidebar"] .block-container{
  padding-top: 1.2rem;
}

#MainMenu, header, footer {visibility:hidden;}

.shell-card{
  background: rgba(255,255,255,.82);
  border: 1px solid rgba(214,218,225,.9);
  box-shadow: var(--shadow-soft);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(4px);
}

.hero{
  padding: 1.5rem;
  background:
    linear-gradient(135deg, rgba(31,41,51,.96) 0%, rgba(62,74,89,.96) 45%, rgba(84,98,116,.95) 100%);
  border: 1px solid rgba(191,166,122,.18);
  border-radius: 28px;
  box-shadow: 0 22px 56px rgba(31,41,51,.18);
  position: relative;
  overflow: hidden;
  min-height: 228px;
}
.hero:before{
  content:"";
  position:absolute;
  inset:0;
  background:
    linear-gradient(180deg, rgba(255,255,255,.08), transparent 18%),
    radial-gradient(circle at 85% 10%, rgba(191,166,122,.14), transparent 24%);
  pointer-events:none;
}
.hero-grid{
  position:relative;
  z-index:1;
  display:grid;
  grid-template-columns: 1.4fr .9fr;
  gap: 1.25rem;
  align-items: stretch;
}
.hero-left{
  display:flex;
  flex-direction:column;
  justify-content:center;
  min-height: 170px;
}
.hero-kicker{
  color: var(--champagne);
  font-size: .74rem;
  text-transform: uppercase;
  letter-spacing: .18em;
  font-weight: 700;
  margin-bottom: .9rem;
}
.hero-brand{
  display:flex;
  gap: 1rem;
  align-items:center;
}
.hero-mark{
  width: 84px;
  height: 84px;
  border-radius: 24px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:
    linear-gradient(160deg, rgba(255,255,255,.12), rgba(255,255,255,.04));
  border: 1px solid rgba(255,255,255,.14);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.12);
  color: #fff;
  font-size: 1.7rem;
  font-weight: 800;
  letter-spacing: .08em;
}
.hero-title{
  margin:0;
  color:#fff;
  font-size: 3rem;
  line-height: 1;
  letter-spacing:-.04em;
}
.hero-subtitle{
  margin:.8rem 0 0;
  color: rgba(255,255,255,.84);
  font-size: 1.25rem;
  line-height: 1.45;
  max-width: 720px;
}
.hero-right{
  display:grid;
  grid-template-columns: repeat(2, minmax(0,1fr));
  gap: .9rem;
  align-content: start;
}
.hero-chip{
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 20px;
  padding: 1rem 1rem 1.05rem;
  min-height: 84px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06);
}
.hero-chip-label{
  color: rgba(255,255,255,.66);
  font-size: .7rem;
  text-transform: uppercase;
  letter-spacing: .13em;
  font-weight: 700;
}
.hero-chip-value{
  margin-top: .55rem;
  color:#fff;
  font-size: 1.45rem;
  font-weight: 700;
  letter-spacing:-.03em;
}
.hero-chip-note{
  margin-top: .25rem;
  color: rgba(255,255,255,.72);
  font-size: .82rem;
}

.sidebar-brand{
  padding: .9rem;
  border-radius: 22px;
  background:
    linear-gradient(135deg, rgba(31,41,51,.96) 0%, rgba(62,74,89,.94) 100%);
  border: 1px solid rgba(191,166,122,.16);
  box-shadow: 0 16px 34px rgba(31,41,51,.16);
  display:flex;
  gap:.85rem;
  align-items:center;
  margin-bottom: 1rem;
}
.sidebar-mark{
  width: 54px;
  height: 54px;
  border-radius: 16px;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#fff;
  font-weight:800;
  font-size:1.05rem;
  letter-spacing:.06em;
  background: linear-gradient(160deg, rgba(255,255,255,.18), rgba(255,255,255,.06));
  border: 1px solid rgba(255,255,255,.14);
}
.sidebar-title{
  color:#fff;
  font-weight:700;
  font-size:1.1rem;
  line-height:1.1;
}
.sidebar-subtitle{
  color: rgba(255,255,255,.7);
  font-size:.84rem;
  margin-top:.18rem;
}

.sidebar-note{
  padding: 1rem 1rem 1.05rem;
  border-radius: 18px;
  border:1px solid var(--line);
  background: rgba(255,255,255,.65);
  color: var(--muted);
  line-height:1.5;
  margin-bottom: 1rem;
}

.sidebar-label{
  color: var(--muted);
  font-size: .74rem;
  text-transform: uppercase;
  letter-spacing: .15em;
  font-weight: 700;
  margin-bottom: .7rem;
}

section[data-testid="stSidebar"] [data-testid="stRadio"]{
  gap: .6rem;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label{
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255,255,255,.72);
  padding: .92rem 1rem;
  transition: .2s ease;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{
  border-color: rgba(62,74,89,.55);
  transform: translateY(-1px);
  box-shadow: 0 8px 16px rgba(31,41,51,.06);
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){
  background: linear-gradient(135deg, var(--steel), var(--steel-2));
  border-color: rgba(191,166,122,.25);
  box-shadow: 0 12px 24px rgba(31,41,51,.14);
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p{
  color:#fff !important;
  font-weight:700;
}

.kpi{
  padding: 1.1rem 1.1rem 1.15rem;
  border-radius: 22px;
  background: linear-gradient(180deg, rgba(255,255,255,.96), rgba(250,251,253,.92));
  border: 1px solid var(--line);
  box-shadow: var(--shadow-soft);
  position:relative;
  overflow:hidden;
}
.kpi:before{
  content:"";
  position:absolute;
  inset:0 auto auto 0;
  width:100%;
  height:3px;
  background: linear-gradient(90deg, var(--champagne), transparent 82%);
}
.kpi-label{
  color: var(--muted);
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .14em;
  font-weight: 700;
}
.kpi-value{
  margin-top: .65rem;
  color: var(--charcoal);
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -.04em;
}
.kpi-note{
  margin-top: .45rem;
  color: var(--muted-2);
  font-size: .9rem;
}

.section-card{
  background: rgba(255,255,255,.84);
  border: 1px solid var(--line);
  box-shadow: var(--shadow-soft);
  border-radius: 24px;
  padding: 1.25rem;
}
.section-eyebrow{
  color: var(--champagne);
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .16em;
  font-weight: 700;
}
.section-title{
  color: var(--charcoal);
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -.03em;
  margin-top: .35rem;
}
.section-copy{
  color: var(--muted);
  font-size: 1rem;
  margin-top: .4rem;
}
.section-meta{
  color: var(--muted-2);
  font-size: .94rem;
  text-align:right;
}

.filter-grid{
  display:grid;
  grid-template-columns: repeat(4, minmax(0,1fr));
  gap: 1rem;
}

.section-rule{
  height: 1px;
  background: linear-gradient(90deg, rgba(191,166,122,.38), rgba(214,218,225,.85) 25%, rgba(214,218,225,.5) 100%);
  margin: .9rem 0 1.15rem;
}

.data-shell{
  background: rgba(255,255,255,.92);
  border: 1px solid var(--line);
  border-radius: 24px;
  box-shadow: var(--shadow-soft);
  overflow: hidden;
}
.data-shell-top{
  display:flex;
  align-items:end;
  justify-content:space-between;
  gap: 1rem;
  padding: 1.15rem 1.2rem .9rem;
  border-bottom: 1px solid var(--line-2);
}
.data-shell-title{
  color: var(--charcoal);
  font-size: 1.15rem;
  font-weight: 700;
}
.data-shell-copy{
  color: var(--muted);
  font-size: .92rem;
  margin-top: .2rem;
}
.data-shell-actions{
  display:flex;
  gap: .8rem;
  align-items:center;
  color: var(--muted);
  font-size: .92rem;
}
.data-shell-inner{
  padding: 0 1rem 1rem;
}

.alert-card{
  background: rgba(255,255,255,.92);
  border: 1px solid var(--line);
  border-radius: 22px;
  box-shadow: var(--shadow-soft);
  padding: 1rem;
  min-height: 100%;
}
.alert-item{
  border-radius: 14px;
  padding: .85rem .95rem;
  margin-top: .75rem;
  border: 1px solid transparent;
}
.alert-item.red{ background: rgba(138,75,75,.08); border-color: rgba(138,75,75,.18); }
.alert-item.amber{ background: rgba(168,132,58,.09); border-color: rgba(168,132,58,.2); }
.alert-item.gray{ background: rgba(123,135,148,.09); border-color: rgba(123,135,148,.18); }

.priority-item{
  padding: .95rem 1rem;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.78);
  margin-top: .75rem;
}
.priority-top{
  display:flex;
  justify-content:space-between;
  gap:1rem;
}
.priority-cause{
  color: var(--muted);
  font-size: .88rem;
  margin-top: .28rem;
}

.stSelectbox label,
.stTextInput label,
.stNumberInput label{
  color: var(--muted) !important;
  font-size: .72rem !important;
  text-transform: uppercase;
  letter-spacing: .14em;
  font-weight: 700 !important;
  margin-bottom: .35rem !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input{
  min-height: 52px !important;
  border-radius: 16px !important;
  border: 1px solid var(--line) !important;
  background: rgba(255,255,255,.92) !important;
  color: var(--charcoal) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.92);
}
.stSelectbox [data-baseweb="select"] > div:hover,
.stTextInput input:hover,
.stNumberInput input:hover{
  border-color: rgba(62,74,89,.55) !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within,
.stTextInput input:focus,
.stNumberInput input:focus{
  border-color: var(--steel) !important;
  box-shadow: 0 0 0 3px rgba(62,74,89,.10) !important;
}
.stSelectbox svg{
  fill: var(--steel) !important;
}
.stButton > button{
  min-height: 48px;
  border-radius: 16px !important;
  font-weight: 700 !important;
  padding: 0 1.1rem !important;
  transition: .2s ease !important;
}
.stButton > button[kind="primary"]{
  border: none !important;
  color:#fff !important;
  background: linear-gradient(145deg, var(--steel), var(--steel-2)) !important;
  box-shadow: 0 10px 18px rgba(62,74,89,.16);
}
.stButton > button[kind="primary"]:hover{
  background: linear-gradient(145deg, #2e3a47, #445062) !important;
  transform: translateY(-1px);
}
.stButton > button:not([kind="primary"]){
  background: rgba(255,255,255,.9) !important;
  border: 1px solid var(--line) !important;
  color: var(--charcoal) !important;
}
.stButton > button:not([kind="primary"]):hover{
  border-color: rgba(62,74,89,.5) !important;
}

.stCheckbox label,
.stToggle label{
  color: var(--muted) !important;
  font-weight: 600 !important;
}

[data-testid="stMetric"]{
  background: linear-gradient(180deg, rgba(255,255,255,.96), rgba(247,248,250,.92));
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 1rem 1.1rem;
}
[data-testid="stMetricValue"]{
  color: var(--charcoal) !important;
  font-weight: 800 !important;
}
[data-testid="stMetricLabel"]{
  color: var(--muted) !important;
  font-size: .72rem !important;
  text-transform: uppercase;
  letter-spacing: .12em !important;
  font-weight: 700 !important;
}

[data-testid="stDataFrame"]{
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid var(--line);
}

.state-badge{
  display:inline-flex;
  align-items:center;
  padding:.28rem .55rem;
  border-radius: 999px;
  font-size:.75rem;
  font-weight:700;
}
.state-green{ background: rgba(46,111,96,.10); color: var(--green); }
.state-amber{ background: rgba(168,132,58,.10); color: var(--amber); }
.state-red{ background: rgba(138,75,75,.10); color: var(--red); }
.state-gray{ background: rgba(123,135,148,.12); color: var(--gray); }

@media (max-width: 1200px){
  .hero-grid{ grid-template-columns: 1fr; }
  .filter-grid{ grid-template-columns: repeat(2, minmax(0,1fr)); }
}
@media (max-width: 760px){
  .block-container{ padding-left: .8rem; padding-right: .8rem; }
  .filter-grid{ grid-template-columns: 1fr; }
  .hero-title{ font-size: 2.2rem; }
  .hero-right{ grid-template-columns: 1fr; }
}

.mobile-dock-wrapper{
  display: none;
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 99999;
  width: calc(100% - 3rem);
  max-width: 380px;
}
@media (max-width: 768px){
  section[data-testid="stSidebar"]{ display: none !important; }
  .stApp{ padding-bottom: 7rem !important; }
}

.mobile-native-dock{
  display: none;
  position: fixed;
  bottom: 1.25rem;
  left: 1rem;
  right: 1rem;
  z-index: 9999;
}
@media (max-width: 768px){
  .mobile-native-dock{ display: block; }
}

.mobile-native-dock > div{
  display: flex;
  gap: .5rem;
}
.mobile-native-dock .stButton > button{
  flex: 1;
  min-height: 3.4rem;
  font-size: .74rem !important;
  font-weight: 600 !important;
  padding: .45rem .5rem !important;
  border-radius: 18px !important;
  background: linear-gradient(165deg, rgba(255,255,255,.96), rgba(250,251,253,.94)) !important;
  border: 1px solid rgba(100,110,120,.14) !important;
  color: var(--muted) !important;
  box-shadow: 0 4px 16px rgba(31,41,51,.08) !important;
  transition: all .15s ease !important;
}
.mobile-native-dock .stButton > button:hover{
  border-color: rgba(62,74,89,.25) !important;
  box-shadow: 0 6px 20px rgba(31,41,51,.12) !important;
}
.mobile-native-dock .stButton > button:focus{
  box-shadow: 0 6px 20px rgba(31,41,51,.12), 0 0 0 2px var(--champagne) !important;
}
.mobile-native-dock .stButton > button[kind="primary"]{
  background: linear-gradient(150deg, var(--charcoal), #2d3640) !important;
  color: #fff !important;
  border: none !important;
  box-shadow: 0 6px 20px rgba(31,41,51,.18) !important;
}

.mobile-actions-panel{
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(160deg, rgba(245,246,248,.96), rgba(238,240,242,.94));
  border: 1px solid rgba(100,110,120,.12);
  border-radius: 999px;
  padding: .38rem .35rem;
  box-shadow: 
    0 8px 24px rgba(31,41,51,.11),
    0 1px 3px rgba(31,41,51,.06),
    inset 0 1px 0 rgba(255,255,255,.7);
  backdrop-filter: blur(12px);
  gap: .25rem;
}
.mobile-dock-item{
  flex: 0 0 auto;
  min-width: 0;
  padding: .58rem .7rem .52rem;
  border-radius: 999px;
  text-align: center;
  color: var(--muted);
  font-size: .68rem;
  font-weight: 600;
  cursor: pointer;
  transition: all .18s ease;
  text-decoration: none;
}
.mobile-dock-item:hover{
  color: var(--charcoal);
  background: rgba(31,41,51,.04);
}
.mobile-dock-item.active{
  background: linear-gradient(145deg, var(--charcoal), #2d3640);
  color: #fff;
  box-shadow: 0 4px 12px rgba(31,41,51,.2);
}
.mobile-dock-item.actions{
  flex: 0 0 auto;
  padding: .68rem 1.1rem .62rem;
  background: linear-gradient(145deg, var(--charcoal), #2d3640);
  color: #fff;
  border-radius: 999px;
  box-shadow: 0 4px 14px rgba(31,41,51,.22);
  margin: 0 .15rem;
}
.mobile-dock-item.actions:hover{
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(31,41,51,.28);
}
.mobile-dock-icon{
  display: block;
  font-size: 1.05rem;
  margin: 0 auto .1rem;
}

.actions-menu{
  display: none;
  position: fixed;
  bottom: 5.8rem;
  left: 50%;
  transform: translateX(-50%) scale(.96);
  width: calc(100% - 3rem);
  max-width: 340px;
  background: linear-gradient(165deg, rgba(255,255,255,.98), rgba(250,251,253,.96));
  border: 1px solid rgba(180,175,165,.18);
  border-radius: 20px;
  padding: .6rem .5rem;
  box-shadow: 
    0 18px 48px rgba(31,41,51,.18),
    0 6px 16px rgba(31,41,51,.1),
    inset 0 1px 0 rgba(255,255,255,.8);
  opacity: 0;
  visibility: hidden;
  transition: all .2s cubic-bezier(.4,0,.2,1);
  z-index: 99998;
}
.actions-menu.open{
  display: block;
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) scale(1);
}
.actions-menu-item{
  display: block;
  width: 100%;
  padding: .72rem .85rem;
  border-radius: 14px;
  color: var(--charcoal);
  font-size: .8rem;
  font-weight: 600;
  text-decoration: none;
  text-align: left;
  cursor: pointer;
  transition: all .16s ease;
  border: none;
  background: transparent;
  margin: .12rem 0;
}
.actions-menu-item:hover{
  background: rgba(31,41,51,.045);
}
.actions-menu-item:first-child{
  margin-top: 0;
}
.actions-menu-divider{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(100,110,120,.12), transparent);
  margin: .5rem 0;
}

.mobile-actions-panel{
  display: block;
  background: linear-gradient(165deg, rgba(255,255,255,.97), rgba(250,251,253,.95));
  border: 1px solid rgba(100,110,120,.14);
  border-radius: 16px;
  padding: .6rem .5rem;
  margin-bottom: .6rem;
  box-shadow: 0 8px 24px rgba(31,41,51,.1);
}
.mobile-actions-panel-title{
  font-size: .64rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: var(--champagne);
  margin-bottom: .5rem;
  text-align: center;
}
.mobile-actions-panel .stButton > button{
  font-size: .7rem !important;
  padding: .45rem .5rem !important;
  border-radius: 14px !important;
  font-weight: 600 !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

def a_float_seguro(valor, default=0.0):
    if valor is None:
        return default

    if isinstance(valor, (int, float)):
        try:
            if pd.isna(valor):
                return default
        except Exception:
            pass
        return float(valor)

    texto = str(valor).strip()

    if texto == "":
        return default

    texto_lower = texto.lower()
    if texto_lower in {"none", "null", "nan", "-", "--"}:
        return default

    # limpia símbolos comunes
    texto = texto.replace("$", "").replace("usd", "").replace("ars", "").strip()

    # normalización simple:
    # 1.430 -> 1430
    # 1,430.50 -> 1430.50
    # 1430,50 -> 1430.50
    if "." in texto and "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")

    # quita espacios remanentes
    texto = texto.replace(" ", "")

    try:
        return float(texto)
    except ValueError:
        return default


def formato_moneda(valor):
    numero = a_float_seguro(valor, 0.0)
    if numero == 0:
        return "-"
    return f"$ {numero:,.0f}".replace(",", ".")

def formato_pct(valor):
    numero = a_float_seguro(valor, 0.0)
    if numero == 0:
        return "-"
    return f"{numero:.1f}%"


def obtener_producto_por_clave(df: pd.DataFrame, clave: str) -> tuple:
    if not clave or clave == "Seleccionar...":
        return None, None, None
    parts = clave.split("||")
    if len(parts) != 2:
        return None, None, None
    codigo, competidor = parts[0], parts[1]
    mask = (df["codigo_reyes"].astype(str) == codigo) & (df["competidor"].astype(str) == competidor)
    df_filt = df[mask]
    if df_filt.empty:
        return None, None, None
    return df_filt.iloc[0], codigo, competidor


def obtener_producto_por_clave_tres(df: pd.DataFrame, clave: str) -> tuple:
    if not clave or clave == "Seleccionar...":
        return None, None, None
    parts = clave.split("||")
    if len(parts) != 3:
        return None, None, None
    codigo, competidor = parts[0], parts[1]
    mask = (df["codigo_reyes"].astype(str) == codigo) & (df["competidor"].astype(str) == competidor)
    df_filt = df[mask]
    if df_filt.empty:
        return None, None, None
    return df_filt.iloc[0], codigo, competidor


def filtrar_productos_reales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["_codigo_str"] = df["codigo_reyes"].astype(str).str.lower().str.strip()
    df["_competidor_str"] = df["competidor"].astype(str).str.lower().str.strip()
    patron = "|".join(["copiar desde", "productos_reyes", "redlenic o", "impotekno o"])
    mask = df["_codigo_str"].str.contains(patron, na=False) | df["_competidor_str"].str.contains(patron, na=False)
    df = df[~mask]
    df = df[df["_codigo_str"].str.len() > 0]
    df = df[df["_competidor_str"].str.len() > 0]
    return df.drop(columns=["_codigo_str", "_competidor_str"], errors="ignore")


def render_sidebar():
    st.markdown(
        """
        <div class="sidebar-brand">
          <div class="sidebar-mark">CSL</div>
          <div>
            <div class="sidebar-title">CSL Monitor</div>
            <div class="sidebar-subtitle">Pricing desk · Reyes</div>
          </div>
        </div>
        <div class="sidebar-note">
          Herramienta interna para lectura competitiva, rentabilidad y operación comercial.
        </div>
        <div class="sidebar-label">Navegación</div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str, chips: list[tuple[str, str, str]]):
    chips_html = "".join(
        f"""
        <div class="hero-chip">
          <div class="hero-chip-label">{label}</div>
          <div class="hero-chip-value">{value}</div>
          <div class="hero-chip-note">{note}</div>
        </div>
        """
        for label, value, note in chips
    )
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-grid">
            <div class="hero-left">
              <div class="hero-kicker">Pricing intelligence</div>
              <div class="hero-brand">
                <div class="hero-mark">CSL</div>
                <div>
                  <h1 class="hero-title">{title}</h1>
                  <div class="hero-subtitle">{subtitle}</div>
                </div>
              </div>
            </div>
            <div class="hero-right">{chips_html}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(eyebrow: str, title: str, copy: str, meta: str | None = None):
    right = f'<div class="section-meta">{meta}</div>' if meta else ""
    st.markdown(
        f"""
        <div class="section-card">
          <div style="display:flex;justify-content:space-between;gap:1rem;align-items:end;">
            <div>
              <div class="section-eyebrow">{eyebrow}</div>
              <div class="section-title">{title}</div>
              <div class="section-copy">{copy}</div>
            </div>
            {right}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_data_shell_open(title: str, copy: str, actions_right: str = ""):
    st.markdown(
        f"""
        <div class="data-shell">
          <div class="data-shell-top">
            <div>
              <div class="data-shell-title">{title}</div>
              <div class="data-shell-copy">{copy}</div>
            </div>
            <div class="data-shell-actions">{actions_right}</div>
          </div>
          <div class="data-shell-inner">
        """,
        unsafe_allow_html=True,
    )


def render_data_shell_close():
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_kpi(label: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="kpi">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pagina_dashboard():
    resumen = dashboard_data.obtener_resumen()
    chips = [
        ("productos activos", str(resumen["total_productos"]), "base monitoreada"),
        ("modo dólar", str(resumen["dolar_modo"]).upper(), "criterio vigente"),
        ("referencia", formato_moneda(resumen["dolar_actual"]), "tipo de cambio"),
        ("sin dato", str(resumen.get("sin_dato", 0)), "faltante competencia"),
    ]
    render_hero(
        "CSL Monitor",
        "Monitoreo competitivo y rentabilidad con lectura comercial ejecutiva.",
        chips,
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        ("productos activos", resumen["total_productos"], "base monitoreada"),
        ("competitivos", resumen["productos_verdes"], "posición sana"),
        ("ajustados", resumen["alertas_amarillas"], "requieren mirada"),
        ("alertas rojas", resumen["alertas_rojas"], "riesgo inmediato"),
        ("sin dato", resumen.get("sin_dato", 0), "faltante competencia"),
        ("dólar oficial", formato_moneda(resumen["dolar_actual"]), str(resumen["dolar_modo"])),
    ]
    for col, item in zip([c1, c2, c3, c4, c5, c6], cards):
        with col:
            render_kpi(item[0], str(item[1]), item[2])

    df, quality = dashboard_data.obtener_productos_con_calidad()

    stats_calidad = dashboard_data.obtener_estadisticas_calidad()

    with st.expander("📊 Tablero de Calidad de Datos", expanded=False):
        cq1, cq2, cq3, cq4, cq5 = st.columns(5)
        with cq1:
            st.metric("Warnings activos", stats_calidad["warnings_activos"])
        with cq2:
            st.metric("Filas plantilla", stats_calidad["filas_plantilla"])
        with cq3:
            st.metric("Precios sospechosos", stats_calidad["productos_sospechosos"])
        with cq4:
            st.metric("Problemas costo", stats_calidad["problemas_costo"])
        with cq5:
            st.metric("Problemas margen", stats_calidad["problemas_margen"])
        if quality.get("warnings"):
            with st.expander("Ver detalle de advertencias", expanded=False):
                for w in quality["warnings"]:
                    st.markdown(f"- **{w.get('type', 'AVISO')}**: {w.get('message', '')}")

    df_historial = dashboard_data.obtener_historial(limite=5)
    if not df_historial.empty:
        with st.expander("📋 Cambios Recientes", expanded=False):
            for _, row in df_historial.iterrows():
                tipo = str(row.get("tipo_accion", "") or "").strip()
                codigo = str(row.get("codigo_reyes", "") or "").strip()
                competidor = str(row.get("competidor", "") or "").strip()
                campo = str(row.get("campo", "") or "").strip()
                anterior = str(row.get("valor_anterior", "") or "").strip()
                nuevo = str(row.get("valor_nuevo", "") or "").strip()
                fecha_raw = row.get("fecha", "")
                fecha = str(fecha_raw)[:16] if fecha_raw else ""

                if tipo == "CAMBIO_CONFIG":
                    titulo = "Config"
                    detalle = f"{campo}: {anterior} -> {nuevo}"
                elif tipo == "ACTUALIZACION_PRECIO":
                    titulo = "Precio competidor"
                    detalle = f"{codigo} / {competidor}: {anterior} -> {nuevo}"
                elif tipo == "CAMBIO_ESTADO":
                    titulo = "Estado"
                    detalle = f"{codigo} / {competidor}: {anterior} -> {nuevo}"
                elif tipo == "EDICION_PRODUCTO":
                    titulo = "Edición"
                    detalle = f"{codigo} / {competidor} - {campo}: {anterior} -> {nuevo}"
                else:
                    titulo = tipo or "Cambio"
                    detalle = f"{campo}: {anterior} -> {nuevo}"

                st.caption(f"{fecha} - **{titulo}** - {detalle}")

    render_section_header(
        "CSL Monitor",
        "Vista comercial",
        "Filtrá, ordená y leé rápidamente la situación competitiva de los productos monitoreados.",
        f"{len(df)} registros",
    )

    ff1, ff2, ff3, ff4 = st.columns([1, 1, 1, 1.3])
    with ff1:
        competidores = ["Todos"] + sorted(df["competidor"].dropna().unique().tolist())
        competidor_sel = st.selectbox("Competidor", competidores)
    with ff2:
        estados = ["Todos", "VERDE", "AMARILLO", "ROJO", "SIN_DATO"]
        estado_sel = st.selectbox("Estado", estados)
    with ff3:
        orden_opciones = ["Código", "Precio Reyes", "Precio Comp.", "Diferencia", "Margen", "Ganancia"]
        orden_sel = st.selectbox("Ordenar por", orden_opciones)
    with ff4:
        busqueda = st.text_input("Buscar", placeholder="Código, descripción o competidor...")

    df_filtro = df.copy()
    if competidor_sel != "Todos":
        df_filtro = df_filtro[df_filtro["competidor"] == competidor_sel]
    if estado_sel != "Todos":
        df_filtro = df_filtro[df_filtro["estado"] == estado_sel]
    if busqueda:
        b = busqueda.lower().strip()
        mask = (
            df_filtro["codigo_reyes"].astype(str).str.lower().str.contains(b, na=False)
            | df_filtro["descripcion_reyes"].astype(str).str.lower().str.contains(b, na=False)
            | df_filtro["competidor"].astype(str).str.lower().str.contains(b, na=False)
        )
        df_filtro = df_filtro[mask]

    orden_mapeo = {
        "Código": ("codigo_reyes", True),
        "Precio Reyes": ("precio_reyes_ars", False),
        "Precio Comp.": ("precio_competidor_actual_ars", False),
        "Diferencia": ("diferencia_vs_competidor_pct", False),
        "Margen": ("margen_real_pct", True),
        "Ganancia": ("ganancia_ars", False),
    }
    col, asc = orden_mapeo.get(orden_sel, ("codigo_reyes", True))
    df_filtro = df_filtro.sort_values(col, ascending=asc)

    cols = [
        "codigo_reyes", "descripcion_reyes", "competidor", "precio_reyes_ars",
        "precio_competidor_actual_ars", "diferencia_vs_competidor_pct", "margen_real_pct",
        "estado", "accion_recomendada", "motivo_accion"
    ]
    df_tbl = df_filtro[cols].copy()
    df_tbl["precio_reyes_ars"] = df_tbl["precio_reyes_ars"].apply(formato_moneda)
    df_tbl["precio_competidor_actual_ars"] = df_tbl["precio_competidor_actual_ars"].apply(formato_moneda)
    df_tbl["diferencia_vs_competidor_pct"] = df_tbl["diferencia_vs_competidor_pct"].apply(formato_pct)
    df_tbl["margen_real_pct"] = df_tbl["margen_real_pct"].apply(formato_pct)
    df_tbl.columns = ["Código", "Descripción", "Competidor", "Precio Reyes", "Precio Comp.", "Diferencia", "Margen", "Estado", "Acción", "Motivo"]

    csv = df_tbl.to_csv(index=False).encode("utf-8")
    actions = '<span>Descarga disponible</span>'
    render_data_shell_open("Productos monitoreados", "Lectura competitiva principal del sistema.", actions)

    top_left, top_right = st.columns([7, 2])
    with top_left:
        st.caption("La tabla refleja los filtros activos y permite una lectura rápida por estado, acción y motivo.")
    with top_right:
        vista_ampliada = st.checkbox("Vista ampliada", value=False)
    filas = 16 if vista_ampliada else 10
    st.dataframe(df_tbl, hide_index=True, height=filas * 36 + 40, width="stretch")
    st.download_button("Exportar CSV", data=csv, file_name="productos_sfl.csv", use_container_width=True)
    render_data_shell_close()

    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="alert-card"><div class="data-shell-title">Alertas</div><div class="data-shell-copy">Productos que necesitan revisión inmediata o dato faltante.</div>', unsafe_allow_html=True)
        rojas = df[df["estado"] == "ROJO"]
        if rojas.empty:
            st.info("Sin alertas rojas.")
        else:
            for _, r in rojas.iterrows():
                st.markdown(f'<div class="alert-item red"><strong>{r["codigo_reyes"]}</strong> · {r["descripcion_reyes"][:60]}</div>', unsafe_allow_html=True)
        sin_dato = df[df["estado"] == "SIN_DATO"]
        if not sin_dato.empty:
            for _, r in sin_dato.iterrows():
                st.markdown(f'<div class="alert-item gray"><strong>{r["codigo_reyes"]}</strong> · {r["descripcion_reyes"][:60]}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="alert-card"><div class="data-shell-title">Prioridades</div><div class="data-shell-copy">Orden sugerido de revisión comercial.</div>', unsafe_allow_html=True)
        df_prior = df.sort_values(["estado", "margen_real_pct"], ascending=[True, True]).head(5)
        for i, (_, r) in enumerate(df_prior.iterrows(), start=1):
            causa = "Alerta roja" if r["estado"] == "ROJO" else ("Sin precio competidor" if r["estado"] == "SIN_DATO" else "Margen ajustado")
            st.markdown(
                f"""
                <div class="priority-item">
                  <div class="priority-top">
                    <strong>{i}. {r["codigo_reyes"]}</strong>
                    <span>{r["estado"]}</span>
                  </div>
                  <div style="margin-top:.25rem;">{r["descripcion_reyes"][:56]}</div>
                  <div class="priority-cause">{causa}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def pagina_operaciones():
    accion_query = obtener_accion_actual()
    opciones = [
        "⚡ Actualización Rápida",
        "➕ Alta de Producto",
        "✏️ Editar Producto",
        "✅ Activar/Desactivar"
    ]
    if "operacion_default" in st.session_state:
        indice_default = st.session_state.operacion_default
    else:
        indice_default = 0
    
    if accion_query in ["rapid", "alta", "edit", "estado"]:
        if accion_query == "rapid":
            indice_default = 0
        elif accion_query == "alta":
            indice_default = 1
        elif accion_query == "edit":
            indice_default = 2
        elif accion_query == "estado":
            indice_default = 3
    
    render_hero(
        "Operaciones",
        "Gestión manual de precios, productos y estado operativo del monitoreo.",
        [
            ("actualización", "rápida", "carga inmediata"),
            ("edición", "producto", "ajuste controlado"),
            ("estado", "activo/inactivo", "gestión de base"),
            ("config", "manual", "control interno"),
        ],
    )
    opcion = st.radio(
        "Seleccionar operación",
        opciones,
        index=indice_default,
        horizontal=True,
        label_visibility="collapsed",
    )

    if opcion == "⚡ Actualización Rápida":
        render_section_header("Operaciones", "Actualización rápida", "Registrá un nuevo precio competidor sobre un producto ya monitoreado.")
        df = excel_service.obtener_productos_todos()
        df = filtrar_productos_reales(df)
        cfg = excel_service.cargar_config()
        df = calculations.procesar_productos(df, cfg)

        if df.empty:
            st.info("No hay productos disponibles para actualizar.")
            return

        df["clave"] = df["codigo_reyes"].astype(str) + "||" + df["competidor"].astype(str)
        sel = st.selectbox("Producto", ["Seleccionar..."] + sorted(df["clave"].unique().tolist()))
        prod, codigo, competidor = obtener_producto_por_clave(df, sel)

        if sel != "Seleccionar...":
            if prod is None:
                st.error("No se encontró el producto seleccionado. Actualizá la página e intentá nuevamente.")
            else:
                c1, c2 = st.columns([1, 2])
                with c1:
                    prev_price = prod.get("precio_competidor_anterior_ars")
                    curr_price = prod.get("precio_competidor_actual_ars", 0)
                    delta = None
                    if prev_price and prev_price != curr_price:
                        curr_price - prev_price
                    st.metric("Actual", formato_moneda(curr_price), 
                             f"Anterior: {formato_moneda(prev_price) if prev_price else '-'}")
                with c2:
                    mover = st.checkbox("Mover actual a anterior", value=True)
                nuevo = st.number_input("Nuevo precio competidor", min_value=0.0, step=1.0)
                if st.button("Actualizar precio", type="primary"):
                    if excel_service.actualizar_precio_competidor(codigo, competidor, nuevo, mover):
                        st.success("Actualizado correctamente.")
                        st.rerun()
                    else:
                        st.error("Error al actualizar.")

    elif opcion == "➕ Alta de Producto":
        render_section_header("Operaciones", "Alta de producto", "Agregá un producto nuevo a la base de monitoreo.")
        c1, c2 = st.columns(2)
        with c1:
            codigo = st.text_input("Código Reyes *")
            desc = st.text_input("Descripción *")
            competidor = st.text_input("Competidor *")
            costo = st.number_input("Costo USD", min_value=0.0, step=0.01)
        with c2:
            precio_r = st.number_input("Precio Reyes ARS", min_value=0.0, step=1.0)
            margen = st.number_input("Margen mínimo %", min_value=0.0, value=20.0, step=1.0)
            url = st.text_input("URL Categoría")
            ref = st.text_input("Referencia")
        if st.button("Crear producto", type="primary"):
            if not codigo or not desc or not competidor:
                st.error("Completá los campos obligatorios.")
            elif excel_service.verificar_codigo_existe(codigo, competidor):
                st.warning("El producto ya existe.")
            else:
                producto = {
                    "codigo_reyes": codigo,
                    "descripcion_reyes": desc,
                    "competidor": competidor,
                    "costo_usd": costo,
                    "precio_reyes_ars": precio_r,
                    "margen_minimo_pct": margen,
                    "url_categoria_competidor": url,
                    "referencia_manual_competidor": ref,
                    "activo": "SI",
                    "precio_competidor_actual_ars": 0,
                    "precio_competidor_anterior_ars": 0,
                }
                if excel_service.insertar_producto(producto):
                    st.success("Producto creado.")
                    st.rerun()
                else:
                    st.error("Error al crear.")

    elif opcion == "✏️ Editar Producto":
        render_section_header("Operaciones", "Editar producto", "Modificá campos principales de un producto existente.")
        df = excel_service.obtener_productos_todos()
        df = filtrar_productos_reales(df)
        cfg = excel_service.cargar_config()
        df = calculations.procesar_productos(df, cfg)

        if df.empty:
            st.info("No hay productos disponibles para editar.")
            return

        df["clave"] = df["codigo_reyes"].astype(str) + "||" + df["competidor"].astype(str)
        sel = st.selectbox("Producto", ["Seleccionar..."] + sorted(df["clave"].unique().tolist()))
        prod, codigo, competidor = obtener_producto_por_clave(df, sel)

        if sel != "Seleccionar...":
            if prod is None:
                st.error("No se encontró el producto seleccionado. Actualizá la página e intentá nuevamente.")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    precio_r = st.number_input("Precio Reyes ARS", value=float(prod.get("precio_reyes_ars", 0) or 0), step=1.0)
                    costo = st.number_input("Costo USD", value=float(prod.get("costo_usd", 0) or 0), step=0.01)
                with c2:
                    precio_c = st.number_input("Precio Competidor ARS", value=float(prod.get("precio_competidor_actual_ars", 0) or 0), step=1.0)
                    margen = st.number_input("Margen mínimo %", value=float(prod.get("margen_minimo_pct", 20) or 20), step=1.0)
                if st.button("Guardar cambios", type="primary"):
                    datos = {
                        "precio_reyes_ars": precio_r,
                        "costo_usd": costo,
                        "precio_competidor_actual_ars": precio_c,
                        "margen_minimo_pct": margen,
                    }
                    if excel_service.actualizar_producto(codigo, competidor, datos):
                        st.success("Actualizado.")
                        st.rerun()
                    else:
                        st.error("Error.")

    elif opcion == "✅ Activar/Desactivar":
        render_section_header("Operaciones", "Estado de producto", "Activá o desactivá registros dentro del monitoreo.")
        f1, f2 = st.columns([1.2, 1.8])
        with f1:
            filtro_sel = st.selectbox("Filtrar por estado", ["Todos", "Activos", "Inactivos"])
        with f2:
            st.caption("Podés recuperar productos inactivos y volver a incluirlos en la operatoria.")

        df = excel_service.obtener_productos_todos()
        df = filtrar_productos_reales(df)
        df["estado"] = (
            df["activo"].astype(str).str.upper().map({"SI": "ACTIVO", "YES": "ACTIVO", "1": "ACTIVO", "TRUE": "ACTIVO"}).fillna("INACTIVO")
        )
        if filtro_sel == "Activos":
            df = df[df["estado"] == "ACTIVO"]
        elif filtro_sel == "Inactivos":
            df = df[df["estado"] == "INACTIVO"]

        df["clave"] = df["codigo_reyes"].astype(str) + "||" + df["competidor"].astype(str) + "||" + df["estado"]
        sel = st.selectbox("Producto", ["Seleccionar..."] + sorted(df["clave"].unique().tolist()))
        prod, codigo, competidor = obtener_producto_por_clave_tres(df, sel)

        if sel != "Seleccionar...":
            if prod is None:
                st.error("No se encontró el producto seleccionado. Actualizá la página e intentá nuevamente.")
            else:
                estado_txt = "ACTIVO" if str(prod.get("activo", "NO")).upper() in ["SI", "YES", "1", "TRUE"] else "INACTIVO"
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Estado actual", estado_txt)
                with c2:
                    nuevo_estado = st.toggle("Activo", value=(estado_txt == "ACTIVO"))
                if st.button("Cambiar estado", type="primary"):
                    if excel_service.cambiar_estado_producto(codigo, competidor, nuevo_estado):
                        st.success("Estado actualizado.")
                        st.rerun()
                    else:
                        st.error("Error.")


def pagina_configuracion():
    cfg = excel_service.cargar_config()
    render_hero(
        "Configuración",
        "Parámetros manuales del sistema para criterio de cálculo y operación.",
        [
            ("oficial", formato_moneda(cfg.get("dolar_oficial", 0)), "base actual"),
            ("blue", formato_moneda(cfg.get("dolar_blue", 0)), "referencia alterna"),
            ("modo", str(cfg.get("dolar_modo", "oficial")).upper(), "criterio activo"),
            ("frecuencia", str(cfg.get("frecuencia_monitoreo_minutos", "-")), "minutos"),
        ],
    )
    render_section_header("Sistema", "Parámetros de cálculo", "Actualizá las referencias centrales del monitoreo.")
    c1, c2, c3 = st.columns(3)
    with c1:
        oficial = st.number_input("Dólar Oficial", value=float(cfg.get("dolar_oficial", 1430)), step=10.0)
    with c2:
        blue = st.number_input("Dólar Blue", value=float(cfg.get("dolar_blue", 0)), step=10.0)
    with c3:
        modo_idx = 0 if cfg.get("dolar_modo", "oficial") == "oficial" else 1
        modo = st.selectbox("Modo", ["oficial", "blue"], index=modo_idx)

    if st.button("Guardar configuración", type="primary"):
        ok = True
        ok = ok and excel_service.actualizar_dolar("dolar_oficial", oficial)
        ok = ok and excel_service.actualizar_dolar("dolar_blue", blue)
        ok = ok and excel_service.actualizar_dolar("dolar_modo", modo)
        if ok:
            st.success("Configuración guardada.")
            st.rerun()
        else:
            st.error("Error al guardar.")


def obtener_pagina_actual() -> str:
    params = st.query_params
    if "page" in params:
        return params["page"]
    return "Dashboard"


def obtener_accion_actual() -> str:
    params = st.query_params
    if "action" in params:
        return params["action"]
    return None


def render_mobile_dock():
    if "mobile_page" not in st.session_state:
        st.session_state.mobile_page = "Dashboard"
    if "mobile_actions_open" not in st.session_state:
        st.session_state.mobile_actions_open = False
    if "operacion_default" not in st.session_state:
        st.session_state.operacion_default = 0
    
    pagina_actual = st.session_state.mobile_page
    
    st.markdown('<div class="mobile-native-dock">', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c1:
        if st.button("Panel", use_container_width=True, type="primary" if pagina_actual == "Dashboard" else "secondary"):
            st.session_state.mobile_page = "Dashboard"
            st.session_state.mobile_actions_open = False
            st.rerun()
    with c2:
        label_btn = "Acciones" if not st.session_state.mobile_actions_open else "Cerrar"
        tipo_btn = "secondary"
        if st.button(label_btn, use_container_width=True, type=tipo_btn):
            st.session_state.mobile_actions_open = not st.session_state.mobile_actions_open
            st.rerun()
    with c3:
        if st.button("Config", use_container_width=True, type="primary" if pagina_actual == "Configuración" else "secondary"):
            st.session_state.mobile_page = "Configuración"
            st.session_state.mobile_actions_open = False
            st.rerun()
    
    if st.session_state.mobile_actions_open:
        st.markdown('<div class="mobile-actions-panel">', unsafe_allow_html=True)
        st.markdown('<div class="mobile-actions-panel-title">Acciones rápidas</div>', unsafe_allow_html=True)
        
        c_act1, c_act2 = st.columns(2)
        with c_act1:
            if st.button("⚡ Actualización rápida", use_container_width=True):
                st.session_state.mobile_page = "Operaciones"
                st.session_state.operacion_default = 0
                st.session_state.mobile_actions_open = False
                st.rerun()
        with c_act2:
            if st.button("➕ Alta de producto", use_container_width=True):
                st.session_state.mobile_page = "Operaciones"
                st.session_state.operacion_default = 1
                st.session_state.mobile_actions_open = False
                st.rerun()
        
        c_act3, c_act4 = st.columns(2)
        with c_act3:
            if st.button("✏️ Editar producto", use_container_width=True):
                st.session_state.mobile_page = "Operaciones"
                st.session_state.operacion_default = 2
                st.session_state.mobile_actions_open = False
                st.rerun()
        with c_act4:
            if st.button("✅ Activar/Desactivar", use_container_width=True):
                st.session_state.mobile_page = "Operaciones"
                st.session_state.operacion_default = 3
                st.session_state.mobile_actions_open = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.session_state.current_page = st.session_state.mobile_page


def main():
    if "mobile_page" not in st.session_state:
        st.session_state.mobile_page = "Dashboard"
    
    render_mobile_dock()
    
    pagina = st.session_state.mobile_page

    if pagina == "Dashboard":
        pagina_dashboard()
    elif pagina == "Operaciones":
        pagina_operaciones()
    elif pagina == "Configuración":
        pagina_configuracion()


if __name__ == "__main__":
    main()
