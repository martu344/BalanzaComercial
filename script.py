import urllib.request, json, time

periodo = "202406,202407,202408"
total = 0
totalcnh = 0
# Leer datos de economias.json
#print("paso3")
with open('info.json', 'r') as f:
    economias = json.load(f)

for economy, datos in economias.items():
    if economy != "eur" and economy != "cnh":
        socios=datos["socios"]
        for i, socio in enumerate(socios):
            if socio["pais"] == "eur":
                total += socio["total"]
                #print("sumando a ",socio["pais"]," la cant= ",socio["total"]," y el total es= ",total)
            if socio["pais"] == "cnh":
                totalcnh += socio["total"]
                #print("sumando a ",socio["pais"]," la cant= ",socio["total"]," y el total es= ",total)
            
    
    if economy == "eur":
        total_fobvalueGrupo = 0
        for i, code in enumerate(datos["code"]):
            parternCode = code
            socios=datos["grupo"]
            preSocios=datos["preSocios"]

            for inx, grupo in enumerate(socios):
                reportercode=grupo["parternCode"]
                #time.sleep(30) 
                try:
                            
                    url = f"https://comtradeapi.un.org/data/v1/get/C/M/HS?period={periodo}&reporterCode={reportercode}&partnerCode={parternCode}&flowCode=M,X&&partner2Code=0&motCode=0&cmdCode=total"

                    hdr ={
                            'Cache-Control': 'no-cache',
                            'Ocp-Apim-Subscription-Key': 'cbb2366660ff4ef882411da58042aaaf',
                        }

                    req = urllib.request.Request(url, headers=hdr)
                    req.get_method = lambda: 'GET'
                    response = urllib.request.urlopen(req)
                    #print(response.getcode())
                    data = response.read()
                    data_dict = json.loads(data)

                    for item in data_dict.get("data", []):  # Proteger ante datos vacíos
                        if "primaryValue" in item and item["primaryValue"] is not None:
                            total_fobvalueGrupo += item["primaryValue"]
                            
                            # Calcular y actualizar el peso solo si no es el primer elemento
                        if inx == len(socio["grupo"]) - 1 and i == len(datos["code"]) - 1:
                            print("a TOTAL le sumo = ", grupo["total"] ," = ", total_fobvalueGrupo)
                            datos["total"]=total + total_fobvalueGrupo

                            print("le total de cnh es= ", total_fobvalueGrupo)
                            datos["socios"]["total"]=total_fobvalueGrupo

                            
                            datos["socios"]["peso"] = (total_fobvalueGrupo * 100) / datos["total"]
                            print("el peso de cnh es ",datos["socios"]["peso"]) 
                           
                            # Guardar los datos actualizados en el archivo JSON
                           #print("paso2")
                            with open('info.json', 'w') as f:
                                json.dump(economias, f, indent=4)

                except Exception as e:
                            print(f"Error en la segunda llamada: {e}")
                            #Llenamos preSocios
        if  "preSocios" in datos:
            for ifx, preSocio in enumerate(datos["preSocios"]):
                for ikk, so in enumerate(economias[preSocio["pais"]]["socios"]):
                    if so["pais"] == economy:
                        preSocio["total"] = so["total"]
                        print (f"estoy buscando los datos de {preSocio["pais"]} e ingrese a {so["pais"]} y quiero el {so["total"]} para llenar el total de {preSocio["total"]}")
                        preSocio["peso"] = (preSocio["total"] * 100) / datos["total"]   

                        # Guardar los datos actualizados en el archivo JSON
                        #print("paso1")
                        with open('info.json', 'w') as f:
                            json.dump(economias, f, indent=4)

    if economy == "cnh":
        datos["total"] = totalcnh
        if  "preSocios" in datos:
            for ifx, preSocio in enumerate(datos["preSocios"]):
                for ikk, so in enumerate(economias[preSocio["pais"]]["socios"]):
                    if so["pais"] == economy:
                        preSocio["total"] = so["total"]
                        print (f"estoy buscando los datos de {preSocio["pais"]} e ingrese a {so["pais"]} y quiero el {so["total"]} para llenar el total de {preSocio["total"]}")
                        preSocio["peso"] = (preSocio["total"] * 100) / datos["total"]   

                        # Guardar los datos actualizados en el archivo JSON
                        #print("paso1")
                        with open('info.json', 'w') as f:
                            json.dump(economias, f, indent=4)
                       
    if economy == "mxnn":
        #print("paso4")
       #Llenamos socios
        reportercode = datos["code"]
        socios=datos["socios"]
        for i, socio in enumerate(socios):
            total_fobvalue = 0
            peso = 0
            if "grupo" in socio:
                for idx,socioCompuesto in enumerate(socio["grupo"]):
                    total_fobvalueCompuesto=0
                    print(f"vuelta en socioCompuesto numero: {idx}")
                    parternCode = socioCompuesto["parternCode"]
                    time.sleep(30)
                    try:
                        url = f"https://comtradeapi.un.org/data/v1/get/C/M/HS?period={periodo}&reporterCode={reportercode}&partnerCode={parternCode}&flowCode=M,X&&partner2Code=0&motCode=0&cmdCode=total"

                        hdr ={
                                'Cache-Control': 'no-cache',
                                'Ocp-Apim-Subscription-Key': 'cbb2366660ff4ef882411da58042aaaf',
                            }

                        req = urllib.request.Request(url, headers=hdr)
                        req.get_method = lambda: 'GET'
                        response = urllib.request.urlopen(req)
                        #print(response.getcode())
                        data = response.read()
                        data_dict = json.loads(data)

                        for item in data_dict.get("data", []):  # Proteger ante datos vacíos
                            if "primaryValue" in item and item["primaryValue"] is not None:
                                total_fobvalueCompuesto += item["primaryValue"]
                                #total_fobvalue += item["primaryValue"]

                        print(f"{i} total commodities para el socio {parternCode}={total_fobvalueCompuesto}")
                        if idx == 0:
                            socio["total"] = 0
                        if idx == len(socio["grupo"]) - 1:
                            peso = (total_fobvalue * 100) /datos["total"]
                            socio["peso"] = peso
                            socioCompuesto["total"] = total_fobvalueCompuesto
                            socio["total"] += total_fobvalue
                        else:
                            socioCompuesto["total"] = total_fobvalueCompuesto
                            socio["total"] += total_fobvalue

                        print(f"los datos a guardar son total= {socio["total"]} y peso= {socio["peso"]}")

                        # Guardar los datos actualizados en el archivo JSON
                        with open('info.json', 'w') as f:
                                json.dump(economias, f, indent=4)

                    except Exception as e:
                        print(f"Error en la segunda llamada: {e}")

                    
            else:
                parternCode = socio["parternCode"]
                print(f"evaluando a {economy} y su codigo es {reportercode}")
                print(f"el socio es {socio["pais"]} y su codigo es {parternCode} estamos en la vuelta {i}")
                time.sleep(50)
                try:
                    
                    url = f"https://comtradeapi.un.org/data/v1/get/C/M/HS?period={periodo}&reporterCode={reportercode}&partnerCode={parternCode}&flowCode=M,X&&partner2Code=0&motCode=0&cmdCode=total"

                    hdr ={
                            'Cache-Control': 'no-cache',
                            'Ocp-Apim-Subscription-Key': 'cbb2366660ff4ef882411da58042aaaf',
                        }

                    req = urllib.request.Request(url, headers=hdr)
                    req.get_method = lambda: 'GET'
                    response = urllib.request.urlopen(req)
                    #print(response.getcode())
                    data = response.read()
                    data_dict = json.loads(data)

                    for item in data_dict.get("data", []):  # Proteger ante datos vacíos
                        if "primaryValue" in item and item["primaryValue"] is not None:
                            total_fobvalue += item["primaryValue"]
                            print(f"paso en la vuelta {i}")

                    print(f"{i} total commodities para el socio {parternCode}={total_fobvalue}")

                    # Calcular y actualizar el peso solo si no es el primer elemento
                    if i>0:
                        peso = (total_fobvalue * 100) /datos["total"]
                        socio["peso"] = peso
                    else:
                        datos["total"]=total_fobvalue

                    socio["total"] = total_fobvalue
                    print(f"los datos a guardar son total= {socio["total"]} y peso= {socio["peso"]}")

                    # Guardar los datos actualizados en el archivo JSON
                    with open('info.json', 'w') as f:
                            json.dump(economias, f, indent=4)

                except Exception as e:
                    print(f"Error en la segunda llamada: {e}")

                
                #Llenamos preSocios
            if  "preSocios" in datos:
             for ifx, preSocios in enumerate(datos["preSocios"]):
                for ikk, so in enumerate(economias[preSocios["pais"]]["socios"]):
                    if so["pais"] == economy:
                        preSocios["total"] = so["total"]
                        print (f"estoy en presocios y el total es: {datos["total"]} perteneciente a {datos["code"]}")
                        preSocios["peso"] = (preSocios["total"] * 100) / datos["total"]      
                        # Guardar los datos actualizados en el archivo JSON
                        with open('info.json', 'w') as f:
                                json.dump(economias, f, indent=4)