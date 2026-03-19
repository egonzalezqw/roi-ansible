import streamlit as st

st.set_page_config(page_title="ROI Ansible", layout="wide")

st.title("💰 ROI Calculator - Ansible (Red Hat Model)")

# 🔹 Sidebar Inputs
st.sidebar.header("📊 Datos del Cliente")

servidores = st.sidebar.number_input("Número de servidores", value=50)
admins = st.sidebar.number_input("Administradores", value=3)
salario = st.sidebar.number_input("Salario mensual ($)", value=2500)
horas_semana = st.sidebar.number_input("Horas semanales por admin", value=40)

porc_tareas = st.sidebar.slider("% tiempo en tareas manuales", 0, 100, 60)
reduccion = st.sidebar.slider("% reducción con Ansible", 0, 100, 70)

incidentes = st.sidebar.number_input("Incidentes mensuales", value=5)
costo_incidente = st.sidebar.number_input("Costo por incidente ($)", value=200)
reduccion_errores = st.sidebar.slider("% reducción errores", 0, 100, 80)

costo_ansible = st.sidebar.number_input("Costo anual Ansible ($)", value=15000)

# 🔹 Cálculos base
horas_anuales = horas_semana * 52
costo_anual_personal = admins * salario * 12

# 💡 Costo por hora (clave en modelo Red Hat)
costo_hora = costo_anual_personal / (admins * horas_anuales)

# 🔹 Tiempo desperdiciado (antes)
horas_manual = horas_anuales * admins * (porc_tareas / 100)
costo_manual = horas_manual * costo_hora

# 🔹 Con Ansible
horas_ahorradas = horas_manual * (reduccion / 100)
ahorro_tiempo = horas_ahorradas * costo_hora

# 🔹 Errores
costo_errores_actual = incidentes * costo_incidente * 12
ahorro_errores = costo_errores_actual * (reduccion_errores / 100)

# 🔹 Totales
ahorro_total = ahorro_tiempo + ahorro_errores
costo_total_actual = costo_anual_personal + costo_errores_actual

roi = ((ahorro_total - costo_ansible) / costo_ansible) * 100 if costo_ansible > 0 else 0
payback = (costo_ansible / ahorro_total) * 12 if ahorro_total > 0 else 0

# 🔹 Layout KPIs
col1, col2, col3 = st.columns(3)

col1.metric("💼 Costo actual anual", f"${costo_total_actual:,.0f}")
col2.metric("💸 Ahorro total estimado", f"${ahorro_total:,.0f}")
col3.metric("📈 ROI (%)", f"{roi:,.1f}%")

st.divider()

col4, col5, col6 = st.columns(3)

col4.metric("⏱️ Payback (meses)", f"{payback:,.1f}")
col5.metric("🕒 Horas ahorradas/año", f"{horas_ahorradas:,.0f}")
col6.metric("⚙️ Costo Ansible", f"${costo_ansible:,.0f}")

# 🔹 Gráfico comparativo
st.subheader("📊 Comparación de Costos")

st.bar_chart({
    "Costo Actual": [costo_total_actual],
    "Costo con Ansible": [costo_total_actual - ahorro_total]
})

# 🔹 Breakdown
st.subheader("🔍 Detalle de Ahorros")

col7, col8 = st.columns(2)
col7.metric("Ahorro por eficiencia", f"${ahorro_tiempo:,.0f}")
col8.metric("Ahorro por reducción de errores", f"${ahorro_errores:,.0f}")

# 🔹 Mensaje comercial
st.subheader("📢 Resultado Ejecutivo")

if roi > 150:
    st.success(f"🚀 Inversión altamente rentable (ROI {roi:.1f}%)")
elif roi > 80:
    st.warning(f"👍 Buena oportunidad de automatización (ROI {roi:.1f}%)")
else:
    st.error(f"⚠️ ROI bajo ({roi:.1f}%) - ajustar supuestos")

# 🔹 Mensaje listo para cliente
st.info(
    f"Con Ansible, el cliente puede ahorrar aproximadamente ${ahorro_total:,.0f} al año, "
    f"recuperando la inversión en {payback:,.1f} meses."
)
