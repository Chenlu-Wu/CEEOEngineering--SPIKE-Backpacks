import hub,utime

print(hub.port.B.info())

while True:
     value = hub.port.B.device.get()[0]
     print(value)
     print("connected")
     if (value == 1):
          print("HAPPY")
          hub.display.show(hub.Image.HAPPY)
     elif (value == 3):
          print("SAD")
          hub.display.show(hub.Image.SAD)
     else:
          hub.display.show("-")
     utime.sleep(0.5)
