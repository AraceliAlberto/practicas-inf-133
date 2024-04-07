from zeep import Client

client = Client('http://localhost:8000/')

suma = client.service.Sumar(a=4, b=6)
print(suma)

resta = client.service.Restar(a=8, b=5)
print(resta)

multiplicacion = client.service.Multiplicar(a=4, b=2)
print(multiplicacion)

division = client.service.Division(a=10, b=2)
print(division)
