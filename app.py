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
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster


load_dotenv()


@st.cache_data
def load_base_data():
    bra_municipios = gpd.read_file("zip://BR_Municipios_2021.zip")

    simplified_bra_municipios = bra_municipios.copy()
    simplified_bra_municipios['geometry'] = simplified_bra_municipios['geometry'].simplify(tolerance = 0.01)
    simplified_bra_municipios['CD_MUN'] = simplified_bra_municipios['CD_MUN'].astype(str)

    bra_castana = pd.read_csv("bra_castana_production_by_municipality.csv")
    bra_castana['CD_MUN'] = bra_castana['CD_MUN'].astype(str)

    bra_gdf_castana = simplified_bra_municipios.merge(bra_castana, how = 'left', left_on = 'CD_MUN', right_on = 'CD_MUN')

    return bra_gdf_castana


def get_colormap(values: List[float]) -> cm.ColorMap:
    min_value, max_value = min(values), max(values)
    colormap = cm.linear.YlOrRd_09.scale(min_value, max_value)
    return colormap

# Base page info
st.title("Brazil Nut and Soy Production in the Amazon Basin")

# Load static data
bra_gdf_castana = load_base_data()

# castana_colormap = get_colormap(bra_gdf_castana['2022'])

def get_color(value):
    if value == None:
        return '#fff5f0'
    if value >= 0 and value <= 1:
        return '#fff5f0'
    if value > 1 and value <= 200:
        return '#fdccb8'
    if value > 200 and value <= 1000:
        return '#fc8f6f'
    if value > 1000 and value <= 2000:
        return '#f44d37'
    if value > 2000 and value <= 3000:
        return '#c5161b'
    if value > 3000:
        return '#67000d'
    else:
        return '#fff5f0'
    
m = folium.Map(location=[-3.4653, -62.2159], zoom_start=5, prefer_canvas = True)


brazil_castana_2018_layer = folium.GeoJson(
    bra_gdf_castana,
    name = '2018 Castana Production in Brazil',
    show = False,
    style_function = lambda feature: {
        'fillColor': get_color(feature['properties']['2018']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.75
    },
    highlight_function=lambda feature: {
        'fillColor': 'yellow',   # Change color on hover
        'color': 'black',         # Keep border black on hover
        'weight': 1.5,            # Increase weight on hover
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', '2018'],  # Replace with the name of your column
        aliases=['Municipality:', '2018 Brazil Nut Production'],             # Tooltip alias
        localize=True                   # Localize numbers
    )
).add_to(m)

brazil_castana_2019_layer = folium.GeoJson(
    bra_gdf_castana,
    show = False,
    name = '2019 Castana Production in Brazil',
    style_function = lambda feature: {
        'fillColor': get_color(feature['properties']['2019']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.75
    },
    highlight_function=lambda feature: {
        'fillColor': 'yellow',   # Change color on hover
        'color': 'black',         # Keep border black on hover
        'weight': 1.5,            # Increase weight on hover
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', '2019'],  # Replace with the name of your column
        aliases=['Municipality:', '2019 Brazil Nut Production'],             # Tooltip alias
        localize=True                   # Localize numbers
    )
).add_to(m)

brazil_castana_2020_layer = folium.GeoJson(
    bra_gdf_castana,
    show = False,
    name = '2020 Castana Production in Brazil',
    style_function = lambda feature: {
        'fillColor': get_color(feature['properties']['2020']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.75
    },
    highlight_function=lambda feature: {
        'fillColor': 'yellow',   # Change color on hover
        'color': 'black',         # Keep border black on hover
        'weight': 1.5,            # Increase weight on hover
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', '2020'],  # Replace with the name of your column
        aliases=['Municipality:', '2020 Brazil Nut Production'],             # Tooltip alias
        localize=True                   # Localize numbers
    )
).add_to(m)

brazil_castana_2021_layer = folium.GeoJson(
    bra_gdf_castana,
    show = False,
    name = '2021 Castana Production in Brazil',
    style_function = lambda feature: {
        'fillColor': get_color(feature['properties']['2021']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.75
    },
    highlight_function=lambda feature: {
        'fillColor': 'yellow',   # Change color on hover
        'color': 'black',         # Keep border black on hover
        'weight': 1.5,            # Increase weight on hover
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', '2021'],  # Replace with the name of your column
        aliases=['Municipality:', '2021 Brazil Nut Production'],             # Tooltip alias
        localize=True                   # Localize numbers
    )
).add_to(m)

brazil_castana_2022_layer = folium.GeoJson(
    bra_gdf_castana,
    name = '2022 Castana Production in Brazil',
    style_function = lambda feature: {
        'fillColor': get_color(feature['properties']['2022']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.75
    },
    highlight_function=lambda feature: {
        'fillColor': 'yellow',   # Change color on hover
        'color': 'black',         # Keep border black on hover
        'weight': 1.5,            # Increase weight on hover
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', '2022'],  # Replace with the name of your column
        aliases=['Municipality:', '2022 Brazil Nut Production'],             # Tooltip alias
        localize=True                   # Localize numbers
    )
).add_to(m)



folium.LayerControl(collapsed = False).add_to(m)

st_data = st_folium(m, width=725)