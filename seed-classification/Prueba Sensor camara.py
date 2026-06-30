# Librerias vision artificial y tratamiento de imagenes
import cv2
import numpy as gfg
import imutils
import os


# Libreria configuracion de raspberry
import RPi.GPIO as GPIO                    
import time
import lcdlibreria as LCD

# libreria para usar threading o hilos
# import threading 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Señales de control (boton on/off, apagado de emergencia)

on = 17
emerg = 27

GPIO.setup(on, GPIO.IN)
GPIO.setup(emerg, GPIO.IN)

# Pines y parametros infrarrojo
sen1 = 2
# sen2 = 3


GPIO.setup(sen1, GPIO.IN)
# GPIO.setup(sen2, GPIO.IN)


# Codigo principal de control 
while True:
    
       
    inicio = GPIO.input(on)
    apagado_emergencia = GPIO.input(emerg)
    sensor1 = GPIO.input(sen1) 
    # encender motores
    if inicio == True and apagado_emergencia == False:
        print('esperando sensor')
        
        if sensor1 == 1:
            print('no detecto')
        
        if sensor1 == 0:
            print('detectando')
    
    elif apagado_emergencia == True and inicio == True:
        print('apagado')
        
    else:
        print('espera por pulsador')

