from functools import cache
from unicodedata import numeric
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#--- IMPORTAMOS LOS DATOS ---#
df=pd.read_csv("clean_airbnb (1).csv", encoding= "ISO-8859-1")

#--- CONFIGURACIÓN DE PÁGINA ---#
st.set_page_config(page_title="Airbnb",
                   page_icon=":busts_in_silhouette:")

st.title("Análisis Airbnb")
st.markdown("Estima el precio de renta, plusvalía ")

#--- LOGO ---#
st.sidebar.image("airbnblogo.jpg")
st.sidebar.markdown("##")

#Aplicamos cache a nuestros datos
@st.cache
def load_data(nrows):
    data = pd.read_csv("clean_airbnb (1).csv", nrows=nrows, encoding= "ISO-8859-1")
    lowercase = lambda x: str(x).lower()
    return data

data_load_state = st.text('Cargando datos...')
data = load_data(1000)
data_load_state.text("Los datos han sido cargados")

#El código que permita desplegar un control para seleccionar la delegación de la ciudad
@st.cache
def load_data_del(neighbourhood):
  filtered_data_del=df[df['neighbourhood'] == neighbourhood]
  return filtered_data_del


selected_del = st.sidebar.selectbox("Selecciona la delegación",df['neighbourhood'].unique())
btnFilterbydel = st.sidebar.button("Filtrar por delegación")

if (btnFilterbydel):
  filterbydel = load_data_del(selected_del)
  count_row1 = filterbydel.shape[0]
  st.write(f"Resultados totales: {count_row1}")
  st.title("Filtro por delegación")
  st.dataframe(filterbydel)






#El código que permita filtrar por rangos de precios del mínimo al máximo
#@st.cache
#def load_data_price(price):
  #filtered_data_price=data[data['price'] == price]
  #return filtered_data_price

#filterbyprice = st.sidebar.slider("price", 0, 999998, 1450)
#filtered_byprice = df[df["price"] == filterbyprice]
#count_row2 = filterbyprice.shape[0]

#st.write(f"Resultados totales: {count_row2}")
#st.dataframe(filtered_byprice)
#El código que permita filtrar por rangos de precios del mínimo al máximo


price_min = st.sidebar.slider(
    "Precio mínimo",
    min_value=float(data['price'].min()),
    max_value=float(data['price'].max())
)
price_max = st.sidebar.slider(
    "Precio máximo",
    min_value=float(data['price'].min()),
    max_value=float(data['price'].max())
)
subset_price = data[ (data['price'] >= price_min) & (data['price'] <= price_max)]

st.write(f"Number of registros con precio entre {price_min} and {price_max}: {subset_price.shape[0]}")
st.write(subset_price)

#El código que permita desplegar un control para seleccionar el tipo de habitación
@st.cache
def load_data_del(room_type):
  filtered_data_room=df[df['room_type'] == room_type]

  return filtered_data_room

selected_room = st.sidebar.selectbox("Selecciona el tipo de habitación",df['room_type'].unique())
btnFilterbyroom = st.sidebar.button("Filtrar por tipo de habitación")

if (btnFilterbyroom):
  filterbyroom = load_data_del(selected_room)
  count_row3 = filterbyroom.shape[0]
  st.write(f"Resultados totales: {count_row3}")
  st.title("Filtro por tipo de habitación")
  st.dataframe(filterbyroom)


#Gibran

histo= st.sidebar.checkbox("Distribución de precios de casas")
if histo:
    fig, ax = plt.subplots()
    ax.hist(data.price)
    st.header("Distribución del precio de las habitaciones")
    st.pyplot(fig)
    st.markdown("_")


graf= st.sidebar.checkbox("Habitaciones por precio promedio") 
if graf:
    fig, ax = plt.subplots()
    x= data["room_type"]
    y=data["price"]
    ax.barh(x,y)
    ax.set_ylabel("Tipo de habitacion")
    ax.set_xlabel("Precio promedio de todas las casas")
    st.header("Habitaciones por precio promedio")
    st.pyplot(fig)
    st.markdown("_")



graf1= st.sidebar.checkbox("Delegacion por el precio promedio") 
if graf1:
    fig, ax = plt.subplots()
    x= data["neighbourhood"]
    y=data["price"]
    ax.barh(x,y)
    ax.set_ylabel("Municipio")
    ax.set_xlabel("Precio promedio por municipio ")
    st.header("DElegacion con el precio promedio")
    st.pyplot(fig)
    st.markdown("_")






