import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# File uploader
uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    df = pd.read_csv(uploaded_file, encoding='UTF-8-SIG')
    
    # Filter by municipality (assuming the municipality data is in a column 'Municipio')
    municipio = st.selectbox("Seleccione el municipio", df['Municipio'].unique())
    df_filtered = df[df['Municipio'] == municipio]
    
    # Mapping variables to questions
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

    # Selection of questions to analyze
    selected_questions = st.multiselect("Seleccione las preguntas para analizar", list(preguntas.values()))

    # Display results for each selected question
    for pregunta in selected_questions:
        # Find the corresponding column in the dataframe
        column = [k for k, v in preguntas.items() if v == pregunta][0]
        
        st.write(f"**{pregunta}**")
        
        # Plot results
        if df_filtered[column].dtype == 'object':
            # Categorical data: bar plot
            chart_data = df_filtered[column].value_counts()
            st.bar_chart(chart_data)
        else:
            # Numerical data: histogram and mean
            st.write(f"Media: {df_filtered[column].mean()}")
            st.histogram(df_filtered[column])

        st.write("---")  # Add a separator between questions
