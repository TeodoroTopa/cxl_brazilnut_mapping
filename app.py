import json
import os
from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple

import branca.colormap as cm
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import requests
import streamlit as st
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from streamlit_folium import st_folium, folium, folium_static
from folium.plugins import MarkerCluster


load_dotenv()

# Base page info
st.title("Recent Brazil Nut and Soy Production in the Amazon Basin")


@st.cache_data
def load_base_data():
    locations = {
    'AFIMAD': (-13.180679543510646, -69.4089469802327),
    'COOPAVAM': (-10.382857589742994, -58.419712312184615),
    'RECA': (-9.75686765859735, -66.6075266735577),
    'RONAP': (-12.591430033691857, -69.17701635817673),
    'COOPERACRE': (-10.029457122219789, -67.7972471794766),
    'COOPBAY': (-7.871209772219521, -51.8345907706893),
    'FEPROCAMD': (-12.111794449723988, -76.98961676442958),
    'ABNC': (-23.557338640005376, -46.661260686767605),
    'GREENFOREST': (-10.996698548344776, -66.07256528093042)
    }

    base_data = gpd.read_file("final_map_data.geojson")


    return base_data, locations


castana_colormap = cm.StepColormap(['#fff5f0', '#FDE6DD', '#fdccb8', '#fc8f6f', '#f44d37', '#c5161b', '#67000d'],
                                   index = [0, 10, 200, 1000, 2000, 3000, 10000])


soy_colormap = cm.StepColormap(['#fff5f0', '#FDE6DD', '#fdccb8', '#fc8f6f', '#f44d37', '#c5161b', '#67000d', '#48010A'],
                                   index = [0, 1000, 50000, 100000, 250000, 500000, 1000000, 10000000])

def get_color(value, crop, castana_colormap = castana_colormap, soy_colormap = soy_colormap):
    if crop == 'Brazil Nut':
        color = castana_colormap(value)
        opacity =  0.01 if value <= 10 else 0.75
        return color, opacity
    if crop == 'Soy':
        color = soy_colormap(value)
        opacity =  0.1 if value < 1000 else 0.75
        return color, opacity
    
def get_data_layer(base_data, crop, year, show = False):

    if crop == 'Brazil Nut':
        name = f'{year} {crop} Production in Brazil'
        crop_data = base_data[base_data['Municipality'].str[:6] == 'Brazil']

    elif crop == 'Soy':
        name = f'{year} {crop} Production in Bolivia and Brazil'
        crop_data = base_data
    
    layer = folium.GeoJson(
    crop_data,
    name = name,
    show = show,
    style_function = lambda feature: {
        'fillColor': get_color(feature['properties'][f'{crop} Production {year}'], crop)[0],
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': get_color(feature['properties'][f'{crop} Production {year}'], crop)[1]
        },
    highlight_function=lambda feature: {
        'fillColor': 'yellow',   # Change color on hover
        'color': 'black',         # Keep border black on hover
        'weight': 1.5,            # Increase weight on hover
        'fillOpacity': get_color(feature['properties'][f'{crop} Production {year}'], crop)[1]
        },
    tooltip=folium.GeoJsonTooltip(
        fields=['Municipality', f'{crop} Production {year}'],  # Replace with the name of your column
        aliases=['Municipality:', f'{year} {crop} Production (metric tons)'],             # Tooltip alias
        localize=True                   # Localize numbers
        )
    )
    return layer


base_data, locations = load_base_data()

m = folium.Map(location=[-3.4653, -62.2159],
               zoom_start=5,
               prefer_canvas = True)

castana_2019_layer = get_data_layer(base_data, 'Brazil Nut', '2019')
castana_2020_layer = get_data_layer(base_data, 'Brazil Nut', '2020')
castana_2021_layer = get_data_layer(base_data, 'Brazil Nut', '2021')
castana_2022_layer = get_data_layer(base_data, 'Brazil Nut', '2022')
castana_2023_layer = get_data_layer(base_data, 'Brazil Nut', '2023', show = True)


soy_2019_layer = get_data_layer(base_data, 'Soy', '2019')
soy_2020_layer = get_data_layer(base_data, 'Soy', '2020')
soy_2021_layer = get_data_layer(base_data, 'Soy', '2021')
soy_2022_layer = get_data_layer(base_data, 'Soy', '2022')
soy_2023_layer = get_data_layer(base_data, 'Soy', '2023')

# Create a FeatureGroup to hold the points
ngos_layer_group = folium.FeatureGroup(name='Brazil Nut Production and Protection Organizations')
for name, coordinates in locations.items():
    folium.Marker(
        location=coordinates,
        popup=name,
        icon=folium.Icon(color='blue')  # Use basic color
    ).add_to(ngos_layer_group)



castana_2019_layer.add_to(m)
castana_2020_layer.add_to(m)
castana_2021_layer.add_to(m)
castana_2022_layer.add_to(m)
castana_2023_layer.add_to(m)
soy_2019_layer.add_to(m)
soy_2020_layer.add_to(m)
soy_2021_layer.add_to(m)
soy_2022_layer.add_to(m)
soy_2023_layer.add_to(m)
ngos_layer_group.add_to(m)

folium.LayerControl().add_to(m)

nuts = {
    'Country': ['Brazil', 'Bolivia', 'Peru'],
    'Brazil Nut Production (metric tons)': [38169, 34020, 7088]
}

soy = {
    'Country': ['Brazil', 'Bolivia', 'Peru'],
    'Soy Production (metric tons)': [120701031, 3457144, 1596]
}

nutdf = pd.DataFrame(nuts)
soydf = pd.DataFrame(soy)


st_data = folium_static(m, width=725, height = 500)

st.markdown("""
Municipality level Brazil Nut production reporting was not found for Bolivia or Peru, and Peru also lacked municipial level Soy production reporting.
Please see the below tables for 2022 national productions statistics from comparison purposes after exploring the interactive map!
""")

st.title('National Brazil Nut Production 2022')
st.dataframe(nutdf)

st.title('National Soy Production 2022')
st.dataframe(soydf)