import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Proyecto Minero", layout="wide")

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
    st.title("🧱 Proyecto de Cálculo Minero")
    st.markdown("---")

    # PARTE 1
    st.subheader("1. Costos Variables Áreas Soporte")
    col1, col2 = st.columns(2)
    with col1:
        planta = st.number_input("PLANTA ($/ton)", min_value=0.0, format="%.2f")
    with col2:
        ga = st.number_input("G&A ($/ton)", min_value=0.0, format="%.2f")

    # PARTE 2
    st.subheader("2. Costos Variables Mina")
    actividades = [
        "CABLE BOLTING ($)", "AVANCES PREPARACIONES ($)", "AVANCES EN RELLENO ($)",
        "REFUGIOS OPEX ($)", "SOSTENIMIENTO CON MALLA ($)", "PERNOS HELICOIDALES ($)",
        "PERNOS EXPANSIVOS ($)", "REHABILITACIONES ($)", "CHIMENEA SLOT ($)",
        "SHOTCRETE ($)", "VOLADURA TAJOS ($)", "TRANSPORTE ($)",
        "ACEROS ($)", "Cemento y Otros ($)", "Servicios Mina ($)", "Transporte CC ($)"
    ]
    coef = [14.73, 965, 789, 389.22, 11.35, 39.96, 40.92, 339, 1284, 240.15, 0.36, 2.2, 1, 1, 1, 0]
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

    # PARTE 3
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

    # PARTE 7 – Finos y Equivalentes
    rec_zn = 1
    rec_pb = 1
    rec_cu = 1
    rec_zn_dup = 1.8645 * ley_ag + 3.2175
    rec_ag_pb = 24.1147 * ley_ag + 10.0657
    rec_ag_cu = -12.8961 * ley_ag + 49.5286
    ley_cc_zn = -0.4184 * ley_zn + 57.0910
    ley_cc_pb = 2.1464 * ley_pb + 60.0425
    ley_cc_cu = 0.8739 * ley_cu + 25.3680

    tms_zn = ((tonelaje * ley_zn) / 100) * ((rec_zn / 100) / (ley_cc_zn / 100)) if ley_cc_zn > 0 else 0
    tms_pb = ((tonelaje * ley_pb) / 100) * ((rec_pb / 100) / (ley_cc_pb / 100)) if ley_cc_pb > 0 else 0
    tms_cu = ((tonelaje * ley_cu) / 100) * ((rec_cu / 100) / (ley_cc_cu / 100)) if ley_cc_cu > 0 else 0

    finos_zn = tms_zn * (ley_cc_zn / 100)
    finos_pb = tms_pb * (ley_cc_pb / 100)
    finos_cu = tms_cu * (ley_cc_cu / 100)
    finos_ag = (
        tonelaje * ley_ag * (rec_zn_dup / 100) +
        tonelaje * ley_ag * (rec_ag_pb / 100) +
        tonelaje * ley_ag * (rec_ag_cu / 100)
    )
    zn_eq = finos_zn + finos_pb * (2137 / 2649) + finos_cu * (8483 / 2649) + finos_ag * (23 / 2649)

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

    st.success("✅ Resultados guardados y disponibles para la otra vista.")

else:
    st.title("📊 Seguimiento de Tajo")
    st.markdown("---")
    st.subheader("Editar valores obtenidos del cálculo previo")

    editable_df = st.data_editor(
        pd.DataFrame([st.session_state.resultados]),
        num_rows="dynamic",
        use_container_width=True
    )
    st.markdown("⚙️ Aquí podrás modificar los datos para hacer simulaciones y control del Tajo.")
