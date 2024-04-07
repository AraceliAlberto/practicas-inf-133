from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse, parse_qs

class JuegoSingleton:
    _instance = None

    def __new__(cls, name):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            cls._instance.partidas = []
            cls._instance.elementos = ["piedra", "papel", "tijera"]
        return cls._instance

    def iniciar_partida(self, elemento_jugador):
        elemento_servidor = random.choice(self.elementos)
        resultado = self.calcular_resultado(elemento_jugador, elemento_servidor)
        partida = {
            "id": len(self.partidas) + 1,
            "elemento_jugador": elemento_jugador,
            "elemento_servidor": elemento_servidor,
            "resultado": resultado
        }
        self.partidas.append(partida)
        return partida

    def calcular_resultado(self, elemento_jugador, elemento_servidor):
        if elemento_jugador == elemento_servidor:
            return "empate"
        elif (
            (elemento_jugador == "piedra" and elemento_servidor == "tijera") or
            (elemento_jugador == "papel" and elemento_servidor == "piedra") or
            (elemento_jugador == "tijera" and elemento_servidor == "papel")
        ):
            return "gano"
        else:
            return "perdio"

    def obtener_partidas(self, resultado=None):
        if resultado:
            return [partida for partida in self.partidas if partida["resultado"] == resultado]
        else:
            return self.partidas

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class JuegoRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partidas":
            data = self.read_data()
            elemento_jugador = data["elemento"]
            partida = juego.iniciar_partida(elemento_jugador)
            HTTPResponseHandler.handle_response(self, 201, partida)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if self.path == "/partidas":
            partidas = juego.obtener_partidas()
            HTTPResponseHandler.handle_response(self, 200, partidas)
        elif "resultado" in query_params:
            resultado = query_params["resultado"][0]
            partidas = juego.obtener_partidas(resultado)
            if partidas:
                HTTPResponseHandler.handle_response(self, 200, partidas)
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
def run_server(port=8000):
    global juego
    juego = JuegoSingleton("Piedra, Papel o Tijera")
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, JuegoRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()