import numpy as np
import pandas as pd

def calcular_indice_gini(data, atributo_clase):
    valores, conteos = np.unique(data[atributo_clase], return_counts=True)
    gini = 1 - sum((count / np.sum(conteos))**2 for count in conteos)
    return gini

# Calcular entropía
def calcular_entropia(data, atributo_clase):
    valores, conteos = np.unique(data[atributo_clase], return_counts=True)
    entropia = 0
    for count in conteos:
        probabilidad = count / np.sum(conteos)
        entropia -= probabilidad * np.log2(probabilidad)
    return entropia

def ganancia_informacion(data, atributo, atributo_clase, criterio="entropia"):
    if criterio == "entropia":
        total_impureza = calcular_entropia(data, atributo_clase)
    else:
        total_impureza = calcular_indice_gini(data, atributo_clase)
    
    valores, conteos = np.unique(data[atributo], return_counts=True)
    impureza_parcial = 0
    for i in range(len(valores)):
        subset_data = data[data[atributo] == valores[i]]
        probabilidad = conteos[i] / np.sum(conteos)
        if criterio == "entropia":
            impureza = calcular_entropia(subset_data, atributo_clase)
        else:
            impureza = calcular_indice_gini(subset_data, atributo_clase)
        impureza_parcial += probabilidad * impureza
    
    return total_impureza - impureza_parcial


# Seleccionar mejor umbral de división para un atributo numérico
def mejor_umbral(data, atributo, atributo_clase):
    valores_unicos = np.unique(data[atributo])
    mejor_ganancia = -1
    mejor_threshold = None

    for threshold in valores_unicos:
        data_izq = data[data[atributo] <= threshold]
        data_der = data[data[atributo] > threshold]

        if len(data_izq) == 0 or len(data_der) == 0:
            continue

        entropia_izq = calcular_entropia(data_izq, atributo_clase)
        entropia_der = calcular_entropia(data_der, atributo_clase)
        peso_izq = len(data_izq) / len(data)
        peso_der = len(data_der) / len(data)

        ganancia = calcular_entropia(data, atributo_clase) - (peso_izq * entropia_izq + peso_der * entropia_der)

        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_threshold = threshold

    return mejor_threshold, mejor_ganancia

# Construcción del árbol binario
def construir_arbol_binario(data, atributos, atributo_clase):
    clases_unicas = np.unique(data[atributo_clase])
    if len(clases_unicas) == 1:
        return clases_unicas[0]

    mejor_atributo = None
    mejor_ganancia = -1
    mejor_threshold = None
    es_numerico = False

    for atributo in atributos:
        if data[atributo].dtype in [np.int64, np.float64]:  # Atributo numérico
            threshold, ganancia = mejor_umbral(data, atributo, atributo_clase)
            if ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_atributo = atributo
                mejor_threshold = threshold
                es_numerico = True
        else:  # Atributo categórico
            ganancia = ganancia_informacion(data, atributo, atributo_clase)
            if ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_atributo = atributo
                es_numerico = False

    if es_numerico:
        arbol = {f"{mejor_atributo} <= {mejor_threshold}": {}}
        data_izq = data[data[mejor_atributo] <= mejor_threshold]
        data_der = data[data[mejor_atributo] > mejor_threshold]
        arbol[f"{mejor_atributo} <= {mejor_threshold}"]["True"] = construir_arbol_binario(data_izq, atributos, atributo_clase)
        arbol[f"{mejor_atributo} <= {mejor_threshold}"]["False"] = construir_arbol_binario(data_der, atributos, atributo_clase)
    else:
        arbol = {mejor_atributo: {}}
        for valor in np.unique(data[mejor_atributo]):
            subset_data = data[data[mejor_atributo] == valor]
            nuevo_arbol = construir_arbol_binario(subset_data, [a for a in atributos if a != mejor_atributo], atributo_clase)
            arbol[mejor_atributo][valor] = nuevo_arbol

    return arbol

