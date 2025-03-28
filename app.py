import streamlit as st
import math

st.set_page_config(page_title="Proyecto Minero", layout="wide")
st.title("🧱 Proyecto de Cálculo Minero")
st.markdown("---")

# =======================
# PARTE 1: COSTOS SOPORTE
# =======================
st.subheader("1. Costos Variables Áreas Soporte")
planta = st.number_input("PLANTA ($/ton)", min_value=0.0, format="%.2f")
ga = st.number_input("G&A ($/ton)", min_value=0.0, format="%.2f")

# ======================
# PARTE 2: COSTOS MINA
# ======================
st.subheader("2. Costos Variables Mina")
costos_mina = []
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    st.markdown("**Actividad**")
    actividades = [
        "CABLE BOLTING ($)", "AVANCES PREPARACIONES ($)", "AVANCES EN RELLENO ($)",
        "REFUGIOS OPEX ($)", "SOSTENIMIENTO CON MALLA ($)", "PERNOS HELICOIDALES ($)",
        "PERNOS EXPANSIVOS ($)", "REHABILITACIONES ($)", "CHIMENEA SLOT ($)",
        "SHOTCRETE ($)", "VOLADURA TAJOS ($)", "TRANSPORTE ($)",
        "ACEROS ($)", "Cemento y Otros ($)", "Servicios Mina ($)", "Transporte CC ($)"
    ]
    for act in actividades:
        st.text(act)

# Coeficientes por actividad
coef = [14.73, 965, 789, 389.22, 11.35, 39.96, 40.92, 339, 1284, 240.15,
        0.36, 2.2, 1, 1, 1, 0]  # Transporte CC se calcula aparte

metrajes = []
costos = []

with col2:
    st.markdown("**Metraje (input)**")
    for i in range(len(actividades)):
        val = st.number_input(f"", key=f"metraje_{i}", min_value=0.0)
        metrajes.append(val)

with col3:
    st.markdown("**Costo ($)**")
    for i in range(len(actividades)):
        if actividades[i] == "Transporte CC ($)":
            costos.append(0)  # temporal, se calculará después
            st.write("Calculado abajo")
        else:
            resultado = metrajes[i] * coef[i]
            costos.append(resultado)
            st.write(f"{resultado:,.2f}")

# Suma total de costos (excepto Transporte CC)
total_costos_mina = sum(costos[:-1])

# ======================
# PARTE 3: TAJO 1
# ======================
st.subheader("3. TAJO 1 – Parámetros de Cabeza")
tonelaje = st.number_input("Tonelaje (TMS)", min_value=0.0, format="%.2f")
ley_zn = st.number_input("Ley Cabeza Zn (%)", min_value=0.0, format="%.4f")
ley_pb = st.number_input("Ley Cabeza Pb (%)", min_value=0.0, format="%.4f")
ley_cu = st.number_input("Ley Cabeza Cu (%)", min_value=0.0, format="%.4f")
ley_ag = st.number_input("Ley Cabeza Ag (oz/ton)", min_value=0.0, format="%.4f")

st.markdown("---")
st.subheader("🔽 En la siguiente etapa se mostrarán los resultados estadísticos y visualizaciones.")
