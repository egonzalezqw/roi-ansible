import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="ROI Ansible Pro", layout="wide")

# ----------------------
# PATHS (IMPORTANTE)
# ----------------------
BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"

logo_path = ASSETS / "logo.png"
sidebar_img = ASSETS / "nexsys.png"

# ----------------------
# STYLES
# ----------------------
st.markdown("""
<style>
.main {background-color: #ffffff;}
.stMetric {
    background-color: #f8e6e6;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}
h1, h2, h3 {color: #800000;}
</style>
""", unsafe_allow_html=True)

# ----------------------
# FUNCTIONS
# ----------------------
def calcular_roi(admins, salario, horas_semana, porc_tareas, reduccion,
                 incidentes, costo_incidente, reduccion_errores, costo_ansible):

    horas_anuales = horas_semana * 52
    costo_anual_personal = admins * salario * 12

    costo_hora = costo_anual_personal / (admins * horas_anuales)

    horas_manual = horas_anuales * admins * (porc_tareas / 100)
    horas_ahorradas = horas_manual * (reduccion / 100)
    ahorro_tiempo = horas_ahorradas * costo_hora

    costo_errores_actual = incidentes * costo_incidente * 12
    ahorro_errores = costo_errores_actual * (reduccion_errores / 100)

    ahorro_total = ahorro_tiempo + ahorro_errores
    costo_total_actual = costo_anual_personal + costo_errores_actual

    roi = ((ahorro_total - costo_ansible) / costo_ansible) * 100 if costo_ansible > 0 else 0
    payback = (costo_ansible / ahorro_total) * 12 if ahorro_total > 0 else 0

    return {
        "costo_total": costo_total_actual,
        "ahorro_total": ahorro_total,
        "roi": roi,
        "payback": payback,
        "horas_ahorradas": horas_ahorradas,
        "ahorro_tiempo": ahorro_tiempo,
        "ahorro_errores": ahorro_errores
    }

# ----------------------
# HEADER
# ----------------------
col1, col2 = st.columns([1, 5])

with col1:
    try:
        st.image(logo_path, width=100)
    except:
        st.warning("Logo no disponible")

with col2:
    st.title("💰 ROI Calculator - Ansible (Pro)")
    st.caption("Optimiza decisiones de automatización")

# ----------------------
# SIDEBAR
# ----------------------
try:
    st.sidebar.image(sidebar_img, use_column_width=True)
except:
    st.sidebar.warning("Imagen no disponible")

st.sidebar.header("📊 Datos del Cliente")

servidores = st.sidebar.number_input("Servidores", min_value=1, value=100)
admins = st.sidebar.number_input("Administradores", min_value=1, value=3)
salario = st.sidebar.number_input("Salario mensual ($)", min_value=0, value=2500)
horas_semana = st.sidebar.number_input("Horas semanales", min_value=1, value=40)

porc_tareas = st.sidebar.slider("% tareas manuales", 0, 100, 60)
reduccion = st.sidebar.slider("% automatización", 0, 100, 90)

incidentes = st.sidebar.number_input("Incidentes mensuales", min_value=0, value=5)
costo_incidente = st.sidebar.number_input("Costo por incidente", min_value=0, value=200)
reduccion_errores = st.sidebar.slider("% reducción errores", 0, 100, 80)

costo_ansible = st.sidebar.number_input("Costo Ansible anual", min_value=0, value=10000)

# ----------------------
# CALCULATION
# ----------------------
result = calcular_roi(
    admins, salario, horas_semana,
    porc_tareas, reduccion,
    incidentes, costo_incidente,
    reduccion_errores, costo_ansible
)

# ----------------------
# KPIs
# ----------------------
col1, col2, col3 = st.columns(3)

col1.metric("💼 Costo actual", f"${result['costo_total']:,.0f}")
col2.metric("💸 Ahorro", f"${result['ahorro_total']:,.0f}")
col3.metric("📈 ROI", f"{result['roi']:,.1f}%")

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric("⏱ Payback (meses)", f"{result['payback']:,.1f}")
col5.metric("🕒 Horas ahorradas", f"{result['horas_ahorradas']:,.0f}")
col6.metric("⚙️ Inversión", f"${costo_ansible:,.0f}")

# ----------------------
# CHART
# ----------------------
st.subheader("📊 Comparación de escenarios")

df = pd.DataFrame({
    "Escenario": ["Actual", "Con Ansible"],
    "Costo": [
        result['costo_total'],
        result['costo_total'] - result['ahorro_total']
    ]
})

st.bar_chart(df.set_index("Escenario"))

# ----------------------
# DETAIL
# ----------------------
st.subheader("🔍 Detalle de Ahorros")

col7, col8 = st.columns(2)

col7.metric("Ahorro eficiencia", f"${result['ahorro_tiempo']:,.0f}")
col8.metric("Ahorro errores", f"${result['ahorro_errores']:,.0f}")

# ----------------------
# RESULT MESSAGE
# ----------------------
st.subheader("📢 Resultado Ejecutivo")

if result['roi'] > 150:
    st.success(f"Inversión altamente rentable (ROI {result['roi']:.1f}%)")
elif result['roi'] > 80:
    st.warning(f"Buena oportunidad (ROI {result['roi']:.1f}%)")
else:
    st.error(f"ROI bajo ({result['roi']:.1f}%)")

# ----------------------
# SUMMARY
# ----------------------
st.markdown(f"""
---
### 📄 Resumen Ejecutivo

Con Ansible, la organización puede ahorrar aproximadamente:

- 💰 **${result['ahorro_total']:,.0f} al año**
- 📈 **ROI de {result['roi']:.1f}%**
- ⏱ Recuperación en **{result['payback']:.1f} meses**
""")

# ----------------------
# DOWNLOAD
# ----------------------
st.subheader("📥 Exportar resultados")

df_export = pd.DataFrame([result])

st.download_button(
    label="Descargar CSV",
    data=df_export.to_csv(index=False),
    file_name="roi_ansible.csv",
    mime="text/csv"
)
