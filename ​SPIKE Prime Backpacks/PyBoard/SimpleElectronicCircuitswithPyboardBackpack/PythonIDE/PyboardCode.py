import gc,utime
import pyb, micropython
from LPF2Class import LPF2

micropython.alloc_emergency_exception_buf(200)

red_led=pyb.LED(1)
green_led = pyb.LED(2)
red_led.on()

lpf2 = LPF2(3, 'Y9', 'Y10', timer = 4, freq = 5)    # Pyboard
lpf2.initialize()
value = 0

led = pyb.Pin('X3',pyb.Pin.OUT)
adc = pyb.ADC(pyb.Pin.board.X4)    

value = 0

# Loop
while True:
     if not lpf2.connected:
          lpf2.sendTimer.callback(None)
          red_led.on()
          utime.sleep_ms(200)
          lpf2.initialize()
     else:
          red_led.off()
          value = int(adc.read()/200)
          print(value)
          if value<2:
               led.high()
          else:
               led.low()
          lpf2.load_payload(value)
          data = lpf2.readIt()
          if len(data) > 0:
               print(data)
               if data.find(b'toggle')>=0:
                    green_led.toggle()

          utime.sleep_ms(200)

