import hub,utime

hub.port.B.info()

while True:
  try:
    value = hub.port.B.device.get()[0]
    if value == 1:
      utime.sleep(0.2)
      value2 = hub.port.B.device.get()[0] # x_axis values
      print(value2)
      print('d')
      hub.port.D.motor.pwm(value2) 
      utime.sleep(0.2)
    elif value == 2:
      utime.sleep(0.2)
      value3 = hub.port.B.device.get()[0] #y_axis values
      print(value3)
      print('c')
      hub.port.C.motor.pwm(value3)
      utime.sleep(0.2)
  except:
    utime.sleep(0.2)
    print("not connected")
    
utime.sleep(0.21)
