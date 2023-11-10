import bs4
import requests
import re
from datetime import datetime


def titulosDiariosAAA(urlLanzamientos):
    try:
        resultLanzamiento = requests.get(urlLanzamientos)
        soupLanzamientos = bs4.BeautifulSoup(resultLanzamiento.text, 'html.parser')

        tablasAAA = soupLanzamientos.find_all('table', class_='table transparente tablasinbordes')

        fechaHoy = datetime.now().date()
        fecha_formato_pagina = "%d/%m/%Y"

        datos_serializados = []

        for tabla in tablasAAA:
            fecha_element = tabla.find('div', class_='tcenter w100 t11')
            fecha_text = fecha_element.text
            fecha_formateada = datetime.strptime(fecha_text, fecha_formato_pagina).date()

            if fecha_formateada == fechaHoy:
                titulo_element = tabla.find('strong')
                enlace_element = tabla.find('a')

                fecha = fecha_text
                titulo = titulo_element.text
                enlace = enlace_element.get('href')

                datos_serializados.append({
                    "fecha": fecha,
                    "titulo": titulo,
                    "enlace": enlace
                })

        return datos_serializados

    except Exception as e:
        print("Error al serializar la aplicación:", str(e))
        return []

def titulosDiariosIndie(urlLanzamientos):
    try:
        resultLanzamiento = requests.get(urlLanzamientos)
        soupLanzamientos = bs4.BeautifulSoup(resultLanzamiento.text, 'html.parser')

        date_pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{4}')

        fecha_formato_pagina = "%d/%m/%Y"
        fechaHoy = datetime.now().date()

        tablas = soupLanzamientos.select('table.table.table-striped.froboto_real')
        data_list = []

        for tabla in tablas:
            fechas = tabla.find_all('td', class_='t08')
            nombres = tabla.find_all('span', itemprop='name')
            plataformas = tabla.find_all('td', {'itemprop': 'operatingSystem gamePlatform'})
            for fecha, nombre, plataforma in zip(fechas, nombres, plataformas):
                fechaStrip = fecha.get_text(strip=True)
                if date_pattern.match(fechaStrip):
                    fechaFormated = datetime.strptime(fechaStrip, fecha_formato_pagina).date()
                    if fechaFormated == fechaHoy:
                        nombreText = nombre.get_text()
                        plataformaText = plataforma.get_text()
                        data_dict = {
                            "fecha": fechaStrip,
                            "titulo": nombreText,
                            "plataforma": plataformaText
                        }
                        data_list.append(data_dict)
        data_listO = sorted(data_list, key=lambda x: x['plataforma'])
        return data_listO

    except Exception as e:
        print("Error al serializar la aplicación:", str(e))
        return []

