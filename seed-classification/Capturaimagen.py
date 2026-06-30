import os
import cv2
import numpy as gfg
from PIL import Image, ImageDraws

# cd Documents\ARCHIVOS 2022\Proyecto Sacha Inchi\Codigo seleccion\Red neuronal
# python Capturaimagen.py
Datos = 'Claras Banda2'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW) #seleccion de camara y captura con esa ( 0 o 1)

# coordenadas de recorteq
x1, y1 = 30, 0 
x2, y2 = 420, 350
longitud, altura = 150, 150
# Localizacion de la semilla aleatoria para efecto de contorno
seed = (0, 0)
# Valor de pixel con el que se reemplazará el entorno de la silueta
rep_value = (0, 0, 0, 0)

semillas = 6

def camara(objeto,semillas):
     
    # codigo prediccion
    # tomar foto y proceso de prediccion
    # frame = objeto
    image = objeto
           
    image = cv2.resize(image,(460,345),interpolation=cv2.INTER_CUBIC)
    
    image = image[y1:y2,x1:x2]
    
    objeto = image
    # image = Image.fromarray(image)

    # ImageDraw.floodfill(image, seed, rep_value, thresh = 180)
    
    # objeto = gfg.asarray(image)

    cv2.imwrite(Datos+'/objeto_{}.jpg'.format(semillas),objeto)
    print('Imagen guardada:'+'/objeto_{}.jpg'.format(semillas))
            
    
    

while True:
    
    ret, frame = cap.read()
    if ret == False: break
    # imAux = frame.copy()
    objeto = frame.copy()
    # objeto = imAux
    # objeto = cv2.resize(objeto,(460,345),interpolation=cv2.INTER_CUBIC)
    print(frame.shape)
    print(objeto.shape)

    cv2.imshow('frame',frame)
    # cv2.imshow('objeto',objeto)
        
    k = cv2.waitKey(1)
    if k == ord('s'):
        semillas = semillas + 1
        camara(objeto,semillas)
    if k == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()

