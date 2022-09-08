from functools import cache
from unicodedata import numeric
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

#--- IMPORTAMOS LOS DATOS ---#
df=pd.read_csv("clean_airbnb (1).csv", encoding= "ISO-8859-1")

#--- CONFIGURACIÓN DE PÁGINA ---#
st.set_page_config(page_title="Airbnb",
                   page_icon=":busts_in_silhouette:")

st.title("Plataforma Airbnb")
st.markdown("Esta plataforma muestra datos y gráficos de interés sobre los inmuebles Airbnb de la ciudad de México")

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

histo= st.sidebar.checkbox("Distribución de precios de inmuebles")
if histo:
    fig, ax = plt.subplots()
    ax.hist(data.price)
    st.header("Distribución del precio de los inmuebles")
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
    ax.set_xlabel("Precio promedio por delegación")
    st.header("Delegacion con el precio promedio")
    st.pyplot(fig)
    st.markdown("_")

DATA_URL = ('clean_airbnb (1).csv')
DATE_COLUMN = 'neighbourhood'
LAT = 'latitude'
LON = 'longitude'

#st.title("Ubicaciones de las casas")
#st.header("Casas") 
#test = data["neighbourhood"]
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [19.42, -99.12],
    columns=['latitude', 'longitude'])
st.map(map_data)



#Creamos el mapa 
#LAT = (df["latitude"])
#LON = (df["longitude"])

#iltered_data = df[df["neighbourhood"] ]
#st.subheader('Ubicación de inmuebles en')
#map_data = pd.DataFrame(columns=[LAT, LON])
#st.map(map_data)

st.header("Conclusiones")
st.write("Se observa que gracias a los gráficos mostrados dentro de nuestra plataforma, podemos recabar información acerca de los inmuebles de Ciudad de México registrados con Airbnb. Podemos explorar la disftribución de precio por delegación. También podemos filtrar por rango de precio y por tipo de habitación ")
st.write("El análisis gráfico nos indica que el rango de precios de los inmuebles se concentra en el rango 200 a los 6000 y si bien hay inmuebles de precios mucho más altos estos no son tan frecuentes")
st.write("Observamos que el precio promedio es más cara una casa/departamento entero que una habitación privada, habitación de hotel y habitación compartida")
st.write("Se puede notar que hay variación de precios promedio por delegación. Vemos que los inmuebles con los precios más altos se ubican en Benito Juárez, Cuauhtémoc, Miguel Hidalgo")