# Construcción del árbol clásico ID3
def construir_arbol_id3(data, atributos, atributo_clase):
    clases_unicas = np.unique(data[atributo_clase])
    if len(clases_unicas) == 1:
        return clases_unicas[0]
    
    if len(atributos) == 0:
        return data[atributo_clase].mode()[0]

    mejor_atributo = seleccionar_mejor_atributo(data, atributos, atributo_clase)
    arbol = {mejor_atributo: {}}

    for valor in np.unique(data[mejor_atributo]):
        subset_data = data[data[mejor_atributo] == valor]
        nuevo_arbol = construir_arbol_id3(subset_data, [a for a in atributos if a != mejor_atributo], atributo_clase)
        arbol[mejor_atributo][valor] = nuevo_arbol
    
    return arbol

# Seleccionar el mejor atributo en el algoritmo ID3 Clásico
def seleccionar_mejor_atributo(data, atributos, atributo_clase):
    ganancia_maxima = -1
    mejor_atributo = None
    for atributo in atributos:
        ganancia = ganancia_informacion(data, atributo, atributo_clase)
        if ganancia > ganancia_maxima:
            ganancia_maxima = ganancia
            mejor_atributo = atributo
    return mejor_atributo

from itertools import combinations

def mejor_division_binaria(data, atributo, atributo_clase, criterio="entropia"):
    valores_unicos = np.unique(data[atributo])
    mejor_ganancia = -1
    mejor_grupo_izq = None
    mejor_grupo_der = None

    for i in range(1, len(valores_unicos) // 2 + 1):
        for grupo_izq in combinations(valores_unicos, i):
            grupo_der = [v for v in valores_unicos if v not in grupo_izq]
            data_izq = data[data[atributo].isin(grupo_izq)]
            data_der = data[data[atributo].isin(grupo_der)]

            if criterio == "entropia":
                impureza_izq = calcular_entropia(data_izq, atributo_clase)
                impureza_der = calcular_entropia(data_der, atributo_clase)
            else:
                impureza_izq = calcular_indice_gini(data_izq, atributo_clase)
                impureza_der = calcular_indice_gini(data_der, atributo_clase)

            peso_izq = len(data_izq) / len(data)
            peso_der = len(data_der) / len(data)

            ganancia = (calcular_entropia(data, atributo_clase) if criterio == "entropia" else calcular_indice_gini(data, atributo_clase)) - (peso_izq * impureza_izq + peso_der * impureza_der)

            if ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_grupo_izq = grupo_izq
                mejor_grupo_der = grupo_der

    return mejor_grupo_izq, mejor_grupo_der, mejor_ganancia


def construir_arbol_binario_categorico(data, atributos, atributo_clase, criterio="entropia"):
    clases_unicas = np.unique(data[atributo_clase])
    if len(clases_unicas) == 1:
        return clases_unicas[0]

    mejor_atributo = None
    mejor_ganancia = -1
    mejor_grupo_izq = None
    mejor_grupo_der = None

    for atributo in atributos:
        grupo_izq, grupo_der, ganancia = mejor_division_binaria(data, atributo, atributo_clase, criterio)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_atributo = atributo
            mejor_grupo_izq = grupo_izq
            mejor_grupo_der = grupo_der

    if mejor_atributo is None:
        return data[atributo_clase].mode()[0]

    arbol = {mejor_atributo: {
        f"{' o '.join(map(str, mejor_grupo_izq))}": construir_arbol_binario_categorico(
            data[data[mejor_atributo].isin(mejor_grupo_izq)], 
            [a for a in atributos if a != mejor_atributo], 
            atributo_clase, criterio
        ),
        f"{' o '.join(map(str, mejor_grupo_der))}": construir_arbol_binario_categorico(
            data[data[mejor_atributo].isin(mejor_grupo_der)], 
            [a for a in atributos if a != mejor_atributo], 
            atributo_clase, criterio
        )
    }}

    return arbol



from graphviz import Digraph

def visualizar_arbol(arbol, nombre_nodo=None, grafo=None):
    if grafo is None:
        grafo = Digraph(format="png")
    
    if isinstance(arbol, dict):
        for atributo, ramas in arbol.items():
            nodo_atributo = str(atributo) if nombre_nodo is None else nombre_nodo
            grafo.node(nodo_atributo, label=str(atributo), shape='box', style='filled', color='lightblue')

            for valor, sub_arbol in ramas.items():
                if isinstance(sub_arbol, dict):
                    nodo_hijo = f"{nodo_atributo}_{valor}"
                    grafo.edge(nodo_atributo, nodo_hijo, label=str(valor))
                    visualizar_arbol(sub_arbol, nombre_nodo=nodo_hijo, grafo=grafo)
                else:
                    nodo_hoja = f"{nodo_atributo}_{valor}_hoja"
                    grafo.node(nodo_hoja, label=str(sub_arbol), shape='ellipse', style='filled', color='lightgrey')
                    grafo.edge(nodo_atributo, nodo_hoja, label=str(valor))
    
    return grafo

def extraer_reglas(arbol, camino="", reglas=None):
    if reglas is None:
        reglas = []

    if not isinstance(arbol, dict):
        regla = f"{camino} => {arbol}"
        reglas.append(regla)
        return reglas

    for atributo, ramas in arbol.items():
        for valor, sub_arbol in ramas.items():
            nueva_rama = f"{camino}({atributo} = {valor}) "
            extraer_reglas(sub_arbol, nueva_rama, reglas)

    return reglas

def mejor_umbral_numerico(data, atributo, atributo_clase, criterio="entropia"):
    valores_unicos = np.sort(data[atributo].unique())
    mejor_ganancia = -1
    mejor_threshold = None

    for i in range(len(valores_unicos) - 1):
        threshold = (valores_unicos[i] + valores_unicos[i + 1]) / 2
        data_izq = data[data[atributo] <= threshold]
        data_der = data[data[atributo] > threshold]

        if len(data_izq) == 0 or len(data_der) == 0:
            continue

        if criterio == "entropia":
            impureza_izq = calcular_entropia(data_izq, atributo_clase)
            impureza_der = calcular_entropia(data_der, atributo_clase)
        else:
            impureza_izq = calcular_indice_gini(data_izq, atributo_clase)
            impureza_der = calcular_indice_gini(data_der, atributo_clase)
        
        peso_izq = len(data_izq) / len(data)
        peso_der = len(data_der) / len(data)

        ganancia = (calcular_entropia(data, atributo_clase) if criterio == "entropia" else calcular_indice_gini(data, atributo_clase)) - (peso_izq * impureza_izq + peso_der * impureza_der)

        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_threshold = threshold

    return mejor_threshold, mejor_ganancia


def construir_arbol_binario_numerico(data, atributos, atributo_clase, criterio="entropia"):
    clases_unicas = np.unique(data[atributo_clase])
    if len(clases_unicas) == 1:
        return clases_unicas[0]

    mejor_atributo = None
    mejor_ganancia = -1
    mejor_threshold = None

    for atributo in atributos:
        if data[atributo].dtype in [np.int64, np.float64]:  # Atributo numérico
            threshold, ganancia = mejor_umbral_numerico(data, atributo, atributo_clase, criterio)
            if ganancia > mejor_ganancia:
                mejor_ganancia = ganancia
                mejor_atributo = atributo
                mejor_threshold = threshold

    if mejor_atributo is None:
        return data[atributo_clase].mode()[0]

    arbol = {mejor_atributo: {
        f"<= {mejor_threshold}": construir_arbol_binario_numerico(
            data[data[mejor_atributo] <= mejor_threshold], atributos, atributo_clase, criterio
        ),
        f"> {mejor_threshold}": construir_arbol_binario_numerico(
            data[data[mejor_atributo] > mejor_threshold], atributos, atributo_clase, criterio
        )
    }}

    return arbol

