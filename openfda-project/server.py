
import http.server
import http.client
import json
import socketserver
PORT=8000
########################################################################################################################
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    ofda_api_url="api.fda.gov"
    ofda_api_evento="/drug/label.json"
    ofda_api_drug='&search=active_ingredient:'
    ofda_api_comp='&search=openfda.manufacturer_name:'


    def get_pag_principal(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                 <body style='background-color: red'>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html
    def devuelve_web (self, lista):
        list_html = """
                            <html>
                                <head>
                                    <title>OpenFDA Cool App</title>
                                </head>
                                <body style='background-color: pink'>
                                    <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                    </ul>
                                </body>
                            </html>
                        """
        return list_html
    def devuelve_resultados_genericos (self, limit=10):

        conn = http.client.HTTPSConnection(self.ofda_api_url)
        conn.request("GET", self.ofda_api_evento + "?limit="+str(limit))
        print (self.ofda_api_evento + "?limit="+str(limit))
        r1 = conn.getresponse()
        data_raw = r1.read().decode("utf8")
        data = json.loads(data_raw)
        resultados = data['results']
        return resultados

    def do_GET(self):
        recursos = self.path.split("?")
        if len(recursos) > 1:
            parametros = recursos[1]
        else:
            parametros = ""

        limit = 10

        if parametros:
            pars_limit = parametros.split("=")
            if pars_limit[0] == "limit":
                limit = int(pars_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("NO SE HAN OBTENIDO PARAMETROS")


        if self.path=='/':

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html=self.get_pag_principal()

            self.wfile.write(bytes(html, "utf8"))

        elif 'listDrugs' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            medicinas = []
            resultados = self.devuelve_resultados_genericos(limit)
            for r in resultados:
                if ('generic_name' in r['openfda']):
                    medicinas.append (r['openfda']['generic_name'][0])
                else:
                    medicinas.append('UNKNOWN')
            resultado_html = self.devuelve_web (medicinas)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listCompanies' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            comp = []
            resultados = self.devuelve_resultados_genericos (limit)
            for r in resultados:
                if ('manufacturer_name' in r['openfda']):
                    comp.append (r['openfda']['manufacturer_name'][0])
                else:
                    comp.append('Desconocido')
            resultado_html = self.devuelve_web(comp)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listWarnings' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            warnings_lista = []
            resultados = self.devuelve_resultados_genericos (limit)
            for r in resultados:
                if ('warnings' in r):
                    warnings_lista.append (r['warnings'][0])
                else:
                    warnings_lista.append('Desconocido')
            resultado_html = self.devuelve_web(warnings_lista)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'searchCompany' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            comp=self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection(self.ofda_api_url)
            conn.request("GET", self.ofda_api_evento + "?limit=" + str(limit) + self.ofda_api_comp + comp)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")

            datosofda = json.loads(data)
            events_search_comp = datosofda['results']

            for event in events_search_comp:
                companies.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.devuelve_web(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'searchDrug' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10
            drug=self.path.split('=')[1]

            drugs = []
            conn = http.client.HTTPSConnection(self.ofda_api_url)
            conn.request("GET", self.ofda_api_evento + "?limit="+str(limit) + self.ofda_api_drug + drug)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            datosofda_2 = json.loads(data)
            events_search_drug = datosofda_2['results']
            for r in events_search_drug:
                if ('generic_name' in r['openfda']):
                    drugs.append(r['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')

            resultado_html = self.devuelve_web(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        ###########################REDIRECT????????###############################
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            #self.wfile.write("WHAT IS  '{}'?".format(self.path).encode())

        return



socketserver.TCPServer.allow_reuse_address= True
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
