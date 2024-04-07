import requests
import json

# URL del servidor de mensajes
url = "http://localhost:8000/mensajes"

# Crear un mensaje
nuevo_mensaje = {
    "id": 1,
    "contenido": "Hola, mundo!"
}
response = requests.post(url, json=nuevo_mensaje)
print("Respuesta de creación de mensaje:", response.status_code)
print("Mensaje creado:", response.json())

# Obtener todos los mensajes
response = requests.get(url)
print("Respuesta de obtener todos los mensajes:", response.status_code)
print("Todos los mensajes:", response.json())

# Obtener un mensaje por ID
id_mensaje = 1
get_url = f"{url}/{id_mensaje}"
response = requests.get(get_url)
print(f"Respuesta de obtener el mensaje con ID {id_mensaje}:", response.status_code)
print("Mensaje obtenido:", response.json())

# Actualizar un mensaje por ID
id_mensaje = 1
update_data = {
    "contenido": "¡Hola, mundo actualizado!"
}
update_url = f"{url}/{id_mensaje}"
response = requests.put(update_url, json=update_data)
print(f"Respuesta de actualizar el mensaje con ID {id_mensaje}:", response.status_code)
print("Mensaje actualizado:", response.json())

# Eliminar un mensaje por ID
id_mensaje = 1
delete_url = f"{url}/{id_mensaje}"
response = requests.delete(delete_url)
print(f"Respuesta de eliminar el mensaje con ID {id_mensaje}:", response.status_code)
print("Mensaje eliminado:", response.json())
