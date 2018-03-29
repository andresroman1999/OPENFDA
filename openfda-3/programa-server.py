import socketserver
import http.client
import json
import http.server
puerto=8001

headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repos = json.loads(repos_raw)
num=len(repos["results"])
datos=[]
for x in range(num):
    results=repos["results"][x]
    if results["openfda"]:
        datos.append(results["openfda"]["manufacturer_name"][0])

######################################################################
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type","text/html")
        self.end_headers()
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