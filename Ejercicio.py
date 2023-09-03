class Factura:
    valor = 100

    def pago(self):
        print("por aca paso")


#Solamente estoy llamando a un atributo de la clase
#Es sencillo y es entendible
print(f"El valor de la factura es: {Factura.valor}")

#Aca acabo de crear una variable de tipo clase que me permite acceder a 
#los atributos de la clase.
prueba = Factura()
#Como en este ejemplo.
print(prueba.valor)

#aca realizo una instancia del metodo pago
prueba.pago()

