from http.server import HTTPServer,BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

list_pacientes = {}

class Paciente:
    def __init__(self, builder = None):
        if builder is not None:
            self.CI = builder.ci
            self.Nombre = builder.nombre
            self.Apellido = builder.apellido
            self.Edad = builder.edad
            self.Genero = builder.genero
            self.Diagnostico = builder.diagnostico
            self.Doctor = builder.doctor
        else:
            self.CI = None
            self.Nombre = None
            self.Apellido = None
            self.Edad = None
            self.Genero = None
            self.Diagnostico = None
            self.Doctor = None

    def __str__(self):
        return f"CI: {self.CI}, Nombre: {self.Nombre}, Apellido: {self.Apellido}, Edad: {self.Edad}, Género: {self.Genero}, Diagnóstico: {self.Diagnostico}, Doctor: {self.Doctor}"
    
class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()

    def set_ci(self, ci):
        self.paciente.ci = ci
        
    def set_nombre(self, nombre):
        self.paciente.nombre = nombre
        
    def set_apellido(self, apellido):
        self.paciente.apellido = apellido
        
    def set_edad(self, edad):
        self.paciente.edad = edad
        
    def set_genero(self, genero):
        self.paciente.genero = genero
        
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico

    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def build(self):
        return self.paciente

class Persona:
    def __init__(self, builder):
        self.builder = builder

    def crear_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()
    
class PacienteService(BaseHTTPRequestHandler):
    def __init__(self):
        self.builder = PacienteBuilder()
        self.Persona = Persona(self.builder)
    
    def crear_paciente(self, data):
        paciente = Paciente()
        paciente.ci = data['ci'] if 'ci' in data else None
        paciente.nombre = data['nombre'] if 'nombre' in data else None
        paciente.apellido = data['apellido'] if 'apellido' in data else None
        paciente.edad = data['edad'] if 'edad' in data else None
        paciente.genero = data['genero'] if 'genero' in data else None
        paciente.diagnostico = data['diagnostico'] if 'diagnostico' in data else None
        paciente.doctor = data['doctor'] if 'doctor' in data else None

        list_pacientes.append(paciente.__dict__)
    
    def actualizar_paciente(CI, data):
        paciente = PacienteService.buscar_paciente(CI)
        if paciente:
            paciente.update(data)
            return list_pacientes
        else:
            return None
    
    def buscar_paciente(self, CI):
        paciente_encontrado = None
        for encontrado in list_pacientes:
            if encontrado["CI"] == CI:
                paciente_encontrado = encontrado
                break
        return paciente_encontrado
    
    def buscar_diagnostico(self, Diagnostico):
        pacientes_con_diagnostico = []
        for paciente in list_pacientes:
            if paciente["Diagnostico"] == Diagnostico:
                pacientes_con_diagnostico.append(paciente)
        return pacientes_con_diagnostico
    
    def buscar_atendido_por_doctor(self, Doctor):
        pacientes_atendidos = []
        for paciente in list_pacientes:
            if paciente["Doctor"] == Doctor:
                pacientes_atendidos.append(paciente)
        return pacientes_atendidos
    
    def eliminar_paciente(self, CI):
        paciente = PacienteService.buscar_paciente(CI)
        if paciente:
            list_pacientes.remove(paciente)
            return list_pacientes
        else:
            return None
        
class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))
    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))

class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=PacienteService()
        super().__init__(*args,**kwargs)

    def do_POST(self):
        if self.path == '/pacientes':
            data = HTTPResponseHandler.read_data(self)
            builder = PacienteBuilder()
            builder.set_ci(data.get('Ci', None))
            builder.set_nombre(data.get('Nombre', None))
            builder.set_apellido(data.get('Apellido', None))
            builder.set_edad(data.get('Edad', None))
            builder.set_genero(data.get('Genero', None))
            builder.set_diagnostico(data.get('Diagnostico', None))
            builder.set_doctor(data.get('Doctor', None))
            paciente = builder.build()
            self.controller.crear_paciente(paciente)
            HTTPResponseHandler.handle_response(self, 201, paciente.__dict__)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no encontrada"})

    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes/":
            if "diagnostico" in query_params:
                diagnostico=query_params['diagnostico'][0]
                paciente_diag=self.controller.buscar_diagnostico(diagnostico)
                if paciente_diag:
                    HTTPResponseHandler.handle_response(self,200,paciente_diag)
                else:
                    HTTPResponseHandler.handle_response(self,404,{"Error":"Diagnostico no encontrado"})
            
            elif "Doctor" in query_params:
                doctor = query_params["Doctor"][0]
                pacientes_doctor = self.controller.buscar_atendido_por_doctor(doctor)
                if pacientes_doctor:
                    HTTPResponseHandler.handle_response(self, 200, pacientes_doctor)
                else:
                    HTTPResponseHandler.handle_response(self, 404, {"Error": "No se encontraron pacientes atendidos por el doctor especificado"})
            else:    
                HTTPResponseHandler.handle_response(self,200,)
        elif parsed_path.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            paciente_ci=self.controller.buscar_diagnostico(ci)
            if paciente_ci:
                HTTPResponseHandler.handle_response(self,200,paciente_ci)
            else:
                HTTPResponseHandler.handle_response(self,404,{"Error":"Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self,404,{"Error":"Ruta no encontrada"})
    
    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            CI = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.read_data(self)
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

def run(server_class=HTTPServer, handler_class=PacienteBuilder, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=PacienteHandler)
