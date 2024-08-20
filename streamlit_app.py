import streamlit as st
import pandas as pd
import numpy as np

# Título de la aplicación
st.title('Análisis de Encuesta')

# Cargar el archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV
    df = pd.read_csv(uploaded_file, encoding='UTF-8-SIG')

    # Crear un diccionario de mapeo de variables a preguntas
    preguntas = {
        'P05': '¿Cuál es su ocupación principal?',
        'SexoEntrevistado': 'Sexo del entrevistado',
        'EdadEntrevistado': 'Edad del entrevistado',
        'P09': '¿Cuál es su nivel de educación?',
        'EP35': '¿Está registrado para votar?',
        'EP93_1': 'Intención de voto para presidente',
        'AGN1CPP': 'Aprobación del Congreso',
        'AGN2ROP': 'Aprobación del Registro de Organizaciones Políticas',
        'AGN3CRPP': 'Aprobación del Consejo Regional',
        'AGN4CC': 'Aprobación de la Contraloría',
        'AGN5CP': 'Aprobación de la Corte Suprema',
        'P94': '¿Votó en las últimas elecciones?',
        'P95': '¿Por quién votó en las últimas elecciones?',
        'GGTRPresidente': 'Aprobación del Presidente',
        'ICG02': 'Situación económica personal',
        'ICG03': 'Situación económica del país',
        'ICG04': 'Situación política del país',
        'ICG05': 'Dirección del país',
        'ICG06_1': 'Principal problema del país',
        'NuevoNSE': 'Nuevo nivel socioeconómico',
        'NSE': 'Nivel socioeconómico',
        'SCEN': 'Escenario',
        'LC_Nacional': 'Localización nacional'
    }

    # Renombrar las columnas del DataFrame
    df_preguntas = df.rename(columns=preguntas)

    # Mostrar el DataFrame con las preguntas
    st.write("Datos de la encuesta:")
    st.dataframe(df_preguntas)
    
    # Seleccionar solo las columnas numéricas
    numeric_columns = df_preguntas.select_dtypes(include=[np.number]).columns
    
    # Calcular la media de cada columna numérica
    means = df_preguntas[numeric_columns].mean().round(2)
    
    # Convertir a un DataFrame para mostrarlo con preguntas
    means_df = pd.DataFrame({
        'Pregunta': means.index.map(preguntas.get),
        'Media': means.values
    }).sort_values(by='Media', ascending=False)
    
    # Mostrar las medias
    st.write("Media de cada pregunta:")
    st.dataframe(means_df)
    
    # Obtener la lista de municipios
    if 'Municipio' in df_preguntas.columns:
        municipios = df_preguntas['Municipio'].unique()
        st.sidebar.header('Filtrar por municipio')
        selected_municipio = st.sidebar.selectbox(
            'Selecciona un municipio',
            options=['Todos'] + list(municipios)
        )
        
        # Filtrar el DataFrame en función del municipio seleccionado
        if selected_municipio != 'Todos':
            df_preguntas = df_preguntas[df_preguntas['Municipio'] == selected_municipio]
    
    # Convertir las columnas numéricas en preguntas (nombres de las columnas)
    questions = df_preguntas.columns.tolist()
    
    # Selección de preguntas para gráficos
    st.sidebar.header('Opciones de gráfico')
    selected_question = st.sidebar.selectbox(
        'Selecciona una pregunta para generar un gráfico',
        options=questions
    )
    
    if selected_question:
        if df_preguntas[selected_question].dtype in [np.int64, np.float64]:  # Verificar si la pregunta es numérica
            st.write(f"Gráfico para la pregunta: {selected_question}")
            st.bar_chart(df_preguntas[selected_question])
        else:
            st.write("La pregunta seleccionada no es numérica. No se puede generar un gráfico de barras.")
    
    # Selección de preguntas para tabla cruzada
    st.sidebar.header('Opciones de tabla cruzada')
    cross_table_question_1 = st.sidebar.selectbox(
        'Selecciona la primera pregunta para la tabla cruzada',
        options=questions
    )
    
    cross_table_question_2 = st.sidebar.selectbox(
        'Selecciona la segunda pregunta para la tabla cruzada',
        options=questions
    )

    if cross_table_question_1 and cross_table_question_2:
        if df_preguntas[cross_table_question_1].dtype in [np.int64, np.float64] and df_preguntas[cross_table_question_2].dtype in [np.int64, np.float64]:  # Verificar si ambas preguntas son numéricas
            st.write(f"Tabla cruzada entre: {cross_table_question_1} y {cross_table_question_2}")
            cross_table = pd.crosstab(df_preguntas[cross_table_question_1], df_preguntas[cross_table_question_2])
            st.write(cross_table)
        else:
            st.write("Ambas preguntas seleccionadas deben ser numéricas para generar una tabla cruzada.")


