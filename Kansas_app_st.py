import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from shapely import wkt

#insert custom styling with CSS
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

@st.cache_data
def load_data():
    crime_data = pd.read_csv('final_data.csv')
    return crime_data

crime_data= load_data()  

#converting the geometry columns to geometry format
crime_data['Year'].astype(int)
crime_data['geometry'] = crime_data['geometry'].apply(wkt.loads)
crime_data = gpd.GeoDataFrame(crime_data, geometry='geometry')

### CREATING THE APP ###
#image in the sidebar
image = Image.open('Flag_of_Kansas.png')
st.sidebar.image(image, caption='Ad astra per aspera')

#title of the app
st.sidebar.title(':blue[Kansas Crime rate per 100.000 hab]')

#sidebar widgets 
crime_type = ['Murder', 'Robbery', 'Assault', 'Burglary', 'Larceny', 'Motor_vehicle_theft']  
sidebar_year= st.sidebar.slider('SELECT YEAR:', 2003, 2020)
selected_crime = st.sidebar.selectbox("SELECT TYPE OF CRIME:", crime_type)
    
## Filtrar los datos según la selección del usuario
filtered_data = crime_data[(crime_data['Year'] == sidebar_year)]

# Crear el mapa cloroplético con Plotly
st.header(f'Crime rate - {selected_crime} ({sidebar_year})')
fig = px.choropleth_mapbox(filtered_data,
                           geojson=filtered_data.geometry.geometry,
                           locations=filtered_data.index,
                           color=selected_crime,
                           hover_name='City',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=7,
                           center={"lat": 39.04833, "lon": -95.67804},
                           opacity=0.9)


# Agregar las iniciales del nombre de cada ciudad en el centro del gráfico
for index, row in filtered_data.iterrows():
    city_name = row['City']
    city_initials = ''.join(word[0] for word in city_name.split())
    city_center = row['geometry'].centroid
    fig.add_text(lon=city_center.x, lat=city_center.y, text=city_initials,
                 showarrow=False, font=dict(size=12, color='black'))

####revisar
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True, key='styled-graph')

st.sidebar.markdown('''
---
Created by Elianneth Cabrera
''')