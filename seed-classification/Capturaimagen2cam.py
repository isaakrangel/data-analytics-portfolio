import cv2
import numpy as np
import imutils
import os
# cd Documents\ARCHIVOS 2022\Proyecto Sacha Inchi\Codigo seleccion\Red neuronal
# python Capturaimagen.py
Datos = 'Tipo2'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)

cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW) #seleccion de camara y captura con esa ( 0 o 1)
cap2 = cv2.VideoCapture(2,cv2.CAP_DSHOW)

# posicion de recorte
x1, y1 = 20, 0 
x2, y2 = 450, 380

count = 0

def camara(hilo):
    # codigo prediccion
    # tomar foto y proceso de prediccion
    if hilo==1:
        image = frame1.copy()
    elif hilo==2:
        image = frame2.copy()
   
    objeto = image       
    objeto = objeto[y1:y2,x1:x2]
    objeto = cv2.resize(objeto,(460,345),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(Datos+'/objeto_{}.jpg'.format(hilo),objeto)
    print('Imagen guardada:'+'/objeto_{}.jpg'.format(hilo))

while True:
    
    ret1, frame1 = cap1.read()
    if ret1 == False: break

    ret2, frame2 = cap2.read()
    if ret1 == False: break
    
    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    k = cv2.waitKey(1)
    if k == ord('s'):
        camara(1)
    if k == ord('d'):
        camara(2)
    if k == 27:
        break 

cap1.release()
cap2.release()
cv2.destroyAllWindows()