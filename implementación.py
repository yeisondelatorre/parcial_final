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
    - **DESCRIPCIÓN DEL DASH**
El objetivo de este dashboard es proporcionar a la institución académica una herramienta visual e interactiva que 
permita monitorear de manera efectiva el proceso de admisión y la satisfacción estudiantil. A través de la implementación 
de un prototipo en Streamlit, se busca analizar métricas clave como el total de aplicaciones, admisiones e inscripciones por semestre, las 
tendencias de la tasa de retención a lo largo del tiempo, y los niveles de satisfacción estudiantil. Además, se incluirá un desglose de
las inscripciones por departamento (Ingeniería, Negocios, Artes y Ciencias) y se realizará una comparación entre las tendencias de los 
semestres de Primavera y Otoño. Este análisis permitirá identificar las principales tendencias y patrones en los datos, proporcionando 
hallazgos clave y perspectivas accionables para mejorar los procesos académicos y de retención de estudiantes.
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

            # Filtrando los productos más vendidos
            productos_filtrar = [590101, 590102, 590103, 205003, 200130, 800020, 205601, 540101, 501121, 501120]
            dfinal = df[df['codproducto'].isin(productos_filtrar)]  # Filtrar productos

            # Estadísticas descriptivas
            st.write("Estadísticas Descriptivas:")
            st.write(dfinal.describe())  # Muestra las estadísticas de los productos filtrados

            # Histograma de los productos vendidos
            st.subheader("Histograma de Productos Vendidos")
            plt.figure(figsize=(12, 6))
            dfinal.groupby('nom_producto')['Total_Venta'].sum().plot(kind='bar', color='seagreen', alpha=0.7, edgecolor='black')
            plt.xlabel("Producto", fontsize=12)
            plt.ylabel("Total de Ventas", fontsize=12)
            plt.title("Total de Ventas por Producto", fontsize=14)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()  # Asegura que las etiquetas no se corten
            st.pyplot(plt)  # Mostrar gráfico en Streamlit

            # Filtrando los datos para el semestre "Spring"
            spring_data = dfinal[dfinal['Term'] == 'Spring']

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
            fig2 = px.line(dfinal, 
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
            fig3 = px.line(dfinal, 
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

