class Animal:
    """Metodo Animal"""
    def __init__(self, edad, color) -> None:
        self.edad = edad
        self.color = color
    
    def nacer(self):
        """Metodo de nacer"""
        print("Este animal ha nacido")

    def hablar(self):
        print("Este animal emite un sonido")

class Pajaro(Animal):
    #Agregar atributos a una clase heredada
    super().__init__(edad, color)
    self.altura_vuelo = altura_vuelo

piolin=Pajaro(3,'Amarillo')

piolin.nacer()