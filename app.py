import streamlit as st
import pandas as pd

# ----------------------
# CONFIG
# ----------------------
st.set_page_config(
    page_title="ROI de Automatización",
    layout="wide"
)

# ----------------------
# STYLES
# ----------------------
st.markdown("""
<style>
.main {
    background-color: #ffffff;
}

.stMetric {
    background-color: #f8e6e6;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

h1, h2, h3 {
    color: #800000;
}
</style>
""", unsafe_allow_html=True)

# ----------------------
# FUNCTIONS
# ----------------------
def calcular_roi(
    admins,
    salario,
    horas_semana,
    porc_tareas,
    reduccion,
    incidentes,
    costo_incidente,
    reduccion_errores,
    costo_automatizacion
):
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

    roi = (
        ((ahorro_total - costo_automatizacion) / costo_automatizacion) * 100
        if costo_automatizacion > 0 else 0
    )

    payback = (
        (costo_automatizacion / ahorro_total) * 12
        if ahorro_total > 0 else 0
    )

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
st.title("🤖 ROI de Automatización")
st.caption(
    "Calculadora para estimar el retorno de inversión de proyectos de automatización"
)

# ----------------------
# SIDEBAR
# ----------------------
st.sidebar.header("📊 Datos del Cliente")

servidores = st.sidebar.number_input(
    "Cantidad de servidores",
    min_value=1,
    value=100
)

admins = st.sidebar.number_input(
    "Cantidad de administradores",
    min_value=1,
    value=3
)

salario = st.sidebar.number_input(
    "Salario mensual por administrador ($)",
    min_value=0,
    value=2500
)

horas_semana = st.sidebar.number_input(
    "Horas laborales por semana",
    min_value=1,
    value=40
)

porc_tareas = st.sidebar.slider(
    "% de tareas manuales",
    0,
    100,
    60
)

reduccion = st.sidebar.slider(
    "% de automatización esperado",
    0,
    100,
    90
)

incidentes = st.sidebar.number_input(
    "Incidentes mensuales",
    min_value=0,
    value=5
)

costo_incidente = st.sidebar.number_input(
    "Costo promedio por incidente ($)",
    min_value=0,
    value=200
)

reduccion_errores = st.sidebar.slider(
    "% reducción de errores",
    0,
    100,
    80
)

costo_automatizacion = st.sidebar.number_input(
    "Costo anual del proyecto ($)",
    min_value=0,
    value=10000
)

# ----------------------
# CALCULATION
# ----------------------
result = calcular_roi(
    admins,
    salario,
    horas_semana,
    porc_tareas,
    reduccion,
    incidentes,
    costo_incidente,
    reduccion_errores,
    costo_automatizacion
)

# ----------------------
# KPIs
# ----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💼 Costo Actual",
        f"${result['costo_total']:,.0f}"
    )

with col2:
    st.metric(
        "💸 Ahorro Anual",
        f"${result['ahorro_total']:,.0f}"
    )

with col3:
    st.metric(
        "📈 ROI",
        f"{result['roi']:,.1f}%"
    )

st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "⏱ Recuperación (Meses)",
        f"{result['payback']:,.1f}"
    )

with col5:
    st.metric(
        "🕒 Horas Ahorradas",
        f"{result['horas_ahorradas']:,.0f}"
    )

with col6:
    st.metric(
        "💰 Inversión",
        f"${costo_automatizacion:,.0f}"
    )

# ----------------------
# CHART
# ----------------------
st.subheader("📊 Comparación de Escenarios")

df = pd.DataFrame({
    "Escenario": ["Actual", "Automatizado"],
    "Costo": [
        result["costo_total"],
        result["costo_total"] - result["ahorro_total"]
    ]
})

st.bar_chart(df.set_index("Escenario"))

# ----------------------
# DETAIL
# ----------------------
st.subheader("🔍 Detalle de Ahorros")

col7, col8 = st.columns(2)

with col7:
    st.metric(
        "⚙️ Ahorro por Eficiencia",
        f"${result['ahorro_tiempo']:,.0f}"
    )

with col8:
    st.metric(
        "🛡️ Ahorro por Reducción de Errores",
        f"${result['ahorro_errores']:,.0f}"
    )

# ----------------------
# RESULT MESSAGE
# ----------------------
st.subheader("📢 Resultado Ejecutivo")

if result["roi"] > 150:
    st.success(
        f"La inversión es altamente rentable. ROI estimado: {result['roi']:.1f}%"
    )

elif result["roi"] > 80:
    st.warning(
        f"La inversión presenta una buena oportunidad. ROI estimado: {result['roi']:.1f}%"
    )

else:
    st.error(
        f"El ROI proyectado es bajo ({result['roi']:.1f}%)."
    )

# ----------------------
# SUMMARY
# ----------------------
st.markdown(f"""
---
## 📄 Resumen Ejecutivo

La automatización permitiría obtener aproximadamente:

- 💰 **${result['ahorro_total']:,.0f} de ahorro anual**
- 📈 **ROI estimado de {result['roi']:.1f}%**
- ⏱ **Recuperación de la inversión en {result['payback']:.1f} meses**
- 🕒 **{result['horas_ahorradas']:,.0f} horas liberadas al año**
""")

# ----------------------
# EXPORT
# ----------------------
st.subheader("📥 Exportar Resultados")

df_export = pd.DataFrame([{
    "Costo Actual": result["costo_total"],
    "Ahorro Total": result["ahorro_total"],
    "ROI (%)": result["roi"],
    "Payback (Meses)": result["payback"],
    "Horas Ahorradas": result["horas_ahorradas"],
    "Ahorro por Tiempo": result["ahorro_tiempo"],
    "Ahorro por Errores": result["ahorro_errores"]
}])

st.download_button(
    label="📄 Descargar CSV",
    data=df_export.to_csv(index=False),
    file_name="roi_automatizacion.csv",
    mime="text/csv"
)
