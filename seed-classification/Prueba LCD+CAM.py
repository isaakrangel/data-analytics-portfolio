import time
import lcdlibreria as LCD
# Librerias vision artificial y tratamiento de imagenes
import cv2
import numpy as gfg
import imutils
import os



from PIL import Image, ImageDraw

# Libreria configuracion de raspberry
import RPi.GPIO as GPIO                    
import time
import lcdlibreria as LCD

# libreria para usar threading o hilos
# import threading 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#crear carpeta y permitir capturar con la camara

Datos = 'CAM'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)

# camaras de captura
cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2,cv2.CAP_DSHOW)

# coordenadas de recorte
x1, y1 = 20, 0 
x2, y2 = 450, 380
longitud, altura = 150, 150
# Localizacion de la semilla aleatoria para efecto de contorno
seed = (0, 0)
# Valor de pixel con el que se reemplazará el entorno de la silueta
rep_value = (0, 0, 0, 0)


# Señales de control (boton on/off, apagado de emergencia)
inicio = GPIO.setup(17, GPIO.input)
apagado_emergencia = GPIO.setup(27, GPIO.input)

# contadores para visualizar en el LCD
countC1 = 0;       # contador de imagenes tomadas por la camara1
countC2 = 0;       # contador de imagenes tomadas por la camara2
semillas = 0;      # total semillas detectadas 
Expulsadas = 0;    # total semillas expulsadas
Seleccionadas = 0;  # total semillas selccionadas o claras
tiempoMotor = 0;    #tiempo de funcionamiento Motor dosificador 2

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


def main():
  #while True:
  LCD.lcd_texto("Semillas 1:"+countC1,LCD.LINE_1)
  LCD.lcd_texto("Semillas 2:"+countC2,LCD.LINE_2)
   
try: 
    while True:
        
        ret1, frame1 = cap1.read()
        if ret1 == False: break
        
        ret2, frame2 = cap2.read()
        if ret2 == False: break
        
          
        # encender motores
        if inicio == 1 and apagado_emergencia == 0:
            
            main()
            # Encender_Motores_Banda()
            # Encender_Motores_DosificadorGD()
            # print("motores funcionando") 

            k = cv2.waitKey(1)
            if k == ord('s'):
                camara(1)
                countC1 = countC1 + 1
            if k == ord('d'):
                camara(2)
                countC2 = countC2 + 1
            
        
        elif apagado_emergencia() == 1 and inicio == 1:
          
            LCD.lcd_write(0x01, LCD.LCD_CMD)
            LCD.lcd_texto("Hasta pronto",LCD.LINE_1)
            LCD.lcd_texto("  :)  :D  " ,LCD.LINE_2)
            LCD.GPIO.cleanup()
         
except KeyboardInterrupt:
    GPIO.cleanup()
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()