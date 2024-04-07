from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

list_zoologico = [
    {
        "ID": 1,
        "Nombre": "Andes",
        "Especie": "Oso Andino",
        "Genero": "Macho",
        "Edad": 6,
        "Peso": 120,
    },
    {
        "ID": 2,
        "Nombre": "Luna",
        "Especie": "Jaguar",
        "Genero": "Hembra",
        "Edad": 5,
        "Peso": 70,
    },
]

class ZoologicoService:
    # =====> Creando Animal <=====
    @staticmethod
    def crear_animal(data):
       data["ID"] = len(list_zoologico) + 1
       animal_nuevo = {
           "ID": data.get("ID"),
            "Nombre": data.get("Nombre"),
            "Especie": data.get("Especie"),
            "Genero": data.get("Genero"),
            "Edad": data.get("Edad"),
            "Peso": data.get("Peso"),
        }
       list_zoologico.append(animal_nuevo)
       return list_zoologico
    
    # =====> Buscar Animal <=====
    @staticmethod
    def buscar_animal(ID):
        animal_encontrado = None
        for encontrado in list_zoologico:
            if encontrado["ID"] == ID:
                animal_encontrado = encontrado
                break
        return animal_encontrado
    
    # =====> Buscar Especie <=====
    @staticmethod
    def buscar_especie(Especie):
        animales_de_especie = []
        for animal in list_zoologico:
            if animal["Especie"] == Especie:
                animales_de_especie.append(animal)
        return animales_de_especie
    
    # =====> Buscar Genero <=====
    @staticmethod
    def buscar_genero(Genero):
        animales_de_genero = []
        for animal in list_zoologico:
            if animal["Genero"] == Genero:
                animales_de_genero.append(animal)
        return animales_de_genero
    
    # =====> Actualizando Animal <=====
    @staticmethod
    def actualizar_animal(ID, data):
        animal = ZoologicoService.buscar_animal(ID)
        if animal:
            animal.update(data)
            return list_zoologico
        else:
            return None
        
    # =====> Eliminar animal <=====
    @staticmethod
    def eliminar_animal(ID):
        animal = ZoologicoService.buscar_animal(ID)
        if animal:
            list_zoologico.remove(animal)
            return list_zoologico
        else:
            return None
    
#---------------------------- 
class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
#----------------------------

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            nuevo_animal = ZoologicoService.crear_animal(data)[-1]
            HTTPResponseHandler.handle_response(self, 201, nuevo_animal)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
#--------------------------------------
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if self.path == "/animales":
            todos_los_pacientes = list_zoologico
            HTTPResponseHandler.handle_response(self, 200, todos_los_pacientes)
        elif parsed_path.path == "/animales":
            if "Especie" in query_params:
                especie = query_params["Especie"][0]
                deEspecie = ZoologicoService.buscar_especie(especie)
                if deEspecie != []:
                    HTTPResponseHandler.handle_response(self, 200, deEspecie)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])

        elif parsed_path.path == "/animales/":         
            if "Genero" in query_params:
                genero = query_params["Genero"][0]
                deGenero = ZoologicoService.buscar_genero(genero)
                if deGenero != []:
                    HTTPResponseHandler.handle_response(self, 200, deGenero)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

#--------------------------------------
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            ID = int(self.path.split("/")[-1])
            data = self.read_data()
            animal = ZoologicoService.actualizar_animal(ID,data)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
#--------------------------------------
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            ID = int(self.path.split("/")[-1])
            animal_eliminado = ZoologicoService.eliminar_animal(ID)
            if animal_eliminado:
                HTTPResponseHandler.handle_response(self, 200, animal_eliminado)
            else:
                HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
#--------------------------------------

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()