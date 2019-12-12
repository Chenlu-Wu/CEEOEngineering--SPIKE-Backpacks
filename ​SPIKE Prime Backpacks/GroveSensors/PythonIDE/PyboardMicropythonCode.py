#Tufts University Center for Engineering Education and Outreach
#Summer 2019
#Main Contributors: Charvady Hak, Grace Kayode
#This code processes the sensor data in the Grove Backpack and sends it to the SPIKE Prime.

import gc,utime
import pyb, micropython
from LPF2Class import LPF2

micropython.alloc_emergency_exception_buf(200)

red_led=pyb.LED(1)
green_led = pyb.LED(2)
red_led.on()

lpf2 = LPF2(1, 'Y1', 'Y2', timer = 4, freq = 5)  
lpf2.initialize()
adc = pyb.ADC('X1')

val = 0
num = 0 
base = 410

# Loop
while True:
    if not lpf2.connected:
        lpf2.sendTimer.callback(None)
        red_led.on()
        utime.sleep_ms(200)
        lpf2.initialize()
    else:
        red_led.off()
        val = adc.read()
        #print(val)
        if val > 0 and val <= base :
             num = 1
        
        if val > 411  and val <= (base*2) :
             num = 2
            
        if val > (base*2) and val < (base*3) :
             num = 3
            
        if val > (base*3) and val < (base*4) :
             num = 4
            
        if val > (base*4) and val < (base*5) :
             num = 5
            
        if val > (base*5) and val < (base*6) :
             num = 6
            
        if val > (base*6) and val < (base*7) :
             num = 7
            
        if val > (base*7) and val < (base*8) :
             num = 8
        
        if val > (base*8) and val < (base*9) :
             num = 9
            
        if val > (base*9) and val < (base*10) :
             num = 10
            
        # val = num
        print(num)
        z = num*10
        lpf2.load_payload(z)    #sends a motor speed value 
        data = lpf2.readIt()
        if len(data) > 0:
            print(data)
            if data.find(b'toggle')>=0:
                 green_led.toggle()

        utime.sleep_ms(200)