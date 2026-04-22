
"""
CSL Monitor - Dashboard UI refined
"""
import streamlit as st
import pandas as pd
from app import dashboard_data, excel_service, calculations, config

st.set_page_config(page_title="CSL Monitor", page_icon="◈", layout="wide")

# Autenticación: inicializar sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

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
  .stApp{ padding-bottom: 8rem !important; }
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

/* DOCK MOBILE - navegación principal - CAPA 1: navegación clara y premium */
.mobile-native-dock > div{
  display: flex;
  gap: .6rem;
}
.mobile-native-dock .stButton > button{
  flex: 1;
  min-height: 3.8rem;
  font-size: .8rem !important;
  font-weight: 700 !important;
  padding: .55rem .65rem !important;
  border-radius: 22px !important;
  background: linear-gradient(180deg, #ffffff, #f5f6f8) !important;
  border: 2px solid rgba(100,110,120,.22) !important;
  color: #1f2933 !important;
  box-shadow: 0 8px 28px rgba(31,41,51,.14) !important;
  transition: all .2s ease !important;
  letter-spacing: .02em;
}
.mobile-native-dock .stButton > button:hover{
  border-color: #bfa67a !important;
  box-shadow: 0 10px 36px rgba(31,41,51,.2) !important;
  transform: translateY(-2px);
}
.mobile-native-dock .stButton > button:active{
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(31,41,51,.16) !important;
}
/* Botón principal "Acciones" - MUY diferente */
.mobile-native-dock .stButton > button[kind="primary"]{
  background: linear-gradient(155deg, #1f2933, #2e3640) !important;
  color: #ffffff !important;
  border: 2px solid #1f2933 !important;
  box-shadow: 0 10px 36px rgba(31,41,51,.3) !important;
}

/* PANEL DE ACCIONES - CAPA 2: módulo operativo MUY diferenciado */
.mobile-actions-panel{
  display: block;
  background: linear-gradient(165deg, #e8eaf0, #f0f2f5) !important;
  border: 2px solid #bfa67a !important;
  border-radius: 18px !important;
  padding: .75rem .65rem !important;
  margin-bottom: .75rem !important;
  box-shadow: 0 14px 40px rgba(31,41,51,.18) !important;
}
.mobile-actions-panel-title{
  font-size: .68rem !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .16em !important;
  color: #bfa67a !important;
  margin-bottom: .6rem !important;
  text-align: center !important;
}
.mobile-actions-panel .stButton > button{
  font-size: .72rem !important;
  font-weight: 600 !important;
  padding: .5rem .6rem !important;
  border-radius: 12px !important;
  background: rgba(255,255,255,.9) !important;
  border: 1px solid rgba(255,255,255,.15) !important;
  color: var(--charcoal) !important;
  box-shadow: 0 2px 8px rgba(0,0,0,.1) !important;
}
.mobile-actions-panel .stButton > button{
  font-size: .72rem !important;
  font-weight: 600 !important;
  padding: .52rem .6rem !important;
  border-radius: 14px !important;
  background: #ffffff !important;
  border: 1px solid rgba(100,110,120,.2) !important;
  color: #1f2933 !important;
}

/* TARJETAS DE CONTENIDO - CAPA 3: menos accionables, más informativas */
.mobile-content-card{
  border: 1px solid rgba(214,218,225,.8) !important;
  border-radius: 16px !important;
  background: rgba(255,255,255,.7) !important;
  box-shadow: 0 4px 16px rgba(31,41,51,.06) !important;
  padding: 1rem !important;
}

[data-testid="stMetric"]{
  border: 1px solid rgba(214,218,225,.7) !important;
  border-radius: 14px !important;
  background: linear-gradient(180deg, rgba(255,255,255,.85), rgba(250,251,253,.82)) !important;
  box-shadow: 0 2px 10px rgba(31,41,51,.04) !important;
  transition: none !important;
}
[data-testid="stMetric"]:hover{
  box-shadow: 0 2px 12px rgba(31,41,51,.06) !important;
  transform: none !important;
}

/* GUIA DE LECTURA / HELP */
.guide-shell{
  background: rgba(255,255,255,.88) !important;
  border: 1px solid rgba(100,110,120,.12) !important;
  border-radius: 16px !important;
  padding: .9rem 1rem !important;
  margin-bottom: 1rem !important;
  box-shadow: 0 4px 14px rgba(31,41,51,.06) !important;
}
.guide-title{
  font-size: .7rem !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .14em !important;
  color: var(--champagne) !important;
  margin-bottom: .5rem !important;
}
.guide-intro{
  font-size: .82rem !important;
  color: var(--muted) !important;
  margin-bottom: .65rem !important;
  line-height: 1.45 !important;
}
.guide-states{
  display: flex;
  flex-wrap: wrap;
  gap: .5rem;
  margin-bottom: .6rem !important;
}
.guide-state-badge{
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  padding: .3rem .5rem !important;
  border-radius: 8px !important;
  font-size: .7rem !important;
  font-weight: 600 !important;
}
.guide-state-badge.green{ background: rgba(46,111,96,.1); color: var(--green); }
.guide-state-badge.amber{ background: rgba(168,132,58,.1); color: var(--amber); }
.guide-state-badge.red{ background: rgba(138,75,75,.1); color: var(--red); }
.guide-state-badge.gray{ background: rgba(123,135,148,.1); color: var(--gray); }
.guide-state-badge .dot{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
.guide-state-desc{
  font-size: .75rem !important;
  color: var(--charcoal) !important;
  font-weight: 500 !important;
}
.guide-tip{
  background: rgba(31,41,51,.04) !important;
  border-left: 3px solid var(--champagne) !important;
  padding: .5rem .7rem !important;
  border-radius: 0 8px 8px 0 !important;
  font-size: .75rem !important;
  color: var(--charcoal) !important;
  font-style: italic;
}
.guide-tip-label{
  font-size: .62rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--champagne);
  margin-bottom: .2rem !important;
}
.guide-section{
  margin-top: .7rem !important;
}
.guide-section-title{
  font-size: .68rem !important;
  font-weight: 700 !important;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: var(--muted-2);
  margin-bottom: .4rem !important;
}
.guide-list{
  list-style: none;
  padding: 0;
  margin: 0;
}
.guide-list li{
  font-size: .75rem;
  color: var(--charcoal);
  padding: .25rem 0;
  border-bottom: 1px solid rgba(214,218,225,.5);
}
.guide-list li:last-child{
  border-bottom: none;
}
.help-chip{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(191,166,122,.15);
  color: var(--champagne);
  font-size: .6rem;
  font-weight: 700;
  cursor: help;
  margin-left: .25rem;
  vertical-align: middle;
}

/* FOOTER conurbaDEV */
.footer-conurbadev{
  margin-top: 3rem;
  padding: 2rem 1rem 2.5rem;
  border-top: 1px solid var(--line-2);
  text-align: center;
  background: var(--surface-2);
}
.footer-conurbadev-content{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .5rem;
}
.footer-conurbadev-logo{
  height: 28px;
  opacity: .7;
}
.footer-conurbadev-text{
  color: var(--muted);
  font-size: .8rem;
  font-weight: 500;
}
.footer-conurbadev-subtext{
  color: var(--muted-2);
  font-size: .72rem;
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


def render_login():
    """Pantalla de login simple para admin."""
    st.markdown("""
    <div class="hero" style="min-height: 320px;">
      <div class="hero-grid" style="justify-items: center;">
        <div class="hero-left" style="text-align: center;">
          <div class="hero-kicker">CSL MONITOR</div>
          <div style="font-size: 1.8rem; font-weight: 700; color: #fff; margin-bottom: .5rem;">
            Pricing Desk Reyes
          </div>
          <div style="color: rgba(255,255,255,.7); font-size: .95rem;">
            Ingresá para acceder al monitor
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Obtener credenciales (puede lanzar error si no están configuradas)
            try:
                usuario_correcto, password_correcto = config.obtener_credenciales()
            except ValueError as e:
                st.error(str(e))
                st.stop()
            
            st.markdown("**Usuario**")
            usuario = st.text_input("Usuario", label_visibility="collapsed", placeholder="Usuario")
            st.markdown("**Contraseña**")
            password = st.text_input("Contraseña", label_visibility="collapsed", type="password", placeholder="Contraseña")
            
            if st.button("Ingresar", type="primary", use_container_width=True):
                if usuario == usuario_correcto and password == password_correcto:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
            
            st.caption("Acceso restringido a usuarios autorizados.")


def render_footer():
    """Footer global con branding conurbaDEV."""
    import os
    logo_path = config.LOGO_CONURBADEV
    
    st.markdown('<div class="footer-conurbadev">', unsafe_allow_html=True)
    
    if os.path.exists(logo_path):
        st.image(logo_path, width=100, output_format="PNG")
    
    st.markdown('<div class="footer-conurbadev-text">Desarrollado por conurbaDEV</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer-conurbadev-subtext">Soluciones digitales a medida</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


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
    
    # Botón cerrar sesión
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()


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


def render_guia_lectura():
    from app import ayuda_contextual
    
    guia_html = """
    <div class="guide-shell">
      <div class="guide-title">Cómo leer esta pantalla</div>
      <div class="guide-intro">
        <strong>Orden de lectura:</strong> 1. KPIs, 2. Alertas, 3. Prioridades, 4. Tabla
      </div>
      <div class="guide-states">
        <div class="guide-state-badge green"><span class="dot"></span> VERDE</div>
        <div class="guide-state-badge amber"><span class="dot"></span> AMARILLO</div>
        <div class="guide-state-badge red"><span class="dot"></span> ROJO</div>
        <div class="guide-state-badge gray"><span class="dot"></span> SIN DATO</div>
      </div>
      <div class="guide-state-desc">
        <strong>Verde:</strong> Rentable y competitivo. Mantener. &nbsp;
        <strong>Amarillo:</strong> Rentable pero encima del competidor. Revisar. &nbsp;
        <strong>Rojo:</strong> Margen bajo o muy encima. Requiere decisión. &nbsp;
        <strong>Sin dato:</strong> Falta precio del competidor. Cargar.
      </div>
      <div style="margin-top:.5rem;font-size:.75rem;color:var(--muted);font-style:italic;">
        No siempre conviene igualar al más barato. La prioridad es sostener competitividad con rentabilidad.
      </div>
    </div>
    """
    st.markdown(guia_html, unsafe_allow_html=True)
    
    with st.expander("📋 Glosario rápido de columnas"):
        col_help = [
            ("Precio propio", ayuda_contextual.obtener_tooltip_columna("precio_reyes_ars")),
            ("Precio competidor", ayuda_contextual.obtener_tooltip_columna("precio_competidor_actual_ars")),
            ("Dif. vs competidor", ayuda_contextual.obtener_tooltip_columna("diferencia_vs_competidor_pct")),
            ("Margen actual", ayuda_contextual.obtener_tooltip_columna("margen_real_pct")),
            ("Margen mínimo", ayuda_contextual.obtener_tooltip_columna("margen_minimo_pct")),
            ("Qué revisar", ayuda_contextual.obtener_tooltip_columna("accion_recomendada")),
        ]
        for col_label, col_tooltip in col_help:
            st.markdown(f"**{col_label}**: {col_tooltip}")
    
    tips = ayuda_contextual.obtener_todos_tips_fijos()
    tips_html = ""
    for tip in tips[:5]:
        tips_html += f"<li>{tip}</li>"
    
    consejos_html = f"""
    <div class="guide-shell" style="margin-top:.6rem;">
      <div class="guide-title">Consejos comerciales</div>
      <ul class="guide-list">
        {tips_html}
      </ul>
    </div>
    """
    st.markdown(consejos_html, unsafe_allow_html=True)


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

    if df.empty or "estado" not in df.columns:
        with st.container(border=True):
            st.markdown("""
            ### Todavía no hay productos monitoreados
            
            La base está vacía. Para comenzar:
            
            1. **Importar desde Excel** (recomendado para cargar varios productos)
               - Descargá la plantilla desde Operaciones → Importar desde Excel
               - Completá tus productos ysubila
               - O usá tu planilla propia adaptada
            
            2. **Alta manual** (para agregar uno por vez)
               - Operaciones → Alta de Producto
               - Completá los datos del producto
            
            Una vez que haya productos, acá verás el dashboard completo con KPIs, alertas y prioridades.
            """)
        return

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

    render_guia_lectura()

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
    df_tbl.columns = ["Codigo", "Descripcion", "Competidor", "Precio propio", "Precio competidor", "Dif. vs competidor", "Margen actual", "Estado", "Que revisar", "Por que"]

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
        st.markdown('<div class="alert-card"><div class="data-shell-title">Alertas</div><div class="data-shell-copy">Productos que necesitan revision inmediata o dato faltante.</div><div style="margin-top:.4rem;font-size:.68rem;color:var(--muted-2);">Primero Rojo, luego Sin dato. No todas requieren accion: validen siempre el impacto en margen.</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="alert-card"><div class="data-shell-title">Prioridades</div><div class="data-shell-copy">Orden sugerido de revision comercial.</div><div style="margin-top:.4rem;font-size:.68rem;color:var(--muted-2);">Orden: 1.Rojo, 2.Sin dato, 3.Amarillo, 4.Verde.</div>', unsafe_allow_html=True)
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
        "✅ Activar/Desactivar",
        "📥 Importar desde Excel"
    ]
    if "operacion_default" in st.session_state:
        indice_default = st.session_state.operacion_default
    else:
        indice_default = 0
    
    if accion_query in ["rapid", "alta", "edit", "estado", "import"]:
        if accion_query == "rapid":
            indice_default = 0
        elif accion_query == "alta":
            indice_default = 1
        elif accion_query == "edit":
            indice_default = 2
        elif accion_query == "estado":
            indice_default = 3
        elif accion_query == "import":
            indice_default = 4
    
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
        st.caption("Usá esta opción para actualizar rápido precios del competidor sin modificar el resto del producto. Es ideal para el seguimiento diario.")
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
        st.caption("Los datos indispensables son: codigo, descripcion, competidor, costo USD y precio propio. Sin el margen minimo correcto la lectura de la app pierde valor.")
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
        st.caption("Conviene editar cuando cambia el costo, el precio propio o el margen minimo. Modificar estos datos cambia la lectura comercial del producto.")
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
        st.caption("Un producto desactivado sale del monitoreo operativo. No conviene desactivar solo porque este en rojo: primero revisá la causa.")
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

    elif opcion == "📥 Importar desde Excel":
        render_section_header("Operaciones", "Importar productos", "Cargá varios productos a la vez desde un archivo Excel.")
        st.caption("Es ideal para cargar tu lista inicial o para agregar muchos productos de una sola vez.")

        with st.expander("ℹ️ ¿Cómo se obtiene el precio del competidor?"):
            st.markdown("""
            **El precio del competidor NO se obtiene automáticamente.**
            
            El flujo es:
            1. Primero relevás manualmente los precios de la competencia (por fuera de la app)
            2. Completás esos datos en la columna `precio_competidor_actual_ars` de la plantilla
            3. Importás el archivo
            4. La app automáticamente compara tu precio con el competidor y calcula diferencias, márgenes, estados y recomendaciones

            Si dejás la columna vacía, el producto se importa como **"SIN DATO"**.
            """)
        
        with st.expander("📚 Guía práctica"):
            with st.container(border=True):
                st.markdown("**¿Tengo que usar solo esta plantilla?**")
                st.markdown("""
                **No.** Podés usar la plantilla descargable de la app como modelo recomendado, pero si ya trabajás con una planilla propia, también podés usarla.
                
                **La plantilla de la app:**
                - Sirve como formato modelo
                - Ayuda a evitar errores
                - Muestra exactamente qué columnas necesita la importación
                
                **Tu planilla propia:**
                - También puede servir para importar
                - Siempre que respete la estructura esperada (mismos nombres de columnas)
                - Si tiene otros nombres o le faltan campos, hay que adaptarla antes
                
                **¿Qué conviene operativamente?**
                - Si ya tenés una planilla de trabajo, no hace falta volver a cargar todo a mano
                - Usá la plantilla de la app como referencia
                - Copiá o adaptá tu información existente
                - Subí ese archivo ya acomodado al formato correcto
                """)
                st.info("No necesitás volver a cargar todos los productos manualmente. Si ya usás una planilla propia, adaptala al formato requerido y usala para importar.")

            col_guide1, col_guide2 = st.columns(2)
            with col_guide1:
                with st.container(border=True):
                    st.markdown("**Paso a paso recomendado**")
                    st.markdown("""
                    1. Descargá plantilla limpia (o prepará la tuya)
                    2. Completá datos de tus productos
                    3. Agregá precios competidor si los tenés
                    4. Subí y previsualizá
                    5. Confirmá la importación
                    6. Revisá el Dashboard
                    """)
            
            with col_guide2:
                with st.container(border=True):
                    st.markdown("**Buenas prácticas**")
                    st.markdown("""
                    - Usá códigos consistentes con tu sistema
                    - Verificá que el costo USD sea correcto
                    - El margen mínimo define tu rentabilidad objetivo
                    - Dejá activo="SI" para productos vigentes
                    - No pongas el mismo producto+competidor dos veces
                    """)
                
                with st.container(border=True):
                    st.markdown("**Qué revisar después de importar**")
                    st.markdown("""
                    - Productos en ROJO: margen bajo mínimo
                    - Productos en AMARILLO: margen ajustado
                    - Productos SIN DATO: falta precio competidor
                    - Productos VERDES: competitivos y rentables
                    """)

        with st.container(border=True):
            st.markdown("### 📥 Bloque 1: Descargar plantilla")
            st.caption("Descargá la plantilla, completá los datos y subila nuevamente.")
            excel_plantilla = excel_service.generar_plantilla_importacion()
            st.download_button(
                label="⬇️ Descargar plantilla Excel",
                data=excel_plantilla,
                file_name="plantilla_importacion_productos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        with st.container(border=True):
            st.markdown("### 📤 Bloque 2: Subir archivo")
            st.caption("Seleccioná el archivo Excel (.xlsx) o CSV que completaste.")
            archivo = st.file_uploader("Seleccionar archivo", type=["xlsx", "csv"], label_visibility="collapsed")

        if archivo:
            try:
                if archivo.name.endswith(".csv"):
                    df_import = pd.read_csv(archivo)
                else:
                    df_import = pd.read_excel(archivo)

                with st.container(border=True):
                    st.markdown("### 👁️ Bloque 3: Vista previa")
                    st.caption(f"Total de filas en el archivo: {len(df_import)}")
                    st.dataframe(df_import.head(10), use_container_width=True)

                with st.container(border=True):
                    st.markdown("### ✅ Bloque 4: Confirmar importación")
                    st.caption("Verificá los datos antes de importar. No se puede deshacer.")
                    
                    hay_duplicados = False
                    if "codigo_reyes" in df_import.columns and "competidor" in df_import.columns:
                        df_import["clave"] = df_import["codigo_reyes"].astype(str).str.strip().str.lower() + "||" + df_import["competidor"].astype(str).str.strip().str.lower()
                        duplicados = df_import[df_import.duplicated(subset=["clave"], keep=False)]
                        if not duplicados.empty:
                            hay_duplicados = True
                            st.warning(f"⚠️ Se detectaron {len(duplicados)} filas con productos duplicados en el mismo archivo. Cada producto+competidor debe aparecer una sola vez.")
                            with st.expander("Ver duplicados"):
                                st.dataframe(duplicados[["codigo_reyes", "competidor"]], use_container_width=True)
                    
                    col_confirm1, col_confirm2 = st.columns([1, 2])
                    with col_confirm1:
                        st.caption("Columnas detectadas:")
                        st.write(", ".join(df_import.columns.tolist()[:5]) + ("..." if len(df_import.columns) > 5 else ""))
                    with col_confirm2:
                        confirmar = st.checkbox("Confirmo que los datos son correctos", value=False)

                    if st.button("🚀 Importar productos", type="primary", disabled=not confirmar or hay_duplicados):
                        resultado = excel_service.importar_productos_desde_excel(df_import)

                        with st.container(border=True):
                            st.markdown("### 📊 Bloque 5: Resultado de importación")
                            
                            r = resultado
                            c1, c2, c3, c4 = st.columns(4)
                            with c1:
                                st.metric("Total filas", r["total"])
                            with c2:
                                st.metric("Nuevos", r["nuevos"])
                            with c3:
                                st.metric("Actualizados", r["actualizados"])
                            with c4:
                                st.metric("Errores", r["errores"])
                            
                            c5, c6 = st.columns(2)
                            with c5:
                                st.metric("Sin precio competidor", r.get("sin_dato", 0))
                            with c6:
                                st.metric("Duplicados en archivo", r.get("duplicados", 0))

                            if r["nuevos"] > 0 or r["actualizados"] > 0:
                                st.success("✅ Importación completada correctamente.")
                            elif r["errores"] > 0:
                                st.error("❌ La importación tuvo errores.")

                            if r["detalles"]:
                                with st.expander("Ver detalles"):
                                    for det in r["detalles"][:50]:
                                        if "duplicado" in det.lower():
                                            st.error(f"- {det}")
                                        else:
                                            st.write(f"- {det}")
                                    if len(r["detalles"]) > 50:
                                        st.write(f"... y {len(r['detalles']) - 50} más")

                            if r["nuevos"] > 0 or r["actualizados"] > 0:
                                st.rerun()

            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

        with st.container(border=True):
            st.markdown("### 📋 Checklist quincenal")
            st.caption("Rutina recomendada cada 15 días para mantener la base actualizada.")
            
            st.checkbox("1. Revisar productos vigentes del Dashboard", disabled=True)
            st.checkbox("2. Desactivar productos que salgan de venta", disabled=True)
            st.checkbox("3. Agregar productos nuevos al monitoreo", disabled=True)
            st.checkbox("4. Relevar precios de competidores", disabled=True)
            st.checkbox("5. Completar Excel con precios nuevos", disabled=True)
            st.checkbox("6. Importar y verificar estados", disabled=True)
            
            st.caption("💡 *Esta es una guía de referencia. Completá las tareas según tu flujo real.*")


def pagina_configuracion():
    cfg = excel_service.cargar_config()
    render_hero(
        "Configuracion",
        "Parametros manuales del sistema para criterio de calculo y operacion.",
        [
            ("oficial", formato_moneda(cfg.get("dolar_oficial", 0)), "base actual"),
            ("blue", formato_moneda(cfg.get("dolar_blue", 0)), "referencia alterna"),
            ("modo", str(cfg.get("dolar_modo", "oficial")).upper(), "criterio activo"),
            ("frecuencia", str(cfg.get("frecuencia_monitoreo_minutos", "-")), "minutos"),
        ],
    )
    
    with st.expander("Ayuda: como impacta el tipo de cambio"):
        st.markdown("""
        **El dolar de referencia se usa para convertir costos a pesos.**
        
        Si este valor no refleja como realmente financiás la operacion, la rentabilidad mostrada puede quedar distorsionada.
        
        - **Dolar oficial:** usalo si tus costos o financiamiento estan en dolar oficial.
        - **Dolar blue:** usalo si tus costos o financiamiento estan en dolar paralelo.
        - **Modo:** define cual de los dos se usa para calcular costo y margen.
        """)
    
    render_section_header("Sistema", "Parametros de calculo", "Actualiza las referencias centrales del monitoreo.")
    c1, c2, c3 = st.columns(3)
    with c1:
        oficial = st.number_input("Dolar Oficial", value=float(cfg.get("dolar_oficial", 1430)), step=10.0)
    with c2:
        blue = st.number_input("Dolar Blue", value=float(cfg.get("dolar_blue", 0)), step=10.0)
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
        
        c_act5, c_act6 = st.columns(2)
        with c_act5:
            if st.button("📥 Importar desde Excel", use_container_width=True):
                st.session_state.mobile_page = "Operaciones"
                st.session_state.operacion_default = 4
                st.session_state.mobile_actions_open = False
                st.rerun()
        with c_act6:
            if st.button("🚪 Cerrar sesión", use_container_width=True):
                st.session_state.autenticado = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.session_state.current_page = st.session_state.mobile_page


def main():
    # Verificar autenticación
    if not st.session_state.get("autenticado", False):
        render_login()
        return
    
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
    
    render_footer()


if __name__ == "__main__":
    main()
