import streamlit as st
import pandas as pd

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(page_title="ROI Ansible Pro", layout="wide")

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
    costo_manual = horas_manual * costo_hora

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
    st.image("/mnt/data/logo-redhat-a-color-rgb__2___1_2RqDB78NsfFPIiO1SfVoPbi4JbXcuLVpJ5JUKnMP.png", width=100)

with col2:
    st.title("💰 ROI Calculator - Ansible (Pro)")
    st.caption("Optimiza decisiones de automatización")

# ----------------------
# SIDEBAR
# ----------------------
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
result = calcular_roi(admins, salario, horas_semana, porc_tareas, reduccion,
                      incidentes, costo_incidente, reduccion_errores, costo_ansible)

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
st.subheader("📊 Comparación")

df = pd.DataFrame({
    "Escenario": ["Actual", "Con Ansible"],
    "Costo": [result['costo_total'], result['costo_total'] - result['ahorro_total']]
})

st.bar_chart(df.set_index("Escenario"))

# ----------------------
# DETAIL
# ----------------------
st.subheader("🔍 Detalle")
col7, col8 = st.columns(2)
col7.metric("Ahorro eficiencia", f"${result['ahorro_tiempo']:,.0f}")
col8.metric("Ahorro errores", f"${result['ahorro_errores']:,.0f}")

# ----------------------
# RESULT MESSAGE
# ----------------------
st.subheader("📢 Resultado")

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

Ahorro estimado: **${result['ahorro_total']:,.0f} / año**  
ROI: **{result['roi']:.1f}%**  
Payback: **{result['payback']:.1f} meses**
""")

# ----------------------
# DOWNLOAD REPORT
# ----------------------
if st.button("📥 Descargar resultados"):
    df_export = pd.DataFrame([result])
    st.download_button("Descargar CSV", df_export.to_csv(index=False), "roi_ansible.csv")

