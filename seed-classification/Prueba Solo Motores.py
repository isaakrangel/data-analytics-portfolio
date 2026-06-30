# Librerias vision artificial y tratamiento de imagenes
import cv2
import numpy as gfg
import imutils
import os

# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# from tensorflow.keras.models import load_model

# from PIL import Image, ImageDraw

# Libreria configuracion de raspberry
import RPi.GPIO as GPIO                    
import time

#libreria LCD
sys.path.append('/home/isaakrangel/lcd')
import lcd
lcd.lcd_init()

# libreria para usar threading o hilos
# import threading 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#cargar modelos y pesos de entrenamiento
# modelo = './modelo/modelo.h5'
# pesos_modelo = './modelo/pesos.h5'
# cnn = load_model(modelo)
# cnn.load_weights(pesos_modelo)

#crear carpeta y permitir capturar con la camara
# Datos = 'sacha inchi'
# if not os.path.exists(Datos):
#     print('Carpeta creada: ',Datos)
#     os.makedirs(Datos)

# camaras de captura
# cap1 = cv2.VideoCapture(0)
# cap2 = cv2.VideoCapture(2)

# coordenadas de recorte
# x1, y1 = 30, 0 
# x2, y2 = 420, 350
# longitud, altura = 150, 150



# Señales de control (boton on/off, apagado de emergencia)
on = 17
emerg = 27

GPIO.setup(on, GPIO.IN)
GPIO.setup(emerg, GPIO.IN)

# Pines y parametros infrarrojo
sen1 = 2
sen2 = 3

GPIO.setup(sen1, GPIO.IN)
GPIO.setup(sen2, GPIO.IN)

# Pines y parametros motores y valvula
    # motores dosificador
en1 = 19			
in11 = 23
in13 = 24
in14 = 4
    # motores banda
en2 = 13
in21 = 5
in23 = 6
    # valvulas neumaticas
in31 = 10
in33 = 9

    # define salidas motores
#pines motores dosificador
GPIO.setup(en1, GPIO.OUT)  # pines enable puente H de motores de dosificadores
GPIO.setup(in11, GPIO.OUT)
GPIO.setup(in13, GPIO.OUT)
GPIO.setup(in14, GPIO.OUT) 
#pines motores banda
GPIO.setup(en2, GPIO.OUT) # pines enable puente H de motores de bandas
GPIO.setup(in21, GPIO.OUT)
GPIO.setup(in23, GPIO.OUT)
#pines valvulas
GPIO.setup(in31, GPIO.OUT)
GPIO.setup(in33, GPIO.OUT)

#Define las salidas PWM de motores dosificador, banda y valvulas
pwm_1 = GPIO.PWM(en1,255) 
pwm_2 = GPIO.PWM(en2,255)

# inicializa los pmw
pwm_1.start(0)
pwm_2.start(0)





# Funciones de encendido y apagado puentes H
def Encender_Motores_DosificadorGD():
        GPIO.output(in11,True)      
        GPIO.output(in13,True)
        GPIO.output(in14,False)

def Encender_Motores_DosificadorGL():
        GPIO.output(in11,True)      
        GPIO.output(in13,False)
        GPIO.output(in14,True)

def Encender_Motores_Banda():
        GPIO.output(in21,True)
        GPIO.output(in23,True)

def Apagar_Motores_Dosificador():
        GPIO.output(in11,False)
        GPIO.output(in13,False)
        GPIO.output(in14,False)

def Apagar_Motores_Banda():
        GPIO.output(in21,False)
        GPIO.output(in23,False)
       
def Encender_Valvulas(hilo):
    
    if hilo==1:
        GPIO.output(in31,True)
    if hilo==2:
        GPIO.output(in33,True)        
 
def Apagar_Valvulas(hilo):
    
    if hilo==1:
        GPIO.output(in31,False)
    if hilo==2:
        GPIO.output(in33,False)
    else:
        GPIO.output(in33,False)
        GPIO.output(in31,False)
        
# Funcion de prediccion dependiendo el hilo
  
# def predict(file,hilo):
#     x = load_img(file, target_size=(longitud, altura))
#     x = img_to_array(x)
#     x = gfg.expand_dims(x, axis=0)
#     array = cnn.predict(x)
#     result = array[0]
#     answer = gfg.argmax(result)

