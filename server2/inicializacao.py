from control_74595 import Control_74595
OUT = Control_74595(
    pin_RESETn=12, 
    pin_LATCH=18, 
    pin_CLOCK=16, 
    pin_DATA=22, 
    qty_ci= 16
    )
#destaiva todos os reles
OUT.write(list(map(lambda a : 0, range(len(OUT.list_data)))))
