import hub,utime

hub.port.B.info()

# if info comes back with None - then you have to restart the pybaord

while True:
     try:
          value = hub.port.B.device.get()[0]
          hub.display.show(str(value))
          if value == 9:
               hub.port.B.device.mode(0,b'toggle')
          utime.sleep(0.1)
     except:
          utime.sleep(1)

'''
hub.port.B.device.mode([(0,0),(1,0),(1,2),(3,0)])

hub.port.B.device.mode(0,b'hi there')
'''