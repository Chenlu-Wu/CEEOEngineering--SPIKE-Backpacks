import hub,utime
motorB=hub.port.B.motor
hub.port.C.info()
while True:
     if hub.button.center.is_pressed()==True:
          break
     try:
          value = hub.port.C.device.get()[0]
          print(value)
          if (value == 1):
               motorB.pwm(25)
               hub.display.show(hub.Image.HEART_SMALL)
          elif(value==2):
               motorB.pwm(230)
               hub.display.show(hub.Image.HAPPY)
          else:
               motorB.pwm(0)
               hub.display.show(hub.Image.HEART)               
          utime.sleep(0.2)
     except:
          utime.sleep(0.2)
          print("not connected")