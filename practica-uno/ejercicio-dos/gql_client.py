import requests

url = 'http://localhost:8000/graphql'

# =========> Listar plantas <=========
query_listar_plantas = """
{
    plantas {
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

print("Lista plantas: \n")
response = requests.post(url, json={'query': query_listar_plantas})
print(response.text)
#-----------------------------------------------

# =========> Buscando por especie <=========
query_buscar_por_especie = """
{
    plantasPorEspecie(especie: "Lavandula") {
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

print("\nBuscando por Especie: \n")
response_especie = requests.post(url, json={'query': query_buscar_por_especie})
print(response_especie.text)

# =========> Buscando plantas con frutos <=========
query_plantas_con_frutos = """
{
    plantasConFrutos {
        id
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""

print("\nBuscando plantas CON frutos: \n")
response_frutos = requests.post(url, json={'query': query_plantas_con_frutos})
print(response_frutos.text)

# =========> Agregar nueva planta <=========
query_crear_planta = """
mutation {
        crearNuevaPlanta(
            nombre:"Naranja",
            especie: "Citrus sinensis",
            edad: 48,
            altura: 250,
            frutos: true
            ){
            planta{
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_crear_planta})
print("\nCreando nueva planta.......")
print(response_mutation.text)

print("\nLista plantas con la creacion de nueva planta:")
response = requests.post(url, json={'query': query_listar_plantas})
print(response.text)

# =========> Eliminar una Planta <=========
query_eliminar_planta = """
mutation {
        eliminarUnaPlanta(id:1){
            planta{
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation_eliminar = requests.post(url, json={'query': query_eliminar_planta})
print("\nEliminando una Planta.......")
print(response_mutation_eliminar.text)

print("\nLista de plantas con la eliminacion de una planta:")
response = requests.post(url, json={'query': query_listar_plantas})
print(response.text)

# =========> Actualizar una Planta <=========
query_actualizar_planta = """
mutation {
        crearNuevaPlanta(
            nombre:"Naranja",
            especie: "Citrus sinensis",
            edad: 96,
            altura: 350,
            frutos: false
            ){
            planta{
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation_actualizar = requests.post(url, json={'query': query_actualizar_planta})
print("\nActualizando una Planta.......")
print(response_mutation_actualizar.text)

print("\nLista de plantas con la actualizacion de una planta:")
response = requests.post(url, json={'query': query_listar_plantas})
print(response.text)