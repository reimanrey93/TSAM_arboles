import streamlit as st
import pandas as pd
from decision_tree import (
    construir_arbol_binario, construir_arbol_id3, construir_arbol_binario_categorico,
    construir_arbol_binario_numerico, visualizar_arbol, extraer_reglas
)

def main():
    st.title("Construcción de Árbol de Decisión desde Cero")
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

    if archivo is not None:
        data = pd.read_csv(archivo)
        st.dataframe(data)
        st.write(f"Cantidad total de tuplas importadas: {data.shape[0]}")

        atributos = list(data.columns)
        atributo_clase = st.selectbox("Selecciona el atributo de clase", atributos)
        atributos.remove(atributo_clase)

        # Selección del tipo de árbol
        tipo_arbol = st.selectbox(
            "Selecciona el tipo de árbol",
            ["ID3 Clásico", "ID3 Adaptado para Atributos Numéricos", "ID3 Clásico Binario para Datos Categóricos", "ID3 Binario para Datos Numéricos"]
        )

        # Selección del criterio de impureza
        criterio = st.selectbox("Selecciona el criterio de impureza", ["entropía", "índice Gini"])

        if st.button("Construir Árbol de Decisión"):
            if tipo_arbol == "ID3 Clásico":
                arbol = construir_arbol_id3(data, atributos, atributo_clase)
            elif tipo_arbol == "ID3 Adaptado para Atributos Numéricos":
                arbol = construir_arbol_binario(data, atributos, atributo_clase)
            elif tipo_arbol == "ID3 Clásico Binario para Datos Categóricos":
                arbol = construir_arbol_binario_categorico(data, atributos, atributo_clase, criterio)
            else:
                arbol = construir_arbol_binario_numerico(data, atributos, atributo_clase, criterio)

            st.write("Árbol de Decisión (Diccionario):", arbol)

            # Visualización como gráfico de árbol
            grafo = visualizar_arbol(arbol)
            st.graphviz_chart(grafo.source)

            # Mostrar las reglas del árbol
            reglas = extraer_reglas(arbol)
            st.write("Reglas de Decisión:")
            for regla in reglas:
                st.write(regla)

if __name__ == "__main__":
    main()
