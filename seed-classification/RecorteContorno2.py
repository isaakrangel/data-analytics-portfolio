

import cv2
import os
import numpy as gfg
from PIL import Image, ImageDraw
# from __future__ import print_function
"""
direccion de entrada
"""
# input_images_path = "C:/Users/acer/Documents/ARCHIVOS 2022/Proyecto Sacha Inchi/Codigo seleccion/CODIGO VERSION 3.0/Prueba_semilla"

input_images_path = "C:/Users/acer/Documents/ARCHIVOS 2022/Proyecto Sacha Inchi/Codigo seleccion/CODIGO VERSION 3.0/Fotos frutos/clara"

# input_images_path = "C:/Users/acer/Documents/ARCHIVOS 2022/Proyecto Sacha Inchi/Codigo seleccion/CODIGO VERSION 3.0/Fotos frutos/oscura"
files_name = os.listdir(input_images_path)
print(files_name)


"""
carpetas de salida
"""
# Datos = 'Semillas recortadas3'

Datos = 'Semillas Claras recortadas2'

# Datos = 'Semillas Oscuras recortadas2'


"""
creacion de capeta de salida
"""
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)

x1, y1 = 20, 0 
x2, y2 = 450, 380

count = 0
# Localizacion de la semilla aleatoria
seed = (0, 0)
# Valor de pixel con el que se reemplazará el entorno de la silueta
rep_value = (0, 0, 0, 0)

for file_name in files_name:
    #print(file_name)
    image_path = input_images_path + "/" + file_name
    print(image_path)
    image = cv2.imread(image_path)
    if image is None:
        continue

    
    image = cv2.resize(image,(500,345),interpolation=cv2.INTER_CUBIC)
    
    image = image[y1:y2,x1:x2]
    
    image = Image.fromarray(image)

    # print(image.format, image.size, image.mode)
                
    ImageDraw.floodfill(image, seed, rep_value, thresh = 130)
    
    objeto = gfg.asarray(image)

    # print(objeto.format, objeto.size, objeto.mode)

    cv2.imwrite(Datos+'/ob_{}.jpg'.format(count),objeto)
    print('Imagen guardada:'+'/ob_{}.jpg'.format(count))
    count = count +1
      
    
    # cv2.imshow('image',image)
    # cv2.imshow('objeto', objeto)
    cv2.waitKey(0)


cv2.destroyAllWindows()