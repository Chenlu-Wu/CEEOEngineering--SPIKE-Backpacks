import hub,utime

motorC = hub.port.C.motor
motorD = hub.port.D.motor

hub.port.B.info()

def turn_left():
     print("turning left")
     for i in range(3):
          motorC.pwm(0)
          motorD.pwm(50)
          utime.sleep(0.3)
     print("finished turning left")
     motorC.pwm(0)
     motorD.pwm(0)
        
def turn_right():
     print("turning right")
     for i in range(3):
          motorC.pwm(-55)
          motorD.pwm(0)
          utime.sleep(0.3)
     print("finished turning left")
     motorC.pwm(0)
     motorD.pwm(0)

def brake():
     utime.sleep(1)


def heart():
     print("heart")
     hub.led
     for i in range(5):
          hub.led(i)
          utime.sleep(1)
          hub.display.show([hub.Image("09090:99999:99999:09990:00900"),hub.Image("01010:11111:11111:01110:00100")],fade=2,loop=1,delay=500)
     hub.display.show("")

def back_up():
     print("backing up")
     for i in range(2):
          hub.sound.beep()
          motorC.pwm(30)
          motorD.pwm(-30)
          utime.sleep(0.3)
     print("finished backing up")
     motorC.float()
     motorD.float()

def in_place_circle():
     motorC.pwm(50)
     motorD.pwm(50)
     utime.sleep(2.1)


# if info comes back with None - then you have to restart the pybaord

while True:
     try:
          value = int(hub.port.B.device.get()[0])
          print(value)
          hub.display.show(str(value))
          if (value == 1):
               turn_left()
          elif (value == 2):
               turn_right()
          elif (value == 3):
               back_up()
          elif (value == 4):
               brake()
          elif (value == 5):
               heart()
          elif (value == 6):
               in_place_circle()
          else:
               pass
          utime.sleep(0.2)
     except:
          utime.sleep(0.2)
          print("not connected")