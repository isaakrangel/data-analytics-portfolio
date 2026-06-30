"""
Created on Wed Jul 14 16:41:05 2021

@author: acer
cd Documents\ARCHIVOS 2022\Proyecto Sacha Inchi\Codigo seleccion\Red neuronal
python RYC.py
"""
import cv2
import os
import numpy as np
import imutils
from PIL import Image, ImageDraw
import scipy.misc
from scipy import misc
"""
direccion de entrada  Recorte y contorno
"""
input_images_path = "C:/Users/acer/Documents/ARCHIVOS 2022/Proyecto Sacha Inchi/Codigo seleccion/CODIGO VERSION 3.0/Prueba_semilla"
files_name = os.listdir(input_images_path)
print(files_name)




Datos = 'Semillas recortadas3'

if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)

x1, y1 = 20, 0 
x2, y2 = 450, 380

count = 0
# Localizacion de la semilla aleatoria
seed = (0, 0)
# Valor de pixel con el que se reemplazará el entorno de la silueta
rep_value = (255, 255, 255, 255)


for file_name in files_name:
    #print(file_name)
    image_path = input_images_path + "/" + file_name
    print(image_path)
    
    image = cv2.imread(image_path)
    image.shape
    if image is None:
        continue

         
    #cv2.rectangle(image,(x1,y1),(x2,y2),(255,0,0),2)
    # image = Image.open(image_path).convert('RGBA')
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    imageRGB.shape
    imagen_recortada = imageRGB[y1:y2,x1:x2]
    imagen_recortada.shape

    #image = cv2.resize(image,(500,345),interpolation=cv2.INTER_CUBIC)
    # imagen_recortada = misc(imageRGB)
    # La función floodfill() es la que calcula la imagen_silueta
    ImageDraw.floodfill(imagen_recortada, seed, rep_value, thresh = 150) 
    #image
    #imagen_recortada.save("imagen_silueta.png") # Por incopatibilidades en los formatos, se guarda la imagen como png
    
    objeto = imagen_recortada
    cv2.imwrite(Datos+'/objeto_{}.jpg'.format(count),objeto)
    print('Imagen guardada:'+'/objeto_{}.jpg'.format(count))
    count = count +1

    cv2.imshow('objeto', objeto)
    #cv2.imshow('image',image)
    cv2.waitKey(0)


cv2.destroyAllWindows()




