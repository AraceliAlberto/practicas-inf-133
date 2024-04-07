from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

mensajes = []

class MensajeService:
    @staticmethod
    def nuevo_mensaje(id):
        for mensaje in mensajes:
            if mensaje["id"] == id:
                return mensaje
        return None

    @staticmethod
    def encriptar_mensaje(mensaje):
        mensaje_encriptado = ""
        for letra in mensaje:
            if letra.isalpha():
                if letra in ['x', 'y', 'z']:
                    mensaje_encriptado += chr(ord('a') + ord(letra) - ord('x'))
                else:
                    mensaje_encriptado += chr(ord(letra) + 3)
            else:
                mensaje_encriptado += letra
        return mensaje_encriptado

    @staticmethod
    def añadir_mensaje(data):
        if not mensajes:
            data["id"] = 1
        else:
            ultimo_id = max(mensajes, key=lambda x: x["id"])["id"]
            data["id"] = ultimo_id + 1

        data["contenido_encriptado"] = MensajeService.encriptar_mensaje(data["contenido"])
        mensajes.append(data)
        return mensajes

    @staticmethod
    def actualizar_mensaje(id, data):
        mensaje = MensajeService.nuevo_mensaje(id)
        if mensaje:
            mensaje["contenido"] = data["contenido"]
            mensaje["contenido_encriptado"] = MensajeService.encriptar_mensaje(data["contenido"])
        return mensajes

    @staticmethod
    def eliminar_mensaje_id(id):
        mensaje = MensajeService.nuevo_mensaje(id)
        if mensaje:
            mensajes.remove(mensaje)
        return mensaje


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def read_data(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/mensajes":
            data = HTTPResponseHandler.read_data(self)
            mensajes = MensajeService.añadir_mensaje(data)
            HTTPResponseHandler.handle_response(self, 201, mensajes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        parametros_query = parse_qs(parsed_path.query)

        if self.path == "/mensajes":
            HTTPResponseHandler.handle_response(self, 200, mensajes)
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = MensajeService.nuevo_mensaje(id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, [mensaje])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.read_data(self)
            mensajes = MensajeService.actualizar_mensaje(id, data)
            if mensajes:
                HTTPResponseHandler.handle_response(self, 200, mensajes)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Mensaje no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = MensajeService.eliminar_mensaje_id(id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, mensaje)
            else:
                HTTPResponseHandler.handle_response(self, 404, "Mensaje no encontrado")
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
