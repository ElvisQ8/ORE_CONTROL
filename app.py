import streamlit as st
import math

st.set_page_config(page_title="Proyecto Minero", layout="wide")
st.title("🧱 Proyecto de Cálculo Minero")
st.markdown("---")

# =======================
# PARTE 1: COSTOS SOPORTE
# =======================
st.subheader("1. Costos Variables Áreas Soporte")
col1, col2 = st.columns(2)
with col1:
    planta = st.number_input("PLANTA ($/ton)", min_value=0.0, format="%.2f")
with col2:
    ga = st.number_input("G&A ($/ton)", min_value=0.0, format="%.2f")

# ======================
# PARTE 2: COSTOS MINA
# ======================
st.subheader("2. Costos Variables Mina")
costos_mina = []
actividades = [
    "CABLE BOLTING ($)", "AVANCES PREPARACIONES ($)", "AVANCES EN RELLENO ($)",
    "REFUGIOS OPEX ($)", "SOSTENIMIENTO CON MALLA ($)", "PERNOS HELICOIDALES ($)",
    "PERNOS EXPANSIVOS ($)", "REHABILITACIONES ($)", "CHIMENEA SLOT ($)",
    "SHOTCRETE ($)", "VOLADURA TAJOS ($)", "TRANSPORTE ($)",
    "ACEROS ($)", "Cemento y Otros ($)", "Servicios Mina ($)", "Transporte CC ($)"
]

coef = [14.73, 965, 789, 389.22, 11.35, 39.96, 40.92, 339, 1284, 240.15,
        0.36, 2.2, 1, 1, 1, 0]

metrajes = []
costos = []

cols = st.columns(3)
for idx, actividad in enumerate(actividades):
    with cols[idx % 3]:
        st.markdown(f"**{actividad}**")
        input_val = st.number_input(f"Metraje - {actividad}", key=f"metraje_{idx}", min_value=0.0)
        metrajes.append(input_val)
        if actividad == "Transporte CC ($)":
            st.info("Se calcula más adelante con base en concentrados")
            costos.append(0)
        else:
            resultado = input_val * coef[idx]
            costos.append(resultado)
            st.write(f"Costo: ${resultado:,.2f}")

# ======================
# PARTE 3: TAJO 1
# ======================
st.subheader("3. TAJO 1 – Parámetros de Cabeza")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    tonelaje = st.number_input("Tonelaje (TMS)", min_value=0.0, format="%.2f")
with col2:
    ley_zn = st.number_input("Ley Cabeza Zn (%)", min_value=0.0, format="%.4f")
with col3:
    ley_pb = st.number_input("Ley Cabeza Pb (%)", min_value=0.0, format="%.4f")
with col4:
    ley_cu = st.number_input("Ley Cabeza Cu (%)", min_value=0.0, format="%.4f")
with col5:
    ley_ag = st.number_input("Ley Cabeza Ag (oz/ton)", min_value=0.0, format="%.4f")

# ======================
# PARTE 4: CONCENTRADO ZINC
# ======================
st.subheader("4. Concentrado Zinc")
col1, col2, col3, col4 = st.columns(4)
with col1:
    ley_cc_zn = -0.4184 * ley_zn + 57.0910
    st.metric("Ley CC Zn (%)", f"{ley_cc_zn:.4f}")
with col2:
    if ley_zn > 0:
        if ley_zn <= 0.75:
            rec_zn = 88.38 + 4.28 * math.log(ley_zn) - 13.16 * (ley_cu / ley_zn)
        elif ley_zn <= 2.25:
            rec_zn = 89.95 + 4.4 * math.log(ley_zn) - 12.88 * (ley_cu / ley_zn)
        else:
            rec_zn = 92.59 + 1.51 * math.log(ley_zn) - 10.28 * (ley_cu / ley_zn)
        rec_zn += 1
    else:
        rec_zn = 0
    st.metric("Recuperación Zn (%)", f"{rec_zn:.4f}")
with col3:
    rec_zn_dup = 1.8645 * ley_ag + 3.2175
    st.metric("Recuperación Zn duplicado (%)", f"{rec_zn_dup:.4f}")
with col4:
    tms_zn = ((tonelaje * ley_zn) / 100) * ((rec_zn / 100) / (ley_cc_zn / 100)) if ley_cc_zn > 0 else 0
    st.metric("TMS Zinc", f"{tms_zn:,.2f}")
