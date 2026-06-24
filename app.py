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
# CSS MEJORADO (FIX MOBILE + CONTRASTE)
# ----------------------
st.markdown("""
<style>

/* Fondo general */
.main {
    background-color: #ffffff;
}

/* FIX CRÍTICO: st.metric en móvil */
.stMetric {
    background-color: #f3f4f6 !important;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid #e5e7eb;
}

/* Forzar visibilidad de texto dentro de métricas */
.stMetric * {
    color: #111827 !important;
}

/* Mejora títulos */
h1, h2, h3 {
    color: #7f1d1d;
}

/* Subtítulo tipo caption más visible */
[data-testid="stCaptionContainer"] {
    color: #374151 !important;
}

/* Cards personalizados para secciones */
.card {
    background: #ffffff;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Mejor separación en móvil */
@media (max-width: 768px) {
    .stMetric {
        margin-bottom: 12px;
    }
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
st.caption("Calculadora para estimar el retorno de inversión de proyectos de automatización")

# ----------------------
# SIDEBAR
# ----------------------
st.sidebar.header("📊 Datos del Cliente")

admins = st.sidebar.number_input("Cantidad de administradores", min_value=1, value=3)
salario = st.sidebar.number_input("Salario mensual ($)", min_value=0, value=2500)
horas_semana = st.sidebar.number_input("Horas por semana", min_value=1, value=40)

porc_tareas = st.sidebar.slider("% tareas manuales", 0, 100, 60)
reduccion = st.sidebar.slider("% automatización", 0, 100, 90)

incidentes = st.sidebar.number_input("Incidentes mensuales", min_value=0, value=5)
costo_incidente = st.sidebar.number_input("Costo incidente ($)", min_value=0, value=200)

reduccion_errores = st.sidebar.slider("% reducción errores", 0, 100, 80)

costo_automatizacion = st.sidebar.number_input("Costo proyecto ($)", min_value=0, value=10000)

# ----------------------
# CALCULO
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
    st.metric("💼 Costo Actual", f"${result['costo_total']:,.0f}")

with col2:
    st.metric("💸 Ahorro Anual", f"${result['ahorro_total']:,.0f}")

with col3:
    st.metric("📈 ROI", f"{result['roi']:,.1f}%")

st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("⏱ Payback (meses)", f"{result['payback']:,.1f}")

with col5:
    st.metric("🕒 Horas ahorradas", f"{result['horas_ahorradas']:,.0f}")

with col6:
    st.metric("💰 Inversión", f"${costo_automatizacion:,.0f}")

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
# RESULTADO
# ----------------------
st.subheader("📢 Resultado Ejecutivo")

if result["roi"] > 150:
    st.success(f"Alta rentabilidad. ROI: {result['roi']:.1f}%")
elif result["roi"] > 80:
    st.warning(f"Buena oportunidad. ROI: {result['roi']:.1f}%")
else:
    st.error(f"ROI bajo: {result['roi']:.1f}%")

# ----------------------
# RESUMEN
# ----------------------
st.markdown(f"""
## 📄 Resumen Ejecutivo

- 💰 Ahorro anual: **${result['ahorro_total']:,.0f}**
- 📈 ROI: **{result['roi']:.1f}%**
- ⏱ Payback: **{result['payback']:.1f} meses**
- 🕒 Horas liberadas: **{result['horas_ahorradas']:,.0f}**
""")

# ----------------------
# EXPORT
# ----------------------
df_export = pd.DataFrame([{
    "Costo Actual": result["costo_total"],
    "Ahorro Total": result["ahorro_total"],
    "ROI": result["roi"],
    "Payback": result["payback"],
    "Horas": result["horas_ahorradas"]
}])

st.download_button(
    "📄 Descargar CSV",
    df_export.to_csv(index=False),
    "roi.csv",
    "text/csv"
)
