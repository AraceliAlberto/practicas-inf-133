import requests

url = "http://localhost:8000/"

# ============> Crear Paciente <============
print("---> Agregado Paciente....")
ruta_post = url + "pacientes"
nuevo_paciente= {
    "CI": 1006511,
    "Nombre": "Nicolls",
    "Apellido": "Torrez",
    "Edad": 25,
    "Genero": "Masculino",
    "Diagnostico": "Depresion",
    "Doctor": "Marcela Hidalgo",
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)
#------------------------------------------------

# ============> Listar a los pacientes <============
print("\n---> Listado de Pacientes:")
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#---------------------------------------------------

# ============> Paciente con CI <============
print("\n---> El paciente con CI:")
ruta_get = url + "paciente/10065864"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#------------------------------------------------

# ============> Listar a los pacientes con Diabetes<============
print("\n---> Paciente con Diagnostico (Diabetes):")
ruta_get = url + "pacientes/?Diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#------------------------------------------------

# ============> Listar a los pacientes que atiende el Doctor Pedro Pérez <============
print("\n---> El Doctor Pedro Perez atiende a:")
ruta_get = url + "pacientes/?Doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#------------------------------------------------

# ============> Actualizar a los pacientes <============
print("\n---> Listado de Pacientes Modificado:")
ruta_actualizar = url + "pacientes/10061725"
paciente_actualizado = {
    "Edad": 22,
    "Diagnostico": "Bilis",
    "Doctor": "Marcela Hidalgo",
}
put_response = requests.request(method="PUT", url=ruta_actualizar, json=paciente_actualizado)
print(put_response.text)
#------------------------------------------------

# ============> Elimina a paciente <============
print("\n---> Listado de Pacientes despues de Eliminar:")
ruta_eliminar = url + "pacientes/10065864"
delete_response = requests.request(method="DELETE", url=ruta_eliminar)
print("Eliminando a CI: 100065864..........")
print(delete_response.text)
#------------------------------------------------
