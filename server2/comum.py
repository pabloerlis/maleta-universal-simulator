from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

c_s = 7#pino 7 responsável por mudar o comum da placa
c_e = 5#pino 5 responsável por mudar o comum das placas de saídas

GPIO.setup(c_s, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(c_e, GPIO.OUT, initial=GPIO.HIGH)

def mudar_comum_saidas(nvl):
    if nvl:
        GPIO.output(c_s, GPIO.HIGH)
    else:
        GPIO.output(c_s, GPIO.LOW)


def mudar_comum_entradas(nvl):
    if nvl:
        GPIO.output(c_e, GPIO.HIGH)
    else:
        GPIO.output(c_e, GPIO.LOW)