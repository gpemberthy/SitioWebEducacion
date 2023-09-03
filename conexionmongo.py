from os import system
from pymongo import MongoClient
import os
from pathlib import Path


finalizar_programa = True
def inicio():
    """Function printing python version."""
    system('cls')
    print("*" * 70)
    print("*" * 2 + "  Bienvenido al administrador Conjunto Balcones de Capellania    **")
    print("*" * 70)
    eleccion = 'x'
    while not eleccion.isnumeric() or int(eleccion) not in range(1,7):
        print('''
            [1] Administración residentes 
            [2] Ingresar pago
            [3] Consultar estado residente
            [4] Generar facturacion del mes
            [5] Salir del Programa  
            ''')
        eleccion = input('Seleccion: ')
    return(eleccion)
        
def ingresar_pago():
    system('cls')
    print("*" * 70)
    print("*" * 2 + "  Modulo Ingresar Pago")
    print("*" * 70)
    valor_pagado = input('Ingresar valor pagado: ')
    pagado_por = ("Pagado por: ")
    return(valor_pagado)

def conexion_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    return client

def administracion_residentes():
    system('cls')
    print("*" * 70)
    print("*" * 2 + "       Bienvenido al modulo de administracion de residentes       **")
    print("*" * 70)
    print(" Que deseas realizar")
    print(" (1) Consulta de residentes")
    print(" (2) modificar un residente")
    print(" (3) Agregar un residente")
    print(" (4) Volver")
    Residentes = input("Indica: ")
    if Residentes == '1':
        print("**      Modulo de consulta      **")
        Casa = input("Ingresa el numero de casa a consultar: ")
        print("*  A continuacion se muestran los residentes activos de la casa seleccionada")
        cliente = conexion_mongo()
        db = cliente.Balcones
        collection_Personas = db.Personas
        for document in collection_Personas.find({'Casa': Casa}):
                if document['Estado'] == 'Activo':
                    print('\n')
                    print(f"Nombre: {document['Personas']['Nombres']} {document['Personas']['Apellidos']}")
                    print(f"Documento: {document['Identificacion']['Tipo']} {document['Identificacion']['Numero']}")
                    print(f"Tipo: {document['Tipo']}")
                    print(f"Telefono: {document['Telefono']['Activo']}")
                    
                else:
                    print('Casa no encontrada')
        input("Selecciona enter para continuar")
    elif Residentes == '2':
        print("*      Modulo de modificación     *")
        Casa = input("Ingresa el numero de casa a modificar: ")
        print("*  A continuacion se muestran los residentes activos de la casa seleccionada")
        cliente = conexion_mongo()
        db = cliente.Balcones
        collection_Personas = db.Personas
        for document in collection_Personas.find({'Casa': Casa}):
                if document['Estado'] == 'Activo':
                    print('\n')
                    print(f"Nombre: {document['Personas']['Nombres']} {document['Personas']['Apellidos']}")
                    print(f"Documento: {document['Identificacion']['Tipo']} {document['Identificacion']['Numero']}")
                    print(f"Tipo: {document['Tipo']}")
                    print(f"Telefono: {document['Telefono']['Activo']}")
                    
                else:
                    print('Casa no encontrada')
        input("Selecciona enter para continuar")
    elif Residentes == '3':
        print("Modulo de agregar residentes")
    elif Residentes == '4':
        print("Volver")
    else:
        print("Opción no valida")

def cerrar_programa():
    print("Fin del programa")
    return False


#Bucle principal del programa
while finalizar_programa:  
    eleccion = inicio()
    if int(eleccion) == 1:
        administracion_residentes()
    elif int(eleccion) == 2:
        pago = ingresar_pago()
        Casa = input("Ingrese la casa: ")
        cliente = conexion_mongo()
        db = cliente.Balcones
        collection_Recibos = db.Recibos
        collection_Eventos = db.Eventos
        collection_Pagos = db.Pagos
        collection_Personas = db.Personas
        collection_Temporal = db.Temporal
        for document in collection_Recibos.find({'Casa': Casa, 'Mes': 'Enero'}):
            if Casa == document['Casa']:
                print(document['Valor'])
                #print(document['Pagos']['Forma_de_Pago'])
            else:
                print('Casa no encontrada')

        #Consulta para traer el ultimo numero registrado
        for rec in collection_Eventos.find():
            if rec['Descripcion Evento'] == 'Numero Recibo':
                Numero_Recibo = int(rec['Valor'])
            if rec['Descripcion Evento'] == 'Mes Facturado':
                Mes_Facturado = rec['Valor']
            if rec['Descripcion Evento'] == 'Anno':
                Anno_Facturado = rec['Valor']
            if rec['Descripcion Evento'] == 'Cuota Facturacion':
                Cuota_Facturacion = rec['Valor']

        cont = 1
        cero='0'
        for cargar in range(1,15):
            if cont < 10:
                Casa='0'+str(cont)
            else:
                Casa=str(cont)
                collection_Temporal.insert_one({'Recibo': Numero_Recibo, 
                                                'Casa': Casa, 
                                                'Fecha': '2023-08-01',
                                                'Anno': Anno_Facturado,
                                                'Valor': Cuota_Facturacion,
                                                'Mes': Mes_Facturado,
                                                'Estado': "Pendiente" })
            cont += 1
            print(Casa)
            Numero_Recibo += 1
            print(f'El numero del recibo es {Numero_Recibo}')
    elif int(eleccion) == 3:
        print("Consulta estado residente")
    elif int(eleccion) == 4:
        print("Generar facturacion del mes")
        zz=input("Valor casas: ")
    elif eleccion == '5':
        finalizar_programa = cerrar_programa()
    else:
        cerrar_programa()
        
