# Librerias para la conexión con la base de datos Mongo
from pymongo import MongoClient

def conexion_mongo():
    """Funcion que brinda la conexion con la BD Mongo"""
    #Apertura de la conexión con la BD de Mongo
    cliente = MongoClient('mongodb://localhost:27017/')
    #La Base de Datos se llama Balcones
    return cliente

def conexion_produccion():
    cliente = conexion_mongo()
    db = cliente.Balcones
    return db

def conexion_desarollo():
    cliente = conexion_mongo()
    db2 = cliente.Balcones_Desarrollo
    return db2

def borrado_tablas_desarrollo():
    db = conexion_produccion()
    db2 = conexion_desarollo()

    collection_pagos = db.Pagos
    collection_pagos_desarrollo = db2.Pagos
    collection_pagos_desarrollo.drop()
    for produccion in collection_pagos.find():
        if produccion['No Recibo'] < 529:
            collection_pagos_desarrollo.insert_one({'No Recibo': int(produccion['No Recibo']),
                                                    'Casa': produccion['Casa'],
                                                    'Fecha': produccion['Fecha'],
                                                    'Anno': produccion['Anno'],
                                                    'Valor': produccion['Valor'],
                                                    'Tipo': produccion['Tipo'],
                                                    'Recibi De': produccion['Recibi De']
                                                    })
        elif produccion['No Recibo'] < 535:
            collection_pagos_desarrollo.insert_one({'No Recibo': int(produccion['No Recibo']),
                                                    'Casa': produccion['Casa'],
                                                    'Fecha': produccion['Fecha'],
                                                    'Anno': produccion['Anno'],
                                                    'Valor': produccion['Valor'],
                                                    'Tipo': produccion['Tipo'],
                                                    'Observaciones': ' ',
                                                    'Recibi De': produccion['Recibi De'],
                                                    'Estado': produccion['Estado']
                                                    })
        else:
            collection_pagos_desarrollo.insert_one({'No Recibo': int(produccion['No Recibo']),
                                                    'Casa': produccion['Casa'],
                                                    'Fecha': produccion['Fecha'],
                                                    'Anno': produccion['Anno'],
                                                    'Valor': produccion['Valor'],
                                                    'Tipo': produccion['Tipo'],
                                                    'Observaciones': produccion['Observaciones'],
                                                    'Recibi De': produccion['Recibi De'],
                                                    'Estado': produccion['Estado']
                                                    })


borrado_tablas_desarrollo()