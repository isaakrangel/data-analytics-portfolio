"""
cd Documents\ARCHIVOS 2022\Proyecto Sacha Inchi\Codigo seleccion\CODIGO VERSION 3.0

python predecir.py
python predecir2.py
"""
import sys
import os
 

import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K

    
K.clear_session()

data_entrenamiento = './Imagenes finales/Entrenamiento'
data_validacion = './Imagenes finales/Validacion'

"""
Parametros
"""
epocas=20
longitud, altura = 150, 150
batch_size = 15
pasos = 12
validation_steps = 12
clases = 2
lr = 0.0004

filtrosConv1 = 32
filtrosConv2 = 64
tamano_filtro1 = (3, 3)
tamano_filtro2 = (2, 2)
tamano_pool = (2, 2)



"""
cantidad de imagenes por etiqueta

cremas= 115 
manchadas= 66
oscuras= 117

Preparacion de las imagenes
"""
entrenamiento_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

entrenamiento_generador = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical')

validacion_generador = test_datagen.flow_from_directory(
    data_validacion,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical')


""" 
creacion de red
"""
cnn = Sequential()
cnn.add(Convolution2D(filtrosConv1, tamano_filtro1, padding ="same", input_shape=(longitud, altura, 3), activation='relu'))
cnn.add(MaxPooling2D(pool_size=tamano_pool))

cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding ="same"))
cnn.add(MaxPooling2D(pool_size=tamano_pool))

cnn.add(Flatten())
cnn.add(Dense(256, activation='relu'))
cnn.add(Dropout(0.5))
cnn.add(Dense(clases, activation='softmax'))


cnn.compile(loss='categorical_crossentropy',
            optimizer=Adam(learning_rate=lr),
            metrics=['accuracy'])



cnn.fit(entrenamiento_generador,
    steps_per_epoch=pasos,  
    epochs=epocas,
    validation_data=validacion_generador,
    validation_steps=validation_steps)

target_dir = './Modelo final/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
  
cnn.save('./Modelo final/modelo.h5')
cnn.save_weights('./Modelo final/pesos.h5')