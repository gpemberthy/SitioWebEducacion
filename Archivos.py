import os
    from pathlib import *

"""""
mi_archivo = open('Prueba.txt','a')

#mi_archivo.write('Hola soy German')
mi_archivo.writelines(['hola','soy','German'])
mi_archivo.close()
"""
#os.rmdir('C:\\Users\\germa\\Desktop\\SitioWebEducacion\\pruebapaborrar')

ruta = Path('C:/Users/germa/Desktop/SitioWebEducacion')
archivo = ruta / 'Prueba.txt'
mi_archivo = open(archivo)

print(mi_archivo.read())
base=Path.home()
guia = Path(base, 'Escritorio', 'Mongo')
print('base valor')
print(base)
print(guia)

for p in Path(guia).glob('**/*.csv'):
    print(p)
guia2=Path(base, 'Escritorio')
ruta=guia2.relative_to('Mongo')
print(ruta)