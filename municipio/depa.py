from bs4 import BeautifulSoup
import requests
import pandas as pd

total_datos = []

def get_departamentos():
    URL_DEPA = "https://fichacomunidad.ine.gob.bo/"
    resultado = requests.get(URL_DEPA)
    content = resultado.text
    soup = BeautifulSoup(content,"html.parser")
    options = soup.find('select', id = "departamento").findAll("option")

    daerah = []
    for i in options:
        name = i.text
        value = i["value"]
        if value != "":
            daerah.append({
                "depa": name,
                "value": value
            })
            get_provincias(value)
    
    df = pd.DataFrame(total_datos)
    df.index = df.index + 1
    df.to_excel("municipios.xlsx")
    print(df)

def get_provincias(depto):
    URL_PROV = "https://fichacomunidad.ine.gob.bo/c_listadof/llenar_provincias"
    data = {'accion':'cargar_provincias'
            ,'id_depto':depto
            }
    resultado = requests.post(URL_PROV, data=data)
    content = resultado.text
    soup = BeautifulSoup(content,"html.parser")
    options = soup.find_all('option')

    
    for i in options:
        name = i.text
        value = i["value"]
        if value != "" and value != "-1":
            get_municipios(depto,value)

def get_municipios(depto,prov):
    global total_datos

    URL_MUN = "https://fichacomunidad.ine.gob.bo/c_listadof/llenar_municipios"
    data = {'accion':'cargar_municipios'
            ,'id_depto':depto
            ,'id_provincia':prov
            }
    resultado = requests.post(URL_MUN, data=data)
    content = resultado.text
    soup = BeautifulSoup(content,"html.parser")
    options = soup.find_all('option')

    for i in options:
        name = i.text
        value = i["value"]
        if value != "" and value != "-1":
            totales = get_ficha_municipio(depto,prov,value)
            total_datos.append(totales)

def get_comunidad(depto,prov,muni):
    URL_MUN = "https://fichacomunidad.ine.gob.bo/c_listadof/listar_comunidades"
    data = {'accion':'cargar_comunidades'
            ,'id_depto':depto
            ,'id_provincia':prov
            ,'id_municipio':muni
            }
    resultado = requests.post(URL_MUN, data=data)
    content = resultado.text
    soup = BeautifulSoup(content,"html.parser")
    options = soup.find_all('option')

    daerah = []
    for i in options:
        name = i.text
        value = i["value"]
        if value != "" and value != "-1":
            daerah.append({
                "comunidad": name,
                "value": value
            })
        
    print(daerah)
    print("--------------------------------------")
    exit()

def get_ficha_municipio(depto,prov,muni):
    URL_MUN = "https://fichacomunidad.ine.gob.bo/c_listadof/listar_comunidades"
    data = {
            'departamento':depto
            ,'provincias':prov
            ,'municipios':muni
            }
    resultado = requests.post(URL_MUN, data=data)
    content = resultado.text
    soup = BeautifulSoup(content,"html.parser")
    # Mostrar resumen de los datos que se extrae
    
    resp = soup.find('div', id = "imprimeme").find("div", class_="box-contentm").find("p")
    #resumen = unicodedata.normalize("NFKD", resp.text)
    resumen = [total.get_text(strip=True).replace("\xa0","") for total in resp] 
    
    #Sacamos el dato de población total de la tabla
    # Saca los titulo de la tabla de totales
    #resp = soup.find("div", id="NUmeses").find("table").find("thead")
    #print(resp.text)
    resp = soup.find("div", id="NUmeses").find("table").find("tbody").find("tr").find_all("td")
    totales = [total.text for total in resp]
    
    resp_totales = {
                "departamento": resumen[1]
                , "departamento_id": depto
                , "provincia": resumen[5]
                , "provincia_id": prov
                , "municipio": resumen[9]
                , "municipio_id": muni
                , "total": totales[1].replace(".","").replace(",","")
                , "hombres": totales[2].replace(".","").replace(",","")
                , "mujeres": totales[3].replace(".","").replace(",","")
            }
    return resp_totales
