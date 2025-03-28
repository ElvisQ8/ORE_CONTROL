import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Proyecto Minero", layout="wide")

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

    # PARTE 4 al 11 (Resumen)
    st.subheader("4–11. Cálculos Automáticos")
    st.markdown("ℹ️ Los cálculos desde el concentrado hasta utilidad se realizarán automáticamente y pueden verse en las próximas versiones del panel.")

else:
    st.title("📊 Seguimiento de Tajo")
    st.markdown("---")
    st.subheader("Editar valores obtenidos del cálculo previo")
    data = {
        "Finos de Zinc (TMS)": [0],
        "Finos de Plomo (TMS)": [0],
        "Finos de Cobre (TMS)": [0],
        "Finos de Plata (Oz)": [0],
        "Zn Equivalente (TMS)": [0],
        "Ley Cabeza Zn (%)": [0],
        "Ley Cabeza Pb (%)": [0],
        "Ley Cabeza Cu (%)": [0],
        "Ley Cabeza Ag (oz/ton)": [0]
    }
    editable_df = st.data_editor(pd.DataFrame(data), num_rows="dynamic", use_container_width=True)
    st.markdown("⚙️ Aquí podrás modificar los datos para hacer simulaciones y control del Tajo.")
