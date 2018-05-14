import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#En este caso se quieren obtener datos de diez medicamentos distintos, por lo que se agrega limit=10(según como funciona la api )
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

for i in range(10):
#TRY:SE DISPONEN DE ESTA FORMA PARA QUE ,EN EL CASO DE QUE UNO DE LOS DATOS NO SE ENCUENTRE, EL PROGRAMA CONTINUE  EXTRAYENDO LOS DATOS
    try:
        print(i+1)
        print("ID del producto:",repos["results"][i]["id"])
    except KeyError:
        print("No se encontraron resultados")
    try:
        print("Nombre de la fabricante:",repos["results"][i]["openfda"]["manufacturer_name"][0])
    except KeyError:
        print("No se encontraron resultados")
    try:
        print("Propósito:",repos["results"][i]["purpose"][0],"\n")
    except KeyError:
        print("No se encontraron resultados")
        continue
