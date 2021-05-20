# rutas que tengan que ver con la aplicación covid

from flask import render_template, request
from covid import app
import csv
import json 
from datetime import date

@app.route('/provincias')
def provincias():
    fichero = open('data/provincias.csv','r', encoding="utf8") # abrir el archivo 
    csvreader = csv.reader(fichero, delimiter = ',') # leer cada registro 
    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'valor': registro[1]}   # crear diccionario
        lista.append(d)
    
    fichero.close() # cierro fichero 
    print(lista)
    return json.dumps(lista)  # diccionario --> json 

@app.route('/provincias/<codigoProvincia>')
def laprovincia(codigoProvincia): 
    fichero = open('data/provincias.csv','r', encoding="utf8")

    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia'])
    for registro in dictreader: 
        if registro['codigo'] == codigoProvincia: 
            fichero.close()
            return registro['provincia']
        
    fichero.close()
    return 'La provincia no existe' 

'''  
@app.route('/casos/<int:year>', defaults={'mes': None, 'dia':None})
@app.route('/casos/<int:year>/<int:mes>', defaults={'dia':None})
@app.route('/casos/<int:year>/<int:mes>/<int:dia>')
def casos(year, mes, dia)
'''
@app.route('/casos/<int:year>', defaults={'mes': None, 'dia':None})
@app.route('/casos/<int:year>/<int:mes>')
@app.route('/casos/<int:year>/<int:mes>/<int:dia>')
def casos(year, mes, dia=None):
    if not mes: 
        fecha = '{:04d}'.format(year)
    
    elif not dia: 
        fecha = '{:04d}-{:02d}'.format(year, mes)
    
    else:
        fecha = '{:04d}-{:02d}-{:02d}'.format(year, mes, dia) # {:02d} va a coupar dos espacios; el cero es para que rellena el espacio con 0

    fichero = open('data/casos_diagnostico_provincia.csv', 'r', encoding='utf8') 
    dictReader = csv.DictReader(fichero)

    res = {
        'num_casos': 0,
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0,
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0,
    }
    

    for registro in dictReader:
        if fecha in registro['fecha']: 
            for clave in res: 
                res[clave] += int(registro[clave])

        elif registro['fecha'] > fecha:
           break

    fichero.close()
    return json.dumps(res)

@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    formulario = {
        'provincia': '',
        'fecha': str(date.today()), 
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0

    }

    fichero = open('data/provincias.csv','r', encoding="utf8")
    csvreader = csv.reader(fichero, delimiter = ',') 
    
    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'descripcion': registro[1]} 
        lista.append(d)

    if request.method == 'GET':
        return render_template("alta.html", datos = formulario, 
                                    provincias=lista, error='')
    
    for clave in formulario: 
        formulario[clave] = request.form[clave]
                                                                               
    # validar que num_casos en general es no negativo: 
    num_pcr = request.form['num_casos_prueba_pcr']
    try: 
        num_pcr = int(num_pcr)
        if num_pcr < 0: 
            raise ValueError('Debe ser no negativo')
    except ValueError:
        return render_template('alta.html', datos=formulario, error = 'PCR no puede ser negativa')


    return 'Se ha hecho un post'



