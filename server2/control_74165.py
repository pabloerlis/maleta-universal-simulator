from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Control_74165():
    """ SNx4HC165 8-Bit Parallel-Load Shift Registers
    As variáveis pin_ENABLEn, pin_LATCHn, pin_CLOCK e pin_DATA armazenam os números
    dos pinos utilizados para as respectivas funções. A
    Variável qty_ci armazena a quantidade de componentes 74165 que o
    circuito possui e assume 8 entradas para cada CI.
    """
    def __init__(self, pin_LATCHn, pin_CLOCK, pin_DATA, qty_ci=1, pin_ENABLEn=None):
        self.pin_ENABLEn = pin_ENABLEn
        self.pin_LATCHn = pin_LATCHn
        self.pin_CLOCK = pin_CLOCK
        self.pin_DATA = pin_DATA
        self.qty_ci = qty_ci
        self.list_data = list(map(lambda a : 0, range(self.qty_ci * 8)))
#--------------------------------------------------------------------
        GPIO.setup(self.pin_ENABLEn, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_DATA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pin_CLOCK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pin_LATCHn, GPIO.OUT, initial=GPIO.HIGH)
        #Coloque aqui em init as configurações dos pinos.
        #pin_ENABLEn -> output, low - caso não esteja aterrado
        #pin_DATA -> input, pull_down
        #pin_CLOCK -> output, low
        #pin_LATCHn -> output, high           
#--------------------------------------------------------------------
    def delay(self, ms=2):
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
    def clock(self):
        GPIO.output(self.pin_CLOCK, GPIO.HIGH)
        self.delay()
        GPIO.output(self.pin_CLOCK, GPIO.LOW)          
#--------------------------------------------------------------------      
    def latch(self):
        GPIO.output(self.pin_LATCHn, GPIO.LOW)
        self.delay()
        GPIO.output(self.pin_LATCHn, GPIO.HIGH)
#--------------------------------------------------------------------        
    def data(self):
        return not GPIO.input(self.pin_DATA)#Para lógica direta remova o operador not, simplesmente.
#--------------------------------------------------------------------  
    def read(self):
        old_list_data = self.list_data[:]
        self.enable()
        self.latch()
        for k in range(len(self.list_data)):
            if not k == 0:
                self.clock()
                self.list_data[k] = self.data()
            else:
                self.list_data[0] = self.data()
        if old_list_data != self.list_data:
            #Só retorna a lista de dados se eles forem diferentes do anteriormente enviado, ou seja, somente se houver atualização da leitura.
            return self.list_data 
'''
Exemplos de utilização:

e = Control_74165(pin_ENABLEn=36, pin_LATCHn=38, pin_CLOCK=40, pin_DATA=32, qty_ci=2)
while True:
    if e.read():
        print(e.list_data)
        e.delay(100)
'''