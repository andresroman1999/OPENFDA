import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
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
###EN ESTE CASO, LA BÚSQUEDA SE AMPLÍA(+active_ingredient:aspirin)

import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic+active_ingredient:aspirin&limit=100", None, headers)
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

