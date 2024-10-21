import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="movies-project-v2")
#db= firestore.Client.from_service_account_json("movies-project-v2-firebase-adminsdk-4oiue-8d8ee5efd2.json")  -- Es reemplazado por service account

dbMovies= db.collection("movies")

movies_ref= list (db.collection (u'movies').stream())
movies_dic= list (map (lambda x: x.to_dict(), movies_ref))
movies_dataframe= pd.DataFrame (movies_dic)
movies_dataframe= movies_dataframe.loc[:,['name', 'genre', 'director', 'company']]

def load_data_byname (name):
  dfwork= movies_dataframe.copy()
  data= dfwork[dfwork["name"].str.lower().str.contains(name.lower())]
  return data

def load_data_bydirector (director):
  dfwork= movies_dataframe.copy()
  data= dfwork[dfwork["director"] == director]
  return data

def load_data_all ():
  dfwork= movies_dataframe.copy()
  data= dfwork
  return data

#------------------------------------------
#función para obtener registros por nombre
def loadByName(name):
  names_ref = dbMovies.where(u'name', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname    
  return currentName
#------------------------------------------

st.header ("Netflix app")

#Sidebar - mostrar todos los títulos
btn_mostrar_todos= st.sidebar.button ("Mostrar todos los filmes")
if btn_mostrar_todos:
  data_filtrada= load_data_all ()
  count_row= data_filtrada.shape[0]  
  st.write (f"Número del filmes : {count_row}")
  st.dataframe (data_filtrada)
#=============================

#Sidebar - búsqueda por título
nombre_busq= st.sidebar.text_input("Título del filme")
btn_buscar_titulo= st.sidebar.button ("Buscar filmes")
if nombre_busq and btn_buscar_titulo:
  data_filtrada= load_data_byname (nombre_busq)
  count_row= data_filtrada.shape[0]  
  st.write (f"Número del filmes : {count_row}")
  st.dataframe (data_filtrada)
#=============================  

#Sidebar - búsqueda por director
lst_universo_director= list (movies_dataframe['director'].unique())
lst_universo_director.sort()
director_busq= st.sidebar.selectbox('Seleccionar director',lst_universo_director)
btn_buscar_director= st.sidebar.button ("Filtrar director")
if director_busq and btn_buscar_director:
  data_filtrada= load_data_bydirector (director_busq)
  count_row= data_filtrada.shape[0]  
  st.write (f"Número del filmes : {count_row}")
  st.dataframe (data_filtrada)
#=============================  

#Sidebar - nuevo filme
st.sidebar.subheader ("Nuevo filme")
name= st.sidebar.text_input("Nombre del filme")

lst_universo_compania= list (movies_dataframe['company'].unique())
lst_universo_compania.sort()
lst_universo_director= list (movies_dataframe['director'].unique())
lst_universo_director.sort()
lst_universo_genero= list (movies_dataframe['genre'].unique())
lst_universo_genero.sort()

company= st.sidebar.selectbox('Selecciona compañía', lst_universo_compania)
director= st.sidebar.selectbox('Selecciona director', lst_universo_director)
genre= st.sidebar.selectbox('Selecciona género', lst_universo_genero)
btn_nuevo_filme= st.sidebar.button ("Crear nuevo filme")

if name and company and director and genre and btn_nuevo_filme:
  doc_ref= db.collection ("movies").document(name)
  doc_ref.set({
      "name": name,
      "company": company,
      "director": director,
      "genre": genre
  })
  st.sidebar.write ("Registro insertado correctmente")
#=============================
