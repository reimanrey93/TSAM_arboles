
# Proyecto de Árboles de Decisión

Este proyecto implementa un sistema de árboles de decisión en Python, permitiendo la construcción de árboles binarios y árboles ID3 para datos categóricos y numéricos. Además, se ofrece la opción de seleccionar el criterio de impureza (entropía o índice Gini) para evaluar la calidad de las particiones.

## Requisitos Previos

- Python 3.7 o superior
- Git

## Instrucciones de Instalación y Configuración

### 1. Clonar el Repositorio

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/reimanrey93/TSAM_arboles.git
cd TSAM_arboles
```

### 2. Crear un Entorno Virtual

Se recomienda crear un entorno virtual para evitar conflictos con otras dependencias de Python instaladas en tu sistema:

```bash
python3 -m venv venv
```

Activa el entorno virtual:

- **En Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **En macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 3. Instalar las Dependencias

Con el entorno virtual activado, instala las dependencias necesarias para el proyecto usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias, como `numpy`, `pandas`, `streamlit`, y `graphviz`.

### 4. Instalar Graphviz (Opcional)

Para la visualización del árbol, el proyecto utiliza `Graphviz`. Dependiendo de tu sistema operativo, puede que necesites instalar `Graphviz` aparte.

- **En Windows**: [Descarga el instalador de Graphviz](https://graphviz.gitlab.io/_pages/Download/Download_windows.html) e instálalo. Asegúrate de agregar `Graphviz` al PATH de tu sistema.

- **En macOS**: Usa `brew` para instalar `Graphviz`:

  ```bash
  brew install graphviz
  ```

- **En Linux**: Usa el administrador de paquetes para instalar `Graphviz`:

  ```bash
  sudo apt-get install graphviz
  ```

### 5. Ejecutar la Aplicación

Con las dependencias instaladas y `Graphviz` configurado, puedes ejecutar la aplicación de Streamlit:

```bash
streamlit run app.py
```

Esto abrirá la aplicación en tu navegador por defecto, normalmente en `http://localhost:8501`.

## Uso de la Aplicación

1. **Subir un archivo CSV**: Sube un archivo CSV con los datos de entrada que quieres usar para construir el árbol de decisión.
2. **Seleccionar el atributo de clase**: Elige el atributo objetivo o de clase para el árbol de decisión.
3. **Elegir el tipo de árbol**: Selecciona entre las opciones disponibles:
   - ID3 Clásico
   - ID3 Adaptado para Atributos Numéricos
   - ID3 Clásico Binario para Datos Categóricos
   - ID3 Binario para Datos Numéricos
4. **Seleccionar el criterio de impureza**: Puedes elegir entre `entropía` y `índice Gini` como criterio de impureza.
5. **Construir el Árbol**: Haz clic en el botón para construir el árbol de decisión y visualizarlo.

## Desactivar el Entorno Virtual

Cuando hayas terminado, desactiva el entorno virtual con:

```bash
deactivate
```

---

Con estas instrucciones, deberías poder configurar y ejecutar el proyecto en tu máquina. Si tienes problemas o preguntas, no dudes en abrir un issue en el repositorio.
