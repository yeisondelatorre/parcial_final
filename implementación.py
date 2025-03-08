import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Título del dashboard
st.title("Dashboard de Implementación Estudiantil")

# Crear una barra lateral o pestañas para seleccionar entre diferentes secciones
option = st.sidebar.radio("Selecciona una opción", ["Introducción", "EDA"])

if option == "Introducción":
    st.subheader("Introducción de la Base de Datos")
    st.markdown("""
    Este dashboard presenta el análisis de datos de [nombre del conjunto de datos]. Los datos fueron capturados a partir de [fuente de los datos], utilizando técnicas de [método de captura de datos], entre [fecha de inicio] y [fecha de fin].

    Los objetivos principales del análisis son:
    - [Objetivo 1]
    - [Objetivo 2]
    - [Objetivo 3]
    """)

elif option == "EDA":
    st.subheader("Análisis Exploratorio de Datos (EDA)")
    st.write("""
    En esta sección realizaremos el análisis exploratorio de datos (EDA) para comprender mejor la base de datos.
    Se pueden incluir gráficas, estadísticas descriptivas y otras herramientas útiles para explorar los datos.
    """)

    uploaded_file = st.file_uploader("Cargar archivo CSV", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Primeras filas del dataframe:")
            st.write(df.head())  # Muestra las primeras filas del dataframe

            # Estadísticas descriptivas
            st.write("Estadísticas Descriptivas:")
            st.write(df.describe())

            # Filtrando los datos para el semestre "Spring"
            spring_data = df[df['Term'] == 'Spring']

            # Agrupar por año y calcular las sumas de inscripciones por categoría
            enrollment_by_year = spring_data.groupby('Year').agg(
                {'Enrolled': 'sum', 
                 'Engineering Enrolled': 'sum', 
                 'Business Enrolled': 'sum', 
                 'Arts Enrolled': 'sum', 
                 'Science Enrolled': 'sum'}
            ).reset_index()

            # Calcular los porcentajes por cada categoría
            enrollment_by_year['Engineering %'] = (enrollment_by_year['Engineering Enrolled'] / enrollment_by_year['Enrolled']) * 100
            enrollment_by_year['Business %'] = (enrollment_by_year['Business Enrolled'] / enrollment_by_year['Enrolled']) * 100
            enrollment_by_year['Arts %'] = (enrollment_by_year['Arts Enrolled'] / enrollment_by_year['Enrolled']) * 100
            enrollment_by_year['Science %'] = (enrollment_by_year['Science Enrolled'] / enrollment_by_year['Enrolled']) * 100

            # Gráfico de barras con porcentajes de estudiantes inscritos por carrera
            fig1 = px.bar(enrollment_by_year, 
                          x='Year', 
                          y=['Engineering %', 'Business %', 'Arts %', 'Science %'],
                          title='Percentage of Enrolled Students by Major (Spring Term)',
                          labels={'value': 'Percentage of Enrolled Students', 'variable': 'Major', 'Year': 'Year'},
                          color_discrete_sequence=px.colors.qualitative.Set3)  # Colores diferentes

            st.plotly_chart(fig1)  # Mostrar gráfico en Streamlit

            # Gráfico de líneas con la tendencia de inscripciones por departamento
            fig2 = px.line(df, 
                           x='Year', 
                           y=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'], 
                           title='Trends in Enrolled Students by Department',
                           labels={'value': 'Number of Enrolled Students', 'variable': 'Department'},
                           markers=True)
            fig2.update_layout(
                xaxis_title="Year", 
                yaxis_title="Number of Enrolled Students"
            )
            st.plotly_chart(fig2)  # Mostrar gráfico en Streamlit

            # Crear gráfico de líneas para Retention Rate y Student Satisfaction
            fig3 = px.line(df, 
                           x='Year', 
                           y=['Retention Rate (%)', 'Student Satisfaction (%)'], 
                           title='Retention Rate and Student Satisfaction by Year',
                           markers=True,  # Agregar puntos a las líneas
                           line_shape='linear',  # Forma de las líneas
                           labels={'value': 'Percentage', 'variable': 'Metric'},
                           color_discrete_sequence=['#1f77b4', '#ff7f0e'])  # Diferentes colores para Retention Rate y Satisfaction
            fig3.update_layout(
                xaxis_title="Year", 
                yaxis_title="Percentage",
                legend_title="Metrics"
            )
            st.plotly_chart(fig3)  # Mostrar gráfico en Streamlit

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

