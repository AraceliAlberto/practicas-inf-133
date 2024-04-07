from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation

class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()

list_plantas = [
    Planta(
        id=1, nombre = "Fresa", especie = "Fragaria x ananassa", edad=5, altura=10, frutos=True
    ),
    Planta(
        id=2, nombre = "Lavanda", especie = "Lavandula", edad=6, altura=30, frutos=False
    ),
]

class Query(ObjectType):
    #======> Listar plantas
    plantas = List(Planta)

    def resolve_plantas(root, info):
        return list_plantas
    
    #======> Buscar plantas por especie
    plantas_por_especie = List(Planta, especie=String())

    def resolve_plantas_por_especie(root, info, especie):
        encontrado = []
        for i in list_plantas:
            if i.especie == especie:
                encontrado.append(i)
        return encontrado

    #======> Buscar las plantas que tienen frutos
    plantas_con_frutos = List(Planta, frutos=Boolean())

    def resolve_plantas_con_frutos(root, info):
        conFrutos = []
        for i in list_plantas:
            if i.frutos == True:
                conFrutos.append(i)
        return conFrutos
    
#========> MUTATION <=============
#==> Crear
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, frutos):
        nueva_planta = Planta(
            id = len(list_plantas)+1,
            nombre = nombre,
            especie = especie,
            edad = edad,
            altura = altura,
            frutos = frutos
        )
        list_plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)
    
# ==> Eliminar
class EliminarPlanta(Mutation):
    class Arguments:
        id = Int()
    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(list_plantas):
            if planta.id == id:
                list_plantas.pop(i)
                return EliminarPlanta(planta=planta)
        return None

# ==> Actualizar
class ActualizarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()
    planta = Field(Planta)

    def mutate(root, info, id, nombre, especie, edad, altura, frutos):
        for i, planta in enumerate(list_plantas):
            if(planta.id == id):
                planta.nombre = nombre
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.frutos = frutos
                return ActualizarPlanta(planta=planta)
        return None

#--------------------------------------------
class Mutations(ObjectType):
    crear_nueva_planta = CrearPlanta.Field()
    eliminar_una_planta = EliminarPlanta.Field()
    actualizar_la_planta = ActualizarPlanta.Field()
#--------------------------------------------

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()