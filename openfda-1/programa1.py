import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
#print(repos)
print("ID del producto:",repos["results"][0]["id"],"\n"+"Nombre de la fabricante:",repos["results"][0]["openfda"]["manufacturer_name"][0],"\n"+"Propósito:",repos["results"][0]["purpose"][0])
