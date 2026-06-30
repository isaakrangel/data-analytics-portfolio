import cv2
import numpy as np
import imutils
import os

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

#cargar modelos y pesos de entrenamiento
modelo = './Modelo antiguo/modelo.h5'
pesos_modelo = './Modelo antiguo/pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)


#crear carpeta y permitir capturar con la camara
Datos = 'sacha inchi'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)

cap = cv2.VideoCapture(2,cv2.CAP_DSHOW)

x1, y1 = 140, 100 
x2, y2 = 500, 350

count = 0
while True:

    ret, frame = cap.read()
    if ret == False: break
    imAux = frame.copy()
    cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)

    objeto = imAux[y1:y2,x1:x2]
    objeto = cv2.resize(objeto,(460,345),interpolation=cv2.INTER_CUBIC)
    #print(objeto.shape)
    
    longitud, altura = 150, 150
    # count = 0
    #count2 = 1
    k = cv2.waitKey(1)
    
    if k == ord('s'):
        cv2.imwrite(Datos+'/objeto_{}.jpg'.format(count),objeto)
        print('Imagen guardada:'+'/objeto_{}.jpg'.format(count))
        count1 = count + 1
        
        def predict(file):
          x = load_img(file, target_size=(longitud, altura))
          x = img_to_array(x)
          x = np.expand_dims(x, axis=0)
          array = cnn.predict(x)
          result = array[0]
          answer = np.argmax(result)
          if answer == 0:
            print("pred: Crema")
          elif answer == 1:
            print("pred: Manchada")
          elif answer == 2:
            print("pred: Oscura")

          return answer

        predict('./CAM/objeto_{}.jpg'.format(count1-1))

    if k == 27:
        break

    cv2.imshow('frame',frame)
    cv2.imshow('objeto',objeto)

cap.release()
cv2.destroyAllWindows()
