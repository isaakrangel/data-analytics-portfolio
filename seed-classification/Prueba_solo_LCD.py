import time
import lcdlibreria as LCD

def main():
  #while True:
  LCD.lcd_texto("Mensaje",LCD.LINE_1)
  LCD.lcd_texto("Numero 1 " ,LCD.LINE_2)
  time.sleep(1)

  LCD.lcd_texto("Mensaje",LCD.LINE_1)
  LCD.lcd_texto("Numero 2 " ,LCD.LINE_2)
  time.sleep(1)

  LCD.lcd_texto("Mensaje",LCD.LINE_1)
  LCD.lcd_texto("Numero 3 " ,LCD.LINE_2)
  time.sleep(1)

try:
   main()
except KeyboardInterrupt:
  pass
finally:
  LCD.lcd_write(0x01, LCD.LCD_CMD)
  LCD.lcd_texto("Hasta pronto",LCD.LINE_1)
  LCD.lcd_texto("  :)  :D  " ,LCD.LINE_2)
  LCD.GPIO.cleanup()