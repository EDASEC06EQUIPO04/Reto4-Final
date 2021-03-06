"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import csv
import os
from DISClib.Algorithms.Graphs import scc

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadServices(analyzer,servicesfile, aux):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    #servicesfile = cf.data_dir + servicesfile

    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename, aux)


    #input_file = csv.DictReader(open(servicesfile, encoding="utf-8"), delimiter=",")


    return analyzer


def loadFile(analyzer, tripfile, aux):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    i=0
    for service in input_file:

        
        if lastservice is not None:

            sameservice = lastservice['start station id'] == service['start station id'] 
            samedirection = lastservice['end station id'] == service['end station id']


            model.addStopConnection(analyzer, lastservice, service, aux)      
        lastservice = service



    #print (analyzer['connections']) 
        #origen = service['start station id'] 
        #destino = service['end station id']       
        #model.addStopConnection(analyzer, origen , destino)

    model.addRouteConnections(analyzer)
    return analyzer




# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.numSCC(analyzer)


def connectedwithID(cont, id1,id2):
    return model.connectedwithID(cont, id1,id2)

def connectedwithID_1(cont, id1):
    return model.connectedwithID_1(cont, id1)

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg


def pathStationTime(cont, idinicio, time):
    return model.pathStationTime(cont, idinicio, time)


def loadServices_REQ5(analyzer,servicesfile, aux, edades):

    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile_REQ5(analyzer, filename, aux, edades)

    return analyzer

def loadFile_REQ5(analyzer, tripfile, aux, dic_edades):
    
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:

        
        if lastservice is not None:
            """ 
            sameservice = lastservice['start station id'] == service['start station id'] 
            samedirection = lastservice['end station id'] == service['end station id']
            if sameservice and samedirection:
                model.addStopConnection(analyzer, lastservice, service)
                i+=1
                print (i)
            """
            sameservice = lastservice['start station id'] == service['start station id'] 
            samedirection = lastservice['end station id'] == service['end station id']

            edad= 2020-int(service["birth year"])
            model.addStopConnection_REQ5(analyzer, lastservice, service, aux, dic_edades, edad)      
        lastservice = service
        
    model.addRouteConnections(analyzer)
    return analyzer


def loadServices_REQ6(analyzer,servicesfile, aux, lats):

    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            REQ6(analyzer, filename, aux, lats)

    return analyzer


def REQ6 (analyzer, tripfile, aux, dic_latitudes):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:

        
        if lastservice is not None:
            sameservice = lastservice['start station id'] == service['start station id'] 
            samedirection = lastservice['end station id'] == service['end station id']

            latitud= service["start station latitude"]
            print (latitud)
            model.addStopConnection_REQ6(analyzer, lastservice, service, aux, dic_latitudes, latitud)      
        lastservice = service
        
    model.addRouteConnections(analyzer)
    return analyzer


def compararlat2(analyzer, tripfile, latconsultadaf):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")

    latitud = float(latconsultadaf)
    diferencia1 = float(1000.5)
    latfinal = float(0)
    idinicio = 0
    tiempoviaje=0
    for service in input_file:
        comparalatitud1= float(service["start station latitude"])
        diff2= latitud-comparalatitud1
        if diff2<diferencia1:
            diferencia1=diff2
            latfinal= comparalatitud1
            idinicio = service['start station id']
            triptime = int(service['tripduration'])
    triptime2=triptime/6


    
    print("La latidud final mas proxima a la ingresada es: " , latfinal  )
    print("corresponde a la estacion final con id:  ", idinicio )
    print("el tiempo de viaje es:" , triptime2, "minutos ")





def compararlat1(analyzer, tripfile, latconsultadaf):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")

    latitud = float(latconsultadaf)
    diferencia1 = float(1000.5)
    latfinal = float(0)
    idinicio = 0
    
    for service in input_file:
        comparalatitud1= float(service["start station latitude"])
        diff2= comparalatitud1-latitud
        if diff2<diferencia1:
            diferencia1=diff2
            latfinal= comparalatitud1
            idinicio = service['start station id']
    print("La latidud inicial mas proxima a la ingresada es: " , latfinal  )
    print("corresponde a la estacion inicial con id:  ", idinicio )    


def floattoint (flchange):
    process= str(flchange)
    while len(process)<20:
        process= process+"0"
    prefinal= process.replace('.','')
    final = prefinal.replace('-','')
    return int(final)
    

