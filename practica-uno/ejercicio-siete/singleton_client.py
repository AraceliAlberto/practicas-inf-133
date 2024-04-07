import requests

url = "http://localhost:8000/"

print("\nLista de todas las partidas jugadas")
response = requests.get(url + "partidas")
print(response.text)

print("\nEmpezando a Jugar")
yo= {"elemento": "piedra"}
response = requests.post(url + "partidas", json=yo)
print(response.text)
print("--------------------------------")

# Obtener la lista de partidas ganadas
print("\nPartidas Ganadas")
response = requests.get(url + "partidas?resultado=gano")
print(response.text)
print("--------------------------------")

# Obtener la lista de partidas perdidas
print("\nPartidas Perdidas")
response = requests.get(url + "partidas?resultado=perdio")
print(response.text)
print("--------------------------------")

# Obtener la lista de partidas empatadas
print("\nPartidas Empatadas")
response = requests.get(url + "partidas?resultado=empate")
print(response.text)
print("--------------------------------")
