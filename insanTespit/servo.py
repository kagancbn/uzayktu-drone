import RPi.GPIO as GPIO
import time

def runServo():
    # GPIO numaralandırılması
    GPIO.setmode(GPIO.BOARD)

    # sinyal pinini tanımla
    GPIO.setup(11,GPIO.OUT)
    servo1 = GPIO.PWM(11,50) # sinyal 50Hz

    # PWM yi çalıştır
    servo1.start(0)


    angle = float(160)
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(1)
    servo1.ChangeDutyCycle(0)
    time.sleep(3)
    '''
    angle = float(160)
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(1)
    servo1.ChangeDutyCycle(0)
    '''
    # servoyu temizle
    servo1.stop()
    GPIO.cleanup()
    print("Goodbye!")
