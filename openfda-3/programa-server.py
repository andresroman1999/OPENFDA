import socketserver
import http.client
import json
import http.server
puerto=8001

headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=11", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repos = json.loads(repos_raw)
num=len(repos["results"])
datos=[]
##De forma similar al erjercicio anterior se extraen los datos necesarios y se añaden a una lista
for x in range(num):
    results=repos["results"][x]
    ##Se verifica la existencia de la carpeta openfda, pues en el caso de algunos medicamentos no existe.
    if results["openfda"]:
        datos.append(results["openfda"]["manufacturer_name"][0])

######################################################################
#Se crea esta clase que con la funcion do_GET hará que el servidor soporte este tipo de peticiones.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type","text/html")
        self.end_headers()
#Para que se imprima de forma correcta por panatlla, conforme se sacan los datosde la lista se añaden las terminaciones necesarias.
#Asi en la variable cuerpo queda recogida la info en html
        cuerpo="<html><body>"
        for fabricante in datos:
           cuerpo += fabricante+"<br>"
        cuerpo +="</body></html>"
        self.wfile.write(bytes(cuerpo, "utf8"))
        return
#####################################################################
handler= testHTTPRequestHandler
HTTPD = socketserver.TCPServer(("",puerto),handler)
try:
    print("Servidor activado...")
    HTTPD.serve_forever()
except KeyboardInterrupt:
    print("servidor cerrado")
    HTTPD.server_close()
