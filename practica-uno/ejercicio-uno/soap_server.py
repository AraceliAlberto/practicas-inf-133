from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler


def sumar(a,b):
    return "la suma es {}".format(a+b)

def resta(a,b):
    return "la resta es {}".format(a-b)

def multiplicar(a,b):
    return "la multiplicacion es {}".format(a*b)

def division(a,b):
    return "la division es {}".format(a/b)

dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Sumar",
    sumar,
    returns={"suma":str},
    args={"a":int, "b": int}
)

dispatcher.register_function(
    "Restar",
    resta,
    returns={"Resta":str},
    args={"a":int, "b": int}
)

dispatcher.register_function(
    "Multiplicar",
    multiplicar,
    returns={"multiplicar":str},
    args={"a":int, "b": int}
)

dispatcher.register_function(
    "Division",
    division,
    returns={"division":str},
    args={"a":int, "b": int}
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()