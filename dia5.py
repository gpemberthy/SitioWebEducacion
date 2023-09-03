'''
texto = ",:_#,,,,,,:::____##Pyt%on_ _Total,,,,,,::#"
print(texto)
p=texto.lstrip(",:%_#")
print(p)

frutas = ["mango", "banana", "cereza", "ciruela", "pomelo"] 
frutas.insert(3,"Naranja")
print(frutas)

marcas_smartphones = {"Samsung", "Xiaomi", "Apple", "Huawei", "LG"}

marcas_tv = {"Sony", "Philips", "Samsung", "LG"}
conjuntos_aislados=marcas_smartphones.isdisjoint(marcas_tv)

lista= [1,8,9,3]
lista_numeros = []
def todos_positivos(lista):
    for a in lista:
        if a > 0:
            lista_numeros.append(a)
        else:
            return False
    if len(lista) == len(lista_numeros):
        return True
print(todos_positivos(lista))

'''
from random import *
#lista inicial
palitos = ['-', '--', '---', '----']

#mezclar palitos
def mezclar(lista):
    shuffle(lista)
    return(lista)

#pedirle intento
def probar_suerte():
    intento = ''
    while intento not in ['1', '2', '3', '4']:
        intento = input("Elige un numero del 1 al 4: ")

    return int(intento)

#comprobar intento
def comprobar_intento(lista, intento):
    if lista[intento -1] == '-':
        print("Bum A lavar los platos")
    else:
        print(" Esta vez te has salvado")
    
    print(f"Te ha tocado:  {lista[intento-1]}")

palitos_mezclados = mezclar(palitos)

seleccion = probar_suerte()

comprobar_intento(palitos_mezclados,seleccion)




