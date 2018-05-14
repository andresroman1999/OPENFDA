import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#Añadiendo de forma adecuada active_ingredient:acetylsalicylic&limit=100 en la url se obtienen resultados en los que clave y valor coincidan.
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
#Los datos se añaden a una lista vacia(fab) de la que luego se extraerán para evitar que los nombres de os fabricantes salgan repetidos por pantalla
num=len(repos["results"])
fab=[]
try :
    for i in range(num):
        fab.append(repos["results"][i]["openfda"]["manufacturer_name"][0])
except KeyError:
        fab.append("FABRICANTE DESCONOCIDO")
print("Los fabricantes son:")
for i in set(fab):
    print(i)


#############################################################################################################################################
print("###")
#############################################################################################################################################
###EN ESTE CASO, LA BÚSQUEDA SE AMPLÍA(+substance_name:aspirin)
##

import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#####
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic+substance_name:aspirin&limit=100&skip=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
num=len(repos["results"])
fab2=[]
try :
    for i in range(num):
        fab2.append(repos["results"][i]["openfda"]["manufacturer_name"][0])
except KeyError:
        fab2.append("FABRICANTE DESCONOCIDO")
print("Los fabricantes son:")
for i in set(fab2):
    print(i)

