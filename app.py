import streamlit as st
import pandas as pd
import os

# 🔴 Configuración de página
st.set_page_config(
    page_title="ROI Ansible",
    layout="wide"
)

# 🔴 Rutas robustas (PRO)
BASE_DIR = os.path.dirname(__file__)
logo_path = os.path.join(BASE_DIR, "assets", "redhat.png")
nexsys_path = os.path.join(BASE_DIR, "assets", "nexsys.png")

# 🔴 Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stMetric {
        background-color: #f2d6d6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .stMetric label {
        color: #800000;
        font-weight: bold;
    }
    .stMetric div {
        color: #000000;
        font-size: 22px;
    }
    h1, h2, h3 {
        color: #800000;
    }
    </style>
""", unsafe_allow_html=True)

# 🔴 HEADER con logo
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image(logo_path, width=120)

with col_title:
    st.title("💰 ROI Calculator - Ansible")

# 🔴 Sidebar con branding
st.sidebar.image(nexsys_path, use_column_width=True)
st.sidebar.markdown("## 🔴 Datos del Cliente")

# 🔴 Inputs
servidores = st.sidebar.number_input("Número de servidores", value=100)
admins = st.sidebar.number_input("Administradores", value=3)
salario = st.sidebar.number_input("Salario mensual ($)", value=2500)
horas_semana = st.sidebar.number_input("Horas semanales por admin", value=40)

porc_tareas = st.sidebar.slider("% tiempo en tareas manuales", 0, 100, 60)
reduccion = st.sidebar.slider("% automatización con Ansible", 0, 100, 90)

incidentes = st.sidebar.number_input("Incidentes mensuales", value=5)
costo_incidente = st.sidebar.number_input("Costo por incidente ($)", value=200)
reduccion_errores = st.sidebar.slider("% reducción de errores", 0, 100, 80)

costo_ansible = st.sidebar.number_input("Costo Ansible anual ($)", value=10000)

# 🔴 Cálculos
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

# 🔴 KPIs principales
col1, col2, col3 = st.columns(3)

col1.metric("💼 Costo actual anual", f"${costo_total_actual:,.0f}")
col2.metric("💸 Ahorro estimado", f"${ahorro_total:,.0f}")
col3.metric("📈 ROI (%)", f"{roi:,.1f}%")

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric("⏱️ Payback (meses)", f"{payback:,.1f}")
col5.metric("🕒 Horas ahorradas/año", f"{horas_ahorradas:,.0f}")
col6.metric("⚙️ Costo Ansible", f"${costo_ansible:,.0f}")

# 🔴 Gráfico
st.subheader("📊 Comparación de Costos")

data = pd.DataFrame({
    "Concepto": ["Costo Actual", "Costo con Ansible"],
    "Valor": [costo_total_actual, costo_total_actual - ahorro_total]
})

st.bar_chart(data.set_index("Concepto"))

# 🔴 Detalle de ahorro
st.subheader("🔍 Detalle de Ahorros")

col7, col8 = st.columns(2)
col7.metric("Ahorro por eficiencia", f"${ahorro_tiempo:,.0f}")
col8.metric("Ahorro por errores", f"${ahorro_errores:,.0f}")

# 🔴 Resultado ejecutivo
st.subheader("📢 Resultado Ejecutivo")

if roi > 150:
    st.markdown(f"### 🔴 Inversión altamente rentable (ROI {roi:.1f}%)")
elif roi > 80:
    st.markdown(f"### 🟠 Buena oportunidad de automatización (ROI {roi:.1f}%)")
else:
    st.markdown(f"### ⚫ ROI bajo ({roi:.1f}%) - revisar supuestos")

# 🔴 Resumen para cliente
st.markdown(
    f"""
    ---
    ### 📄 Resumen para Cliente

    Con Ansible, la organización puede ahorrar aproximadamente **${ahorro_total:,.0f} al año**,  
    logrando un **ROI de {roi:.1f}%** y recuperando la inversión en **{payback:.1f} meses**.
    """
)
