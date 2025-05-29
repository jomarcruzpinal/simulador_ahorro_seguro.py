
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def simular_ahorro(
    pago_total_periodo,
    porcentaje_ahorro,
    tasa_anual,
    pagos_anuales,
    anios
):
    aporte_periodo = pago_total_periodo * porcentaje_ahorro
    tasa_periodo = tasa_anual / pagos_anuales
    anios_list = list(range(1, anios + 1))
    aportaciones = []
    rendimientos = []
    pagos_totales = []

    valor_acumulado = 0
    aporte_total = 0

    for anio in anios_list:
        for _ in range(pagos_anuales):
            valor_acumulado = valor_acumulado * (1 + tasa_periodo) + aporte_periodo
            aporte_total += aporte_periodo
        aportaciones.append(round(aporte_total, 2))
        rendimientos.append(round(valor_acumulado - aporte_total, 2))
        pagos_totales.append(pago_total_periodo * pagos_anuales * anio)

    df = pd.DataFrame({
        "Año": anios_list,
        "Aportaciones acumuladas (MXN)": aportaciones,
        "Rendimientos generados (MXN)": rendimientos,
        "Valor acumulado (MXN)": [round(a + r, 2) for a, r in zip(aportaciones, rendimientos)],
        "Total pagado (MXN)": pagos_totales
    })

    return df

# Interfaz Streamlit
st.title("Simulador de Ahorro en Seguro por Nómina")

pago_total_periodo = st.number_input("Pago total por periodo (MXN):", min_value=100, value=1000, step=50)
porcentaje_ahorro = st.slider("Porcentaje destinado al ahorro:", 0.0, 1.0, 0.5, 0.05)
tasa_anual = st.number_input("Tasa anual de rendimiento (%):", min_value=0.0, value=7.0, step=0.1) / 100
pagos_anuales = st.selectbox("Pagos por año:", options=[12, 24, 26], index=1)
anios = st.slider("Plazo en años:", min_value=1, max_value=50, value=30)

if st.button("Simular"):
    df_resultado = simular_ahorro(pago_total_periodo, porcentaje_ahorro, tasa_anual, pagos_anuales, anios)
    st.dataframe(df_resultado)

    st.line_chart(df_resultado.set_index("Año")[[
        "Total pagado (MXN)",
        "Valor acumulado (MXN)",
        "Aportaciones acumuladas (MXN)"
    ]])
