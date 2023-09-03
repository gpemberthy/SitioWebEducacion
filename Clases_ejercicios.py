class Alarma:
    def postergar(self, cantidad_minutos):
        print("La alarma ha sido pospuesta {}".format(cantidad_minutos) + " minutos")

mi_alarma = Alarma()
mi_alarma.postergar(10)