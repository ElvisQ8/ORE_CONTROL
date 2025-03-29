import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Ore Control", layout="wide")

# Inicialización de variables globales
if "resultados" not in st.session_state:
    st.session_state.resultados = {
        "Finos de Zinc (TMS)": 0,
        "Finos de Plomo (TMS)": 0,
        "Finos de Cobre (TMS)": 0,
        "Finos de Plata (Oz)": 0,
        "Zn Equivalente (TMS)": 0,
        "Ley Cabeza Zn (%)": 0,
        "Ley Cabeza Pb (%)": 0,
        "Ley Cabeza Cu (%)": 0,
        "Ley Cabeza Ag (oz/ton)": 0
    }

menu = st.sidebar.selectbox("Selecciona una vista", ["Costo de Producción", "Seguimiento de Tajo"])

if menu == "Costo de Producción":
    st.title("🧱 Calculo de valor por tajo")
    st.markdown("---")

    # PARTE 1: SOPORTE
    st.subheader("1. Costos Variables Áreas Soporte")
    col1, col2 = st.columns(2)
    with col1:
        planta = st.number_input("PLANTA ($/ton)", min_value=0.0, format="%.2f")
    with col2:
        ga = st.number_input("G&A ($/ton)", min_value=0.0, format="%.2f")

    # PARTE 2: COSTOS MINA
    st.subheader("2. Costos Variables Mina")
    actividades = [
        "CABLE BOLTING ($)", "AVANCES PREPARACIONES ($)", "AVANCES EN RELLENO ($)",
        "REFUGIOS OPEX ($)", "SOSTENIMIENTO CON MALLA ($)", "PERNOS HELICOIDALES ($)",
        "PERNOS EXPANSIVOS ($)", "REHABILITACIONES ($)", "CHIMENEA SLOT ($)",
        "SHOTCRETE ($)", "VOLADURA TAJOS ($)", "TRANSPORTE ($)",
        "ACEROS ($)", "Cemento y Otros ($)", "Servicios Mina ($)", "Transporte CC ($)"
    ]
    coef = [14.73, 965, 789, 389.22, 11.35, 39.96, 40.92, 339, 1284,
            240.15, 0.36, 2.2, 1, 1, 1, 0]
    metrajes, costos = [], []
    cols = st.columns(3)
    for idx, actividad in enumerate(actividades):
        with cols[idx % 3]:
            st.markdown(f"**{actividad}**")
            val = st.number_input(f"Metraje - {actividad}", key=f"metraje_{idx}", min_value=0.0)
            metrajes.append(val)
            if actividad == "Transporte CC ($)":
                st.info("Se calcula más adelante")
                costos.append(0)
            else:
                resultado = val * coef[idx]
                costos.append(resultado)
                st.write(f"Costo: ${resultado:,.2f}")

    # PARTE 3: TAJO 1
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

    # PARTE 4: CONCENTRADO ZINC
    st.subheader("4. Concentrado Zinc")
    ley_cc_zn = -0.4184 * ley_zn + 57.0910
    rec_zn = 88.38 + 4.28 * math.log(ley_zn) - 13.16 * (ley_cu / ley_zn) if ley_zn > 0 else 0
    rec_zn += 1
    rec_zn_dup = 1.8645 * ley_ag + 3.2175
    tms_zn = ((tonelaje * ley_zn) / 100) * ((rec_zn / 100) / (ley_cc_zn / 100)) if ley_cc_zn > 0 else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ley CC Zn (%)", f"{ley_cc_zn:.2f}")
        st.metric("Recuperación Zn (%)", f"{rec_zn:.2f}")
    with col2:
        st.metric("Recuperación Zn duplicado (%)", f"{rec_zn_dup:.2f}")
    with col3:
        st.metric("TMS Zinc", f"{tms_zn:.2f}")

    # PARTE 5: CONCENTRADO PLOMO
    st.subheader("5. Concentrado Plomo")
    ley_cc_pb = 2.1464 * ley_pb + 60.0425
    rec_pb = 84.9 + 10.79 * math.log(ley_pb) - 1.75 * (ley_cu / ley_pb) if ley_pb > 0 else 0
    rec_pb += 1
    rec_ag_pb = 24.1147 * ley_ag + 10.0657
    tms_pb = ((tonelaje * ley_pb) / 100) * ((rec_pb / 100) / (ley_cc_pb / 100)) if ley_cc_pb > 0 else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ley CC Pb (%)", f"{ley_cc_pb:.2f}")
        st.metric("Recuperación Pb (%)", f"{rec_pb:.2f}")
    with col2:
        st.metric("Recuperación Ag en Pb (%)", f"{rec_ag_pb:.2f}")
    with col3:
        st.metric("TMS Plomo", f"{tms_pb:.2f}")
   
    # PARTE 6: CONCENTRADO COBRE
    st.subheader("6. Concentrado Cobre")
    ley_cc_cu = 0.8739 * ley_cu + 25.3680
    rec_cu = 82.6 + 0.5 * math.log(ley_cu) - 5.61 * (ley_pb / ley_cu) if ley_cu > 0 else 0
    rec_cu += 0.4
    rec_ag_cu = -12.8961 * ley_ag + 49.5286
    tms_cu = ((tonelaje * ley_cu) / 100) * ((rec_cu / 100) / (ley_cc_cu / 100)) if ley_cc_cu > 0 else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ley CC Cu (%)", f"{ley_cc_cu:.2f}")
        st.metric("Recuperación Cu (%)", f"{rec_cu:.2f}")
    with col2:
        st.metric("Recuperación Ag en Cu (%)", f"{rec_ag_cu:.2f}")
    with col3:
        st.metric("TMS Cobre", f"{tms_cu:.2f}")

    # PARTE 7: TOTALES Y FINOS
    st.subheader("7. Totales y Finos")
    finos_zn = tms_zn * (ley_cc_zn / 100)
    finos_pb = tms_pb * (ley_cc_pb / 100)
    finos_cu = tms_cu * (ley_cc_cu / 100)
    finos_ag = (tonelaje * ley_ag * (rec_zn_dup / 100) + tonelaje * ley_ag * (rec_ag_pb / 100) + tonelaje * ley_ag * (rec_ag_cu / 100))
    zn_eq = finos_zn + finos_pb * (2137 / 2649) + finos_cu * (8483 / 2649) + finos_ag * (23 / 2649)
    sr = ley_zn + 1 + 29.93278969711

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Finos de Zinc (TMS)", f"{finos_zn:.2f}")
        st.metric("Finos de Plomo (TMS)", f"{finos_pb:.2f}")
    with col2:
        st.metric("Finos de Cobre (TMS)", f"{finos_cu:.2f}")
        st.metric("Finos de Plata (Oz)", f"{finos_ag:.2f}")
    with col3:
        st.metric("Zn Equivalente (TMS)", f"{zn_eq:.2f}")
        st.metric("NSR ($/ton)", f"{sr:.2f}")

    # PARTE 8: COSTO Y PRODUCCIÓN
    st.subheader("8. Costo y Producción")
    
    # Primero calcula los valores
    costo_var_mina_tm = sum(costos) / tonelaje if tonelaje > 0 else 0
    costo_var_planta_ga = (planta + ga) * tonelaje
    precio_zn_eq = 2546
    
    # Luego muestra los resultados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Costo Variable Mina (US$/TM)", f"{costo_var_mina_tm:.2f}")
    with col2:
        st.metric("Costo Variable Planta - G&A (US$)", f"{costo_var_planta_ga:.2f}")
    with col3:
    st.metric("Precio $ (T/Zn eq)", f"{precio_zn_eq:.2f}")

    # PARTE 9: PROGRAMA - 1ERA SEMANA
    st.subheader("9. Programa - 1era Semana")
    st.metric("NSR ($/ton)", f"{sr:.2f}")
    st.metric("Zn-Eq (TMS)", f"{zn_eq:.2f}")

    # PARTE 10: MC1
    st.subheader("10. MC1")
    venta = precio_zn_eq * zn_eq
    cv_mina_total = costo_var_mina_tm * tonelaje
    mc = venta - cv_mina_total
    st.metric("VENTA (US$)", f"{venta:,.2f}")
    st.metric("CV Mina (US$)", f"{cv_mina_total:,.2f}")
    st.metric("MC (Miles de US$)", f"{mc / 1000:,.2f}")

    # PARTE 11: UTILIDAD
    st.subheader("11. Utilidad")
    utilidad = mc - costo_var_planta_ga
    st.metric("UTILIDAD (US$)", f"{utilidad:,.2f}")

    # Guardar para seguimiento
    st.session_state.resultados = {
        "Finos de Zinc (TMS)": round(finos_zn, 2),
        "Finos de Plomo (TMS)": round(finos_pb, 2),
        "Finos de Cobre (TMS)": round(finos_cu, 2),
        "Finos de Plata (Oz)": round(finos_ag, 2),
        "Zn Equivalente (TMS)": round(zn_eq, 2),
        "Ley Cabeza Zn (%)": ley_zn,
        "Ley Cabeza Pb (%)": ley_pb,
        "Ley Cabeza Cu (%)": ley_cu,
        "Ley Cabeza Ag (oz/ton)": ley_ag
    }

else:
    st.title("📊 Seguimiento de Tajo")
    st.markdown("---")
    st.subheader("Editar valores obtenidos del cálculo previo")

    editable_df = st.data_editor(
        pd.DataFrame([st.session_state.resultados]),
        num_rows="dynamic",
        use_container_width=True
    )
    st.markdown("⚙️ En proceso para simulacion de tajos.")
