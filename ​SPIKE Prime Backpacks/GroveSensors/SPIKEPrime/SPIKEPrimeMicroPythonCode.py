#Tufts University Center for Engineering Education and Outreach
#Summer 2019
#Main Contributors: Charvady Hak, Grace Kayode
#This code allows the SPIKE Prime to continously try to read any data that is
#coming from the backpack.

#change ports as needed

import hub,utime

hub.port.B.info()

# if info comes back with None - then you have to restart the pyboard

while True:
     try:
          value = hub.port.B.device.get()[0]
          print(value)
          hub.display.show(str(value/10))
          #print(value)

          hub.port.A.motor.pwm(int(value)) # powers motor from 0 - 90
      #    if value == 9:
        #  hub.port.B.device.mode(0,b'toggle')
          utime.sleep(0.2)
     except:
          utime.sleep(1)

