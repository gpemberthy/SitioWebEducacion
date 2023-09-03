##nombre="El agua es dulce como la luna"
##print("agua" in nombre)
##print("Sol" in nombre)
##print(f"El tamaño de la variable es: {len(nombre)}")

##mi_lista=["abc", 55, "bg"]
##print(len(mi_lista))
##print(type(mi_lista))
##resultado=mi_lista[0:2]
##print(resultado)


"""mi_dict = {"valores_1":
           {
               "v1":3,
               "v2":6
            },
           "puntos":
           {
               "points1":9,
               "points2":[10,300,15]
            }}
print(mi_dict["puntos"]["points2"][1])

mi_dic = {"nombre":"Karen", "apellido":"Jurgens", "edad":35, "ocupacion":"Periodista"}
mi_dic["edad"]= 36
mi_dic["ocupacion"]="Editora"
mi_dic["pais"]="Colombia"
print(mi_dic)

mi_tupla=(2,6,9,8)
#Le puedo asignar el valor a 4 variables diferentes de la siguiente manera

a,b,c,d=mi_tupla
print(a)
print(a,b,c,d)


mi_tupla = (1, 2, 3, 2, 3, 1, 3, 2, 3, 3, 3, 1, 3, 2, 2, 1, 3, 2)
print(mi_tupla.count(2))

mi_set_1 = {1, 2, "tres", "cuatro"}
mi_set_2 = {"tres", 4, 5} 
mi_set3 = mi_set_1.union(mi_set_2)

#Solución al taller deldia 3 del curso de python
texto1 = input("Ingrese un texto: ")
letra1= input("Ingrese letra 1: ")
letra2= input("Ingrese letra 2: ")
letra3= input("Ingrese letra 3: ")
print(f"La cantidad de letras {letra1.lower()} es: {texto1.count(letra1.lower())}")
print(f"La cantidad de letras {letra2.lower()} es: {texto1.count(letra2.lower())}")
print(f"La cantidad de letras {letra3.lower()} es: {texto1.count(letra3.lower())}")
mi_tupla=texto1.split()
print(f"La cantidad de palabras que hay en la frase es: {len(mi_tupla)}")
print(f"la primera letra del texto es: {texto1[0]}")
print(f"la ultima letra del texto es: {texto1[-1]}")
print(type(mi_tupla))
mi_tupla.reverse()
#print(mi_tupla)
texto2=" ".join(mi_tupla)
print(texto2)
print(texto1.find("Python"))

num1 = int(input("Ingresa un número: "))
num2 = int(input("Ingresa otro número: "))

if num1>num2:
    print(f"{num1} es mayor que {num2}")
elif (num2>num1): 
    print(f"{num2} es mayor que {num1}")
else:
    print(f"{num1} y {num2} son iguales")

lista_nombres = ["Marcos", "Laura", "Mónica", "Javier", "Celina", "Marta", "Darío", "Emiliano", "Melisa"]
for indice, nombre in enumerate(lista_nombres):
    print(f'{nombre} se encuentra en el índice {indice}')
    #print(f"nombre: {nombre}")

lista_indices = list(enumerate("Python"))
print(lista_indices)

lista_nombres = ["Marcos", "Laura", "Mónica", "Javier", "Celina", "Marta", "Darío", "Emiliano", "Melisa"]
for indice, nombre in enumerate(lista_nombres):
    if "M" in nombre:
        print(indice)

capitales = ["Berlín", "Tokio", "París", "Helsinki", "Ottawa", "Canberra"]
paises = ["Alemania", "Japón", "Francia", "Finlandia", "Canadá", "Australia"]
mi_lista = list(zip(capitales,paises))
for cap, pais in mi_lista:
    print(f"La capital de {pais} es {cap}")

diccionario_edades = {"Carlos":55, "María":42, "Mabel":78, "José":44, "Lucas":24, "Rocío":35, "Sebastián":19, "Catalina":2,"Darío":49}
edad_minima = min(diccionario_edades.values())
ultimo_nombre = max(diccionario_edades)
print(edad_minima)
print(ultimo_nombre)

valores = [1, 2, 3, 4, 5, 6, 9.5]
valores_cuadrado =[]
for a in valores:
    valores_cuadrado.append(a*a)
print(valores_cuadrado)

valores_cuadrado2 =[a*a for a in valores]
print(valores_cuadrado2)

temperatura_fahrenheit = [32, 212, 275]
grados_celsius = []
grados_celsius = [(a-32)*(5/9) for a in temperatura_fahrenheit]

"""
from random import *
nombre=input("Por favor ingresa tu nombre: ")
print(f"Bueno {nombre} he pensado un número entre 1 y 100 y tienes solamente 8 intentos para adivinar cual crees que es el numero ")
intentos = 1
numero=randint(1,40)
while intentos < 9:
    numero1=int(input(f"Intento No {intentos}:"))

    if numero not in range(1,101):
        print("Numero no valido")
    elif numero1<numero:
        print("Incorrecto, numero ingresado menor")
    elif numero1>numero:
        print("Incorrecto, numero ingresado mayor")
    else:
        print(f"Felicitaciones, has acertado en {intentos} intentos")
        break
    if intentos==8:
        print(f"Fallaste el numero que pense era {numero}")
    intentos += 1

