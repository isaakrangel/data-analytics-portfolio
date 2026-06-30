#Codigo de prueba funcionamiento motores y valvulas
import os
import cv2
# Libreria configuracion de raspberry
import RPi.GPIO as GPIO                    
import time

import sys
sys.path.append('/home/isaakrangel/lcd')
import lcd

lcd.lcd_init()
# libreria para usar threading o hilos
# import threading 

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)


# Señales de control (boton on/off, apagado de emergencia)

on = 17
emerg = 27

GPIO.setup(on, GPIO.IN)
GPIO.setup(emerg, GPIO.IN)

count = 1

while True:
    
    inicio = GPIO.input(on)
    apagado_emergencia = GPIO.input(emerg)
    # encender motores
    if inicio == True and apagado_emergencia == False:
        count = count+1
        print('funcionando')
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Funcionando:"+str(count), 2)

       
            
    elif  apagado_emergencia == True and inicio == True:
        print('apagado')
        count = count-1
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Apagado:"+str(count), 2)

    else:
        #finalizar pwm / motores apagados
        print('esperando pulsador')
        

        