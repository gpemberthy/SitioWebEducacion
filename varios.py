lista_numeros=[]
num=0
lista=[1,2,15,7,2]
lista.sort()
lista.pop()
for a in lista:
    if a != num:
        lista_numeros.append(a)
    num = a
print(lista_numeros)

from random import *
#def lanzar_moneda():
moneda=['Cara', 'Cruz']
shuffle(moneda)
print(f'cara/cruz: {moneda[0]}')

args=[1,2,3]
suma =0
for a in args:
    suma += a*a
print(suma)

args2=[2,3,5,-7]
b=0
for a in args2:
    if a < 0:
        a = (-1)*a
        print(f'absoluto: {a}')
    print(f'antes de acumular: {a}')
    b += a
    print(f'despues de acumular: {a}')
print(f'el valor es: {b}')

print(' ')
kwargs={
    'color_ojos': 'azules',
    "color_pelo": 'rubio'
}
lista = []
for clave, valor in kwargs.items():
    lista.append(valor)

print(lista)
