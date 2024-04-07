from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Paciente:
    list_pacientes = [
        {
            "CI": 10061725,
            "Nombre": "Harold",
            "Apellido": "Chipana",
            "Edad": 21,
            "Genero": "Masculino",
            "Diagnostico": "Diabetes",
            "Doctor": "Pedro Perez",
        },

        {
            "CI":10065864,
            "Nombre": "Araceli",
            "Apellido": "Alberto",
            "Edad": 20,
            "Genero": "Femenino",
            "Diagnostico": "Resfriado",
            "Doctor": "Pedro Perez",
        },
    ]

class PacienteService:
    # =====> Creando Paciente <=====
    @staticmethod
    def crear_paciente(data):
        paciente_nuevo = {
            "CI": data.get("CI"),
            "Nombre": data.get("Nombre"),
            "Apellido": data.get("Apellido"),
            "Edad": data.get("Edad"),
            "Genero": data.get("Genero"),
            "Diagnostico":data.get("Diagnostico"),
            "Doctor": data.get("Doctor"),
        }
        Paciente.list_pacientes.append(paciente_nuevo)
        return Paciente.list_pacientes

    # =====> Actualizando Paciente <=====
    @staticmethod
    def actualizar_paciente(CI, data):
        paciente = PacienteService.buscar_paciente(CI)
        if paciente:
            paciente.update(data)
            return Paciente.list_pacientes
        else:
            return None
    
    # =====> Buscar Paciente <=====
    @staticmethod
    def buscar_paciente(CI):
        paciente_encontrado = None
        for encontrado in Paciente.list_pacientes:
            if encontrado["CI"] == CI:
                paciente_encontrado = encontrado
                break
        return paciente_encontrado
    
     # =====> Buscar Diagnostico <=====
    @staticmethod
    def buscar_diagnostico(Diagnostico):
        pacientes_con_diagnostico = []
        for paciente in Paciente.list_pacientes:
            if paciente["Diagnostico"] == Diagnostico:
                pacientes_con_diagnostico.append(paciente)
        return pacientes_con_diagnostico
    
     # =====> Buscar a quien atendio el Doctor <=====
    @staticmethod
    def buscar_atendido_por_doctor(Doctor):
        pacientes_atendidos = []
        for paciente in Paciente.list_pacientes:
            if paciente["Doctor"] == Doctor:
                pacientes_atendidos.append(paciente)
        return pacientes_atendidos

    # =====> Eliminar Paciente <=====
    @staticmethod
    def eliminar_paciente(CI):
        paciente = PacienteService.buscar_paciente(CI)
        if paciente:
            Paciente.list_pacientes.remove(paciente)
            return Paciente.list_pacientes
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
        if self.path == "/pacientes":
            data = self.read_data()
            nuevo_paciente = PacienteService.crear_paciente(data)[-1]
            HTTPResponseHandler.handle_response(self, 201, nuevo_paciente)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
#--------------------------------------
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if self.path == "/pacientes":
            listaPacientes = Paciente.list_pacientes
            HTTPResponseHandler.handle_response(self, 201, listaPacientes)

        elif self.path.startswith("/paciente/"):
            ci = parsed_path.path.split("/")[-1]
            paciente_ci = PacienteService.buscar_paciente(int(ci))
            if paciente_ci:
                HTTPResponseHandler.handle_response(self, 200, paciente_ci)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        
        elif parsed_path.path == "/pacientes/":
            if "Diagnostico" in query_params:
                diagnostico = query_params["Diagnostico"][0]
                conDiagnostico = PacienteService.buscar_diagnostico(diagnostico)
                if conDiagnostico != []:
                    HTTPResponseHandler.handle_response(self, 200, conDiagnostico)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])

            elif "Doctor" in query_params:
                doctor = query_params["Doctor"][0]
                pacientes_doctor = PacienteService.buscar_atendido_por_doctor(doctor)
                if pacientes_doctor:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_doctor)
                else:
                    HTTPResponseHandler.handle_response(self, 404, {"Error": "No se encontraron pacientes atendidos por el doctor especificado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

#--------------------------------------
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            data = self.read_data()
            paciente = PacienteService.actualizar_paciente(CI,data)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente)
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
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            paciente_eliminado = PacienteService.eliminar_paciente(CI)
            if paciente_eliminado:
                HTTPResponseHandler.handle_response(self, 200, paciente_eliminado)
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
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()