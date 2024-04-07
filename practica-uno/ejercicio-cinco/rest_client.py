import requests

url = "http://localhost:8000/"

# ============> Crear Animal <============
print("---> Agregado Animal....")
ruta_post = url + "animales"
nuevo_animal= {
    "Nombre": "Sol",
    "Especie": "Llama",
    "Genero": "Hembra",
    "Edad": 5,
    "Peso": 100,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print(post_response.text)

# ============> Listar a todos los animales <============
print("\n---> Listado de los Animales:")
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#---------------------------------------------------

# ============> Listar a los animales de Especie <============
print("\n---> Animal de especie (Oso Andino):")
ruta_get = url + "animales?Especie=Oso Andino"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#------------------------------------------------

# ============> Listar a los animales de Genero <============
print("\n---> Animal de Genero (Hembra):")
ruta_get = url + "animales/?Genero=Hembra"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#------------------------------------------------

# ============> Actualizar a los animales <============
print("\n---> Listado de animales Modificado:")
ruta_actualizar = url + "animales/2"
animal_actualizado = {
    "Edad": 6,
    "Peso": 80,
}
put_response = requests.request(method="PUT", url=ruta_actualizar, json=animal_actualizado)
print(put_response.text)
#------------------------------------------------

# ============> Elimina a un Animal <============
print("\n---> Listado de animales despues de Eliminar:")
ruta_eliminar = url + "animales/1"
delete_response = requests.request(method="DELETE", url=ruta_eliminar)
print("Eliminando a ID: 1 .........")
print(delete_response.text)
#------------------------------------------------
