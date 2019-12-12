import utime
import gc
from microbit import *

class LPF2Class:
     def __init__(self):
          self.connected = False
          self.tx = pin0
          self.rx = pin1

     def send_value(self, data):
          value = (data & 0xFF)
          payload = bytes([0xC0, value, 0xFF ^ 0xC0 ^ value])
          size = uart.write(payload)
          if not size:
               self.connected = False

     def initialize(self):
          display.show(1)
          self.tx.write_digital(0)
          utime.sleep_ms(500)
          self.tx.write_digital(1)
          uart.init(baudrate=2400, bits=8, parity=None, stop=1,tx = pin0, rx = pin1)
          uart.write(b'\x00')
          uart.write(b'\x40\x23\x9C')  #CMD_TYPE (x40)  Type   checksum
          uart.write(b'\x49\x00\x00\xB6')  #CMD_MODE (x49)  # Modes  # Views   checksum
          uart.write(b'\x52\x00\xC2\x01\x00\x6E')  #CMD_SPEED (x52)  baud (LSB first)   checksum
          uart.write(b'\x5F\x00\x00\x00\x02\x00\x00\x00\x02\xA0')  #CMD_VERSION (x5F)  Hardware_V  Software_V   checksum
          uart.write(b'\xA0\x00\x4C\x50\x46\x32\x2D\x44\x45\x54\x45\x43\x54\x00\x00\x00\x00\x00\x1D')  #CMD_INFO|bytes|mode  0 name 0   checksum
          uart.write(b'\x98\x01\x00\x00\x00\x00\x00\x00\x20\x41\x07')  #CMD_INFO|3|mode  1 (raw) raw_min  raw_max   checksum
          uart.write(b'\x98\x02\x00\x00\x00\x00\x00\x00\xC8\x42\xEF')  #CMD_INFO|3|mode  2 (pct) pct_min  pct_max   checksum
          uart.write(b'\x98\x03\x00\x00\x00\x00\x00\x00\x20\x41\x05')  #CMD_INFO|3|mode  3 (SI) si_min  si_max   checksum
          uart.write(b'\x80\x04\x00\x7B')  #CMD_INFO|size|mode  0,4,symbol   checksum
          uart.write(b'\x88\x05\x10\x00\x62')  #CMD_INFO|1|mode  5 (FM) Function Map-In   -out   checksum
          uart.write(b'\x90\x80\x01\x00\x03\x00\xED')  #CMD_INFO|2|mode  x80 sample_size   Data_type   Figures   Decimals   checksum
          utime.sleep_ms(5)
          uart.write(b'\x04') 
          display.show(4) 
          starttime = utime.ticks_ms()
          currenttime = starttime
          while (currenttime-starttime) < 2000:
               utime.sleep_ms(5)
               data = uart.read(uart.any())
               if data.find(b'\x04') >= 0:
                    self.connected = True
                    display.show(5) 
                    currenttime = starttime+3000 
               else:
                    self.connected = True
                    currenttime = utime.ticks_ms()
          self.tx.write_digital(0)
          utime.sleep_ms(10)
          uart.init(baudrate=115200, bits=8, parity=None, stop=1,tx = pin0, rx = pin1)
          self.send_value(2)
i = 0
lpf2 = LPF2Class()
lpf2.initialize()
#display.show(lpf2.connected)

import microbit


while True:
    if not lpf2.connected:
         print('not connected')
         utime.sleep(1)
         lpf2.initialize()
    else:
        while lpf2.connected:
            gc.collect()

            val = accelerometer.get_x() # checking the value the sensor is at 
            
            # X POSITIVE
            if val > -12 and val <= 12 :    
                num = 0                                                                        
          
            if val > 12  and val <=  200 :
                num = 10
                
            if val > 200 and val <= 300 :
                num = 10
                
            if val > 300 and val <= 400 :
                num = 15
                
            if val > 400 and val <= 500 :
                num = 15
                
            if val > 500 and val <= 600 :
                num = 20
                
            if val > 600 and val <= 700 :
                num = 20
                
            if val > 700 and val <= 800 :
                num = 30
            
            if val > 800 and val < 900 :
                num = 30
                
            if val > 1000 :
                num = 40
                
            # X NEGATIVE
            if val < -1000 :    
                num = -40                                                                      
          
            if val > -900 and val <= -800  :
                num = -30
                
            if val > -800 and val <= -700 :
                num = -30
                
            if val > -700 and val <= -600 :
                num = -20
                
            if val > -600 and val <= -500 :
                num = -20
                
            if val > -500 and val <= -400 :
                num = -15
                
            if val > -400 and val <= -300 :
                num = -15
                
            if val > -300 and val <= -200 :
                num = -10
            
            if val > -200 and val < -12 :
                num = -10
            
            valy = accelerometer.get_y() # checking the value the sensor is at 
            
            # Y POSITIVE
            if valy > -12 and valy <= 12 :    
                num2 = 0                                                                      
          
            if valy > 12  and valy <=  200 :
                num2 = 10
            
            if valy > 200 and valy <= 300 :
                num2 = 10
                
            if valy > 300 and valy <= 400 :
                num2 = 15
                
            if valy > 400 and valy <= 500 :
                num2 = 15
                
            if valy > 500 and valy <= 600 :
                num2 = 20
                
            if valy > 600 and valy <= 700 :
                num2 = 20
                
            if valy > 700 and valy <= 800 :
                num2 = 30
            
            if valy > 800 and valy < 900 :
                num2 = 30
                
            if valy > 1000 :
                num2 = 40
                
            # Y NEGATIVE
            if valy < -1000 :  
                num2 = -40                                                                   
          
            if valy > -900 and valy <= -800  :
                num2 = -30
                
            if valy > -800 and valy <= -700 :
                num2 = -30
                
            if valy > -700 and valy <= -600 :
                num2 = -20
                
            if valy > -600 and valy <= -500 :
                num2 = -20
                
            if valy > -500 and valy <= -400 :
                num2 = -15
                
            if valy > -400 and valy <= -300 :
                num2 = -15
                
            if valy > -300 and valy <= -200 :
                num2 = -10
            
            if valy > -200 and valy < -12 :
                num2 = -10
            
            a=1
            b=2
            lpf2.send_value(a) #trigger for x values 
            utime.sleep_ms(100)
            lpf2.send_value(num)
            utime.sleep_ms(200)
            lpf2.send_value(b) #trigger for y values
            utime.sleep_ms(100)
            lpf2.send_value(num2)
            utime.sleep_ms(200)


        utime.sleep_ms(200)