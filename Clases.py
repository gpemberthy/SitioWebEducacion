class Pajaro:
	
    alas = True

    def __init__(self, color, especie):
        self.color = color
        self.especie = especie
	
    def piar(self):
        print('Pio, mi color es {}'.format(self.color))
	
    def volar(self, metros):
        print(f"El pajaro volo {metros} metros")
        self.piar()
    
    def pintar(): 
        self.color = 'negro'
        print(f"Ahora el papajaro es de color {self.color}")
    @classmethod
    def poner_huevos(cls, cantidad):
	    print(f"Puso {cantidad} de huevos")

#Se puede hacer un llamado de la clase de manera directa.
#Se puede realizar por que es una clase de metodo
Pajaro.poner_huevos(3)

#instancio la clase por medio de la variable piolin que es una variable de tipo clase.
piolin = Pajaro("Amarillo", "Tucan")

piolin.volar(250)
piolin.piar()

#Con esta instrucción lo que hacemos es modificar la clase.m
piolin.alas = True
'''
mi_pajaro = Pajaro('Negro', 'Tucan')
print(mi_pajaro.color)
print(mi_pajaro.especie)
# Le puedo cambiar el valor al atributo color
mi_pajaro.atributo = "Azul"
print(mi_pajaro.color)
# Aca puedo conocer cual es el valor de un atributo de clase.
print(Pajaro.alas)
print(mi_pajaro.alas)
'''