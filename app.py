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

# ======================
# PARTE 5: CONCENTRADO PLOMO
# ======================
st.subheader("5. Concentrado Plomo")
col1, col2, col3, col4 = st.columns(4)
with col1:
    ley_cc_pb = 2.1464 * ley_pb + 60.0425
    st.metric("Ley CC Pb (%)", f"{ley_cc_pb:.4f}")
with col2:
    if ley_pb > 0:
        if ley_pb <= 0.15:
            rec_pb = 84.9 + 10.79 * math.log(ley_pb) - 1.75 * (ley_cu / ley_pb)
        elif ley_pb <= 0.5:
            rec_pb = 97.33 + 17.13 * math.log(ley_pb) - 1.95 * (ley_cu / ley_pb)
        else:
            rec_pb = 89.65 + 8.35 * math.log(ley_pb) - 0.4 * (ley_cu / ley_pb)
        rec_pb += 1
    else:
        rec_pb = 0
    st.metric("Recuperación Pb (%)", f"{rec_pb:.4f}")
with col3:
    rec_ag_pb = 24.1147 * ley_ag + 10.0657
    st.metric("Recuperación Ag en Pb (%)", f"{rec_ag_pb:.4f}")
with col4:
    ley_cc_ag_pb = ((tonelaje * ley_ag) * (rec_ag_pb / 100)) / (((tonelaje * ley_pb * rec_pb / 100) / ley_cc_pb)) if ley_cc_pb > 0 and rec_pb > 0 else 0
    st.metric("Ley CC Ag en Pb (oz/ton)", f"{ley_cc_ag_pb:.4f}")

st.metric("TMS Plomo", f"{((tonelaje * ley_pb) / 100) * ((rec_pb / 100) / (ley_cc_pb / 100)) if ley_cc_pb > 0 else 0:,.2f}")

# ======================
# PARTE 6: CONCENTRADO COBRE
# ======================
st.subheader("6. Concentrado Cobre")
col1, col2, col3, col4 = st.columns(4)
with col1:
    ley_cc_cu = 0.8739 * ley_cu + 25.3680
    st.metric("Ley CC Cu (%)", f"{ley_cc_cu:.4f}")
with col2:
    if ley_cu > 0:
        if ley_cu <= 0.4:
            rec_cu = 82.6 + 0.5 * math.log(ley_cu) - 5.61 * (ley_pb / ley_cu)
        elif ley_cu <= 0.8:
            rec_cu = 93.09 + 10.02 * math.log(ley_cu) - 5.21 * (ley_pb / ley_cu)
        else:
            rec_cu = 90.57 + 2.08 * math.log(ley_cu) - 0.43 * (ley_pb / ley_cu)
        rec_cu += 0.4
    else:
        rec_cu = 0
    st.metric("Recuperación Cu (%)", f"{rec_cu:.4f}")
with col3:
    rec_ag_cu = -12.8961 * ley_ag + 49.5286
    st.metric("Recuperación Ag en Cu (%)", f"{rec_ag_cu:.4f}")
with col4:
    ley_cc_ag_cu = ((tonelaje * ley_ag) * (rec_ag_cu / 100)) / (((tonelaje * ley_cu * rec_cu / 100) / ley_cc_cu)) if ley_cc_cu > 0 and rec_cu > 0 else 0
    st.metric("Ley CC Ag en Cu (oz/ton)", f"{ley_cc_ag_cu:.4f}")

st.metric("TMS Cobre", f"{((tonelaje * ley_cu) / 100) * ((rec_cu / 100) / (ley_cc_cu / 100)) if ley_cc_cu > 0 else 0:,.2f}")
