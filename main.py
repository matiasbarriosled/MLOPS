from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
import pandas as pd
import random

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    principal= """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Movies</title>
    <style>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    </style>
</head>
<style>

  body{
    background-color:yellow
  }

</style>
<body>
  <h1>Hola Mundo!!!</h1>
  <h6>En este espacio lo voy a rellenar con cosas... cuales no se aun</h6>
  <p>
  credula postero dolo asit quasi men parabellum nome nomelorem ipsum dolo asit quasi men parabellum nome nome deje quan mininum credula postero dolo asit quasi men parabellum nome nome deje
  asit quasi men parabellum nome nome deje lorem ipsum dolo asit quasi men parabellum nome nome deje quan mininum credula postero dolo asit quasi men parabellum nome nome deje
  lorem ipsum dolo asit quasi men parabellum men parabellum nome nome deje quan mininum credula postero dolo a parabellum nome nome deje
  lorem ipsum dolo asit quasi men parabellum nome nome deje quan mininum credula postero dolo asit quasi men parabellum nome nome deje</p>
  men parabellum nome nome deje quan mininum credula postero dolo alorem ipsum dolo asit quasi men parabellum nome nome deje quan mininum credula postero dolo asit quasi men parabellum nome nome deje
  lorem ipsum dolo asit quasi men parabellum nome nome deje quan mininum credula postero dolo asit quasi men parabellum nome nome deje
   dolo asit quasi men parabellum nome nome deje dolo asit quasi men parabellum nome nome deje dolo asit quasi men parabellum nome nome deje
  <div class=""><a href="https://pi1-mlops-vv02.onrender.com/docs" target="_blank"> #SoyHenry </a></div>
  <br>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>


        """    
    return principal

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    """def cantidad_filmaciones_mes( Mes ): Se ingresa un mes en idioma Español.
    Debe devolver la cantidad de películas que fueron estrenadas en el mes 
    consultado en la totalidad del dataset:
        Ejemplo de retorno: X cantidad de películas fueron estrenadas en el mes de X"""
    
    peliculas = pd.read_parquet("consultas/movies.parquet")
    mes_input = mes.capitalize()
    cant = peliculas['mes'].value_counts()[mes_input]
    return f"en el mes de {mes_input} fueron estrenadas {int(cant)} películas"


@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    """def cantidad_filmaciones_dia( Dia ): Se ingresa un día en idioma Español. 
    Debe devolver la cantidad de películas que fueron estrenadas en día 
    consultado en la totalidad del dataset:
        Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X"""
    
    peliculas = pd.read_parquet("consultas/movies.parquet")
    dia_input = dia.capitalize()
    cant = peliculas['dia_semana'].value_counts()[dia_input]
    return f"Los dias {dia_input} se estrenaron {int(cant)} películas"


@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    """def score_titulo( titulo_de_la_filmación ): Se ingresa el título de una 
    filmación esperando como respuesta el título, el año de estreno y el score.
        Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X"""
    
    peliculas = pd.read_parquet("consultas/movies.parquet")
    titulo_input = titulo.lower()
    busqueda = peliculas[peliculas['title'].str.lower()==titulo_input]
    if busqueda.empty:
        def busquedas_anidadas(lista):
            return ', '.join(map(str,lista))
        posible_busqueda = peliculas[peliculas['title'].str.lower().str.contains(titulo_input)]
        coincidencias = int(posible_busqueda.shape[0])
        lista_titulos = list(posible_busqueda['title'])
        return f"tu busqueda obtuvo {coincidencias} coincidencias: {busquedas_anidadas(lista_titulos)}"
    titulo = str(busqueda['title'].values[0])
    anio = int(busqueda['anio'].values[0])
    score = float(busqueda['popularity'].values[0])
    return f" el titulo {titulo} se estreno el año {anio} y hasta el dia de hoy tiene un score de {score}"


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    """def votos_titulo( titulo_de_la_filmación ): Se ingresa el título de una 
    filmación esperando como respuesta el título, la cantidad de votos y el 
    valor promedio de las votaciones. La misma variable deberá de contar con 
    al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje 
    avisando que no cumple esta condición y que por ende, no se devuelve ningun valor:
        Ejemplo de retorno: La película X fue estrenada en el año X. La misma cuenta
        con un total de X valoraciones, con un promedio de X"""
    
    peliculas = pd.read_parquet("consultas/movies.parquet")
    titulo_input = titulo.lower()
    busqueda = peliculas[peliculas['title'].str.lower()==titulo_input]

    def busquedas_anidadas(lista):
            return ', '.join(map(str,lista))
    if busqueda.empty:
        posible_busqueda = peliculas[peliculas['title'].str.lower().str.contains(titulo_input)]
        coincidencias = int(posible_busqueda.shape[0])
        lista_titulos = list(posible_busqueda['title'])
        return f"tu busqueda obtuvo {coincidencias} coincidencias: {busquedas_anidadas(lista_titulos)}"


    elif int(busqueda['vote_count'].values[0])>2000:
        cantidad_votos = int(busqueda['vote_count'].values[0])
        titulo = str(busqueda['title'].values[0])
        promedio_votos = float(busqueda['vote_average'].values[0])
        return f" el titulo {titulo} tiene en total {cantidad_votos} votos con un promedio de {promedio_votos}"
    else:
        sugerencias = peliculas[peliculas['vote_count']>2000]
        sugerencias = list(sugerencias['title'])
        sugerencias_random = random.sample(sugerencias,3)
        return f"Su busqueda no cumple con las condiciones, no hay valores a devolver. Aqui algunas sugerencias que cumplen con los requisitos: {busquedas_anidadas(sugerencias_random)}"


@app.get('/nombre_actor/{actor}')
def nombre_actor(actor: str):
    """def get_actor( nombre_actor ): Se ingresa el nombre de un actor que se 
    encuentre dentro de un dataset debiendo devolver el éxito del mismo medido 
    a través del retorno. Además, la cantidad de películas que en las que ha 
    participado y el promedio de retorno. La definición no deberá considerar directores:
        Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones, el 
        mismo ha conseguido un retorno de X con un promedio de X por filmación"""
    
    actores = pd.read_parquet("consultas/actores.parquet")
    if actor in actores.name.values:
        peliculas = pd.read_parquet("consultas/movies.parquet")
        actores = actores.loc[actores.name == actor]
        suma = actores.shape[0]
        lista_peliculas = list(actores.id_pelicula)
        peliculas = peliculas[peliculas.id.isin(lista_peliculas)]
        retorno = "{:.2f}".format(peliculas.retorno.sum())
        promedio = "{:.2f}".format(peliculas.retorno.mean())
        return f"El actor {actor} a participado en {suma} peliculas, de las cuales ha obtenido {retorno} de retorno total, dando un promedio de {promedio} con todas las peliculas"
    else:
        return f"no se encontro resultados con el nombre: {actor}"


@app.get('/nombre_director/{director}')
def nombre_director(director: str):
    """def get_director( nombre_director ): Se ingresa el nombre de un director 
    que se encuentre dentro de un dataset debiendo devolver el éxito del mismo 
    medido a través del retorno. Además, deberá devolver el nombre de cada 
    película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma."""

    return None