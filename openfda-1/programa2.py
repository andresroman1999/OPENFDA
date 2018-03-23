import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
#print(repos)
for i in repos["results"]:
    print("ID del producto:",repos["results"][i]["id"],"\n"+"Nombre de la fabricante:",repos["results"][i]["openfda"]["manufacturer_name"][0],"\n"+"Propósito:",repos["results"][i]["purpose"][0])
