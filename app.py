import streamlit as st

st.title("ROI Calculator - Ansible")

servidores = st.number_input("Número de servidores", 1)
admins = st.number_input("Administradores", 1)
salario = st.number_input("Salario mensual", 500)
reduccion = st.slider("Reducción (%)", 0, 100, 70)

costo_anual = admins * salario * 12
ahorro = costo_anual * (reduccion/100)

st.metric("Costo anual", costo_anual)
st.metric("Ahorro estimado", ahorro)
