from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Control_74595():
    """
    Autor: Pablo Erlis
    As variáveis pin_RESETn, pin_LATCH, pin_CLOCK e pin_DATA, armazenam os números
    dos pinos utilizados no raspberry para as respectivas funções. A
    Variável qty_ci armazena a quantidade de componentes 74595 que o
    circuito possui e assume 8 saídas para cada CI.
    Substitua o comando print pelo comando do pino em questão.
    """
    def __init__(self, pin_LATCH, pin_CLOCK, pin_DATA, qty_ci=1, pin_RESETn=None, pin_ENABLEn=None):
        self.pin_ENABLEn = pin_ENABLEn
        self.pin_RESETn = pin_RESETn
        self.pin_LATCH = pin_LATCH
        self.pin_CLOCK = pin_CLOCK
        self.pin_DATA = pin_DATA
        self.qty_ci = qty_ci
        self.old_list_data = list(map(lambda a : 0, range(self.qty_ci * 8)))
        self.list_data = list(map(lambda a : 0, range(self.qty_ci * 8)))
        self.a = 1 #me apague
#--------------------------------------------------------------------
        GPIO.setup(self.pin_RESETn, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.pin_CLOCK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_LATCH, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_DATA, GPIO.OUT, initial=GPIO.LOW)

#-----------------------------------------

        #Coloque aqui em init as configurações dos pinos.
        #pin_ENABLEn -> output, low - caso não esteja já aterrado
        #pin_RESETn -> output, high
        #pin_DATA -> output, low
        #pin_CLOCK -> output, low
        #pin_LATCH -> output, low
#--------------------------------------------------------------------
    def delay(self, ms=1):
        sleep(ms/1000)
#--------------------------------------------------------------------
    def enable(self, nvl=0):
        if self.pin_ENABLEn:
            if nvl:
                GPIO.output(self.pin_ENABLEn, GPIO.HIGH)
                self.delay()
            else:
                GPIO.output(self.pin_ENABLEn, GPIO.LOW)
                self.delay()
        else:
            pass
#--------------------------------------------------------------------              
    def reset(self):
        if self.pin_RESETn:
            GPIO.output(self.pin_RESETn, GPIO.LOW)
            self.delay()
            GPIO.output(self.pin_RESETn, GPIO.HIGH)   
        else:
            pass
#--------------------------------------------------------------------          
    def data(self, nvl=0):
        if nvl:
            GPIO.output(self.pin_DATA, GPIO.HIGH)
        else:
            GPIO.output(self.pin_DATA, GPIO.LOW)
#--------------------------------------------------------------------      
    def clock(self):
        GPIO.output(self.pin_CLOCK, GPIO.HIGH)
        self.delay()
        GPIO.output(self.pin_CLOCK, GPIO.LOW)
#--------------------------------------------------------------------      
    def latch(self):
        GPIO.output(self.pin_LATCH, GPIO.HIGH)
        self.delay()
        GPIO.output(self.pin_LATCH, GPIO.LOW)
#--------------------------------------------------------------------      
    def write(self, list_data=None):
        if not list_data:
            list_data = self.list_data
        #print(self.a, self.old_list_data)#me apague
        self.old_list_data = list_data[:]
        self.reset()
        self.enable(0)
        for i in list_data:
            if i:
                self.data(1)
            else:
                self.data(0)
            self.clock()
        self.latch()
#--------------------------------------------------------------------              

'''
Exemplos de utilização:

s = Control_74595(pin_RESETn=12, pin_LATCH=18, pin_CLOCK=16, pin_DATA=22, qty_ci=1)
s.write()
'''