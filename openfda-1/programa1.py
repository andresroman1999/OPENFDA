import http.client
import json
#En las lineas siguientes se recogen los datos necesarios (de forma smilar a ejercicios anteriores) para acceder a la api de OPENFDA.
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")

conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
#repos es la variable que recoge los datos obtenidos de la web
repos = json.loads(repos_raw)
#Dado que estos datos estan clasificados en listas en diccionarios se acederá a ellos en funcion de las valores que queramos obtener.
print("ID del producto:",repos["results"][0]["id"],"\n"+"Nombre de la fabricante:",repos["results"][0]["openfda"]["manufacturer_name"][0],"\n"+"Propósito:",repos["results"][0]["purpose"][0])