#     if answer == 0:
#         print("pred: Oscura")
#         Seleccionadas = Seleccionadas + 1 

#     elif answer == 1:
#         print("pred: Clara")
#         time.sleep(5.2)   #Tiempo para llegar a valvula
#         Encender_Valvulas(hilo)
#         Expulsadas = Expulsadas + 1
#         time.sleep(1)   #Tiempo funcionando valvula
#         Apagar_Valvulas(hilo)

#     return answer

# def camara(hilo):
     
#     # codigo prediccion
#     # tomar foto y proceso de prediccion
#     if hilo==1:
#         image = frame1.copy()
#     elif hilo==2:
#         image = frame2.copy()
           
#     objeto = image       
#     objeto = objeto[y1:y2,x1:x2]
#     objeto = cv2.resize(objeto,(460,345),interpolation=cv2.INTER_CUBIC)
#     cv2.imwrite(Datos+'/objeto_{}.jpg'.format(hilo),objeto)
#     print('Imagen guardada:'+'/objeto_{}.jpg'.format(hilo))
            
    # predict('./sacha ichi/objeto_{}.jpg'.format(hilo), hilo)     

# contadores para visualizar en el LCD
countC1 = 0;       # contador de imagenes tomadas por la camara1
countC2 = 0;       # contador de imagenes tomadas por la camara2
semillas = 0;      # total semillas detectadas 
Expulsadas = 0;    # total semillas expulsadas
Seleccionadas = 0;  # total semillas selccionadas o claras
tiempoMotor = 0;    #tiempo de funcionamiento Motor dosificador 2


# Codigo principal de control 
while True:
    
    # ret1, frame1 = cap1.read() #verificacion de camaras funcionando
    # if ret1 == False: break
    
    # ret2, frame2 = cap2.read()
    # if ret2 == False: break
   
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string("Clasificador", 2)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string("Inicializando", 2)

    time.sleep(5)
    #lectura de señales de entrada pulsadores y sensores infrared
    inicio = GPIO.input(on)
    apagado_emergencia = GPIO.input(emerg)
    sensor1 = GPIO.input(sen1)
    sensor2 = GPIO.input(sen2)
    
    if inicio == True and apagado_emergencia == False:
        time.sleep(0.3)
       # encender motores
        Encender_Motores_Banda()
        Encender_Motores_DosificadorGD()
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("SS:"+str(semillas)+ "SE:"+ str(Expulsadas), 1)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string("SB1:"+str(countC1)+ "SB2:"+str(countC2), 1)

        if sensor1 == 0:
            time.sleep(3.2)#Tiempo para llegar a la camara 1
            semillas = semillas + 1
            countC1 = countC1 +1
            lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
            lcd.lcd_string("SS:"+str(semillas)+ "SE:"+ str(Expulsadas), 1)
            lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
            lcd.lcd_string("SB1:"+str(countC1)+ "SB2:"+str(countC2), 1)
            # camara(1)
        
        if sensor2 == 0:
            time.sleep(3.2) #tiempo para llegar a la camara 2
            semillas = semillas + 1 
            countC2 = countC2 + 1
            lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
            lcd.lcd_string("SS:"+str(semillas)+ "SE:"+ str(Expulsadas), 1)
            lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
            lcd.lcd_string("SB1:"+str(countC1)+ "SB2:"+str(countC2), 1)
            # camara(2)
    
    elif apagado_emergencia == True and inicio == True:
            time.sleep(0.3)
            lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
            lcd.lcd_string("SS:"+str(semillas)+ "SE:"+ str(Expulsadas), 1)
            lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
            lcd.lcd_string("SB1:"+str(countC1)+ "SB2:"+str(countC2), 1)
            Apagar_Motores_Banda()
            Apagar_Motores_Dosificador()
            Apagar_Valvulas()
        
    else:
        pwm_1.stop()
        pwm_2.stop()
        Apagar_Valvulas()
        #finalizar pwm / motores apagados 

lcd.GPIO.cleanup()
cap1.release()
cap2.release()
# cv2.destroyAllWindows()
        



    