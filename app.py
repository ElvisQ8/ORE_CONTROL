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

coef = [14.73, 965, 789, 389.22, 11.35, 39.96, 40.92, 339, 1284, 240.15,
        0.36, 2.2, 1, 1, 1, 0]

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
            costos.append(0)
            st.write("Calculado abajo")
        else:
            resultado = metrajes[i] * coef[i]
            costos.append(resultado)
            st.write(f"{resultado:,.2f}")

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

# ======================
# PARTE 4: CONCENTRADO ZINC
# ======================
st.subheader("4. Concentrado Zinc")
ley_cc_zn = -0.4184 * ley_zn + 57.0910
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
rec_zn_dup = 1.8645 * ley_ag + 3.2175
tms_zn = ((tonelaje * ley_zn) / 100) * ((rec_zn / 100) / (ley_cc_zn / 100)) if ley_cc_zn > 0 else 0

# ======================
# PARTE 5: CONCENTRADO PLOMO
# ======================
st.subheader("5. Concentrado Plomo")
ley_cc_pb = 2.1464 * ley_pb + 60.0425
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
rec_ag_pb = 24.1147 * ley_ag + 10.0657
ley_cc_ag_pb = ((tonelaje * ley_ag) * (rec_ag_pb / 100)) / (((tonelaje * ley_pb * rec_pb / 100) / ley_cc_pb)) if ley_cc_pb > 0 and rec_pb > 0 else 0
tms_pb = ((tonelaje * ley_pb) / 100) * ((rec_pb / 100) / (ley_cc_pb / 100)) if ley_cc_pb > 0 else 0

# ======================
# PARTE 6: CONCENTRADO COBRE
# ======================
st.subheader("6. Concentrado Cobre")
ley_cc_cu = 0.8739 * ley_cu + 25.3680
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
rec_ag_cu = -12.8961 * ley_ag + 49.5286
ley_cc_ag_cu = ((tonelaje * ley_ag) * (rec_ag_cu / 100)) / (((tonelaje * ley_cu * rec_cu / 100) / ley_cc_cu)) if ley_cc_cu > 0 and rec_cu > 0 else 0
tms_cu = ((tonelaje * ley_cu) / 100) * ((rec_cu / 100) / (ley_cc_cu / 100)) if ley_cc_cu > 0 else 0

# ======================
# PARTE 7: TOTALES Y FINOS
# ======================
st.subheader("7. Totales y Finos")
total_concentrado = tms_zn + tms_pb + tms_cu
finos_zn = tms_zn * (ley_cc_zn / 100)
finos_pb = tms_pb * (ley_cc_pb / 100)
finos_cu = tms_cu * (ley_cc_cu / 100)
finos_ag = (
    tonelaje * ley_ag * (rec_zn_dup / 100) +
    tonelaje * ley_ag * (rec_ag_pb / 100) +
    tonelaje * ley_ag * (rec_ag_cu / 100)
)
zn_eq = finos_zn + finos_pb * (2137 / 2649) + finos_cu * (8483 / 2649) + finos_ag * (23 / 2649)
sr = ley_zn + 1 + 29.93278969711

# =============================
# PARTE 8: COSTO Y PRODUCCIÓN
# =============================
st.subheader("8. Costo y Producción General")
costo_var_mina_tm = (total_costos_mina + costos[-1]) / tonelaje if tonelaje > 0 else 0
costo_var_planta_ga = (planta + ga) * tonelaje
produccion_tmd = tonelaje
precio_zn_eq = 2546
dias = 1

# =============================
# PARTE 9: PROGRAMA - 1ERA SEMANA
# =============================
st.subheader("9. Programa - 1era Semana")
st.write(f"**NSR ($/ton):** {sr:,.2f}")
st.write(f"**Zn Equivalente (TMS):** {zn_eq:,.2f}")

# =============================
# PARTE 10: MC1 – Margen de Contribución
# =============================
st.subheader("10. MC1 – Margen de Contribución")
venta = precio_zn_eq * zn_eq
costo_var_mina_total = costo_var_mina_tm * tonelaje
mc = venta - costo_var_mina_total
st.write(f"**VENTA (US$):** {venta:,.2f}")
st.write(f"**CV Mina (US$):** {costo_var_mina_total:,.2f}")
st.write(f"**MC (Miles de US$):** {mc / 1000:,.2f}")

# =============================
# PARTE 11: UTILIDAD FINAL
# =============================
st.subheader("11. Utilidad Final")
utilidad = mc - costo_var_planta_ga
st.write(f"**UTILIDAD (US$):** {utilidad:,.2f}")
