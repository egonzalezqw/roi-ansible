import streamlit as st

st.set_page_config(page_title="ROI Ansible", layout="wide")

st.title("💰 ROI Calculator - Ansible")

# 🔹 Inputs
st.sidebar.header("Datos del Cliente")

servidores = st.sidebar.number_input("Número de servidores", value=50)
admins = st.sidebar.number_input("Administradores", value=3)
salario = st.sidebar.number_input("Salario mensual ($)", value=2500)
horas = st.sidebar.number_input("Horas semanales", value=40)

reduccion = st.sidebar.slider("Reducción de esfuerzo (%)", 0, 100, 70)
incidentes = st.sidebar.number_input("Incidentes mensuales", value=5)
costo_incidente = st.sidebar.number_input("Costo por incidente ($)", value=200)
costo_ansible = st.sidebar.number_input("Costo anual Ansible ($)", value=15000)

# 🔹 Cálculos
costo_anual = admins * salario * 12
costo_errores = incidentes * costo_incidente * 12
costo_total = costo_anual + costo_errores

ahorro = costo_total * (reduccion / 100)
roi = ((ahorro - costo_ansible) / costo_ansible) * 100
payback = (costo_ansible / ahorro) * 12 if ahorro > 0 else 0

# 🔹 Layout
col1, col2, col3 = st.columns(3)

col1.metric("💼 Costo actual anual", f"${costo_total:,.0f}")
col2.metric("💸 Ahorro estimado", f"${ahorro:,.0f}")
col3.metric("📈 ROI (%)", f"{roi:,.1f}%")

st.divider()

col4, col5 = st.columns(2)

col4.metric("⏱️ Payback (meses)", f"{payback:,.1f}")
col5.metric("⚙️ Costo Ansible", f"${costo_ansible:,.0f}")

# 🔹 Gráfico simple
st.subheader("📊 Comparación de Costos")

st.bar_chart({
    "Costo Actual": [costo_total],
    "Costo con Ansible": [costo_total - ahorro]
})

# 🔹 Mensaje automático de ventas
st.subheader("📢 Resultado")

if roi > 100:
    st.success(f"Excelente inversión: ROI de {roi:.1f}%")
elif roi > 50:
    st.warning(f"Buena oportunidad: ROI de {roi:.1f}%")
else:
    st.error(f"ROI bajo: {roi:.1f}% - revisar supuestos")
