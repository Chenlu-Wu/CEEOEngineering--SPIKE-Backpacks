import machine, utime, gc
import math, struct
import utime,pyb

CMD_Type = 0x40   # set sensor type command
CMD_Mode = 0x49   # set mode type command
CMD_Baud = 0x52   # set the transmission baud rate
CMD_Vers = 0x5F   # set the version number
CMD_ModeInfo = 0x80  # name command

NAME,RAW,Pct,SI,SYM,FCT, FMT = 0x0,0x1,0x2,0x3,0x4,0x5, 0x80
DATA8,DATA16,DATA32,DATAF = 0,1,2,3  # Data type codes
ABSOLUTE,RELATIVE,DISCRETE = 16,8,4

# Name, Format [# datasets, type, figures, decimals], raw [min,max], Percent, SI, Symbol,functionMap, view
mode0 = ['LPF2-DETECT',[1,DATA8,3,0],[0,10],[0,100],[0,10],'',[ABSOLUTE,0],True]
mode1 = ['LPF2-COUNT',[1,DATA32,4,0],[0,100],[0,100],[0,100],'CNT',[ABSOLUTE,0],True]
mode2 = ['LPF2-CAL',[3,DATA16,3,0],[0,1023],[0,100],[0,1023],'RAW',[ABSOLUTE,0],False]
modes = [mode0,mode1,mode2]

class LPF2(object):
     def __init__(self, uartChannel, txPin, rxPin, timer = 4, freq = 5):
          self.txPin = txPin
          self.rxPin = rxPin
          self.uart = machine.UART(uartChannel)
          self.txTimer = timer
          self.connected = False
          self.payload = bytearray([])
          self.freq = freq
          self.oldbuffer =  bytes([])

     def load_payload(self,data):
          value = (data & 0xFF)
          self.payload = bytes([0xC0, value, 0xFF ^ 0xC0 ^ value])
          
     def sendCall(self, timerInfo):
          if self.connected:
               size = self.writeIt(self.payload)
               if not size: self.connected = False

     def writeIt(self,array):
          #print(binascii.hexlify(array))
          return self.uart.write(array)
          
     def readIt(self):
          if self.uart.any() == 0:    # if nothing is there then leave
               return b''
          if not self.waitFor(b'\x02'):
               return b''
          status, data = self.waitFor(b'\x02')
          if not status:    # make sure it is long enough to give data
               return b''
          #data = data[0:-1] if (data[-1] == 2) else data
          loc = data.find(b'F')
          if (loc >= 0) and (len(data) > 5):       
               mode = data[1]
               something = data[2]
               chksm = data[-1]
               counter = data[3]
               payload = data[4:-1]
               chksm2 = 0xFF ^ counter
               for i in payload:
                    chksm2 ^= i
               if not(chksm == chksm2):
                    print('checksum error   read %d, measured %d' % (chksm,chksm2))
          else:
               payload = b''
          return payload

     def waitFor (self, char, timeout = 2):
          starttime = utime.time()
          currenttime = starttime
          status = False
          buffer = self.oldbuffer
          while (currenttime-starttime) < timeout:
               utime.sleep_ms(5)
               data = self.uart.read(self.uart.any())   #self.readIt()
               buffer += data
               if data.find(char) >= 0:
                    status = True
                    reply = buffer.split(char)
                    buffer = reply[0]
                    self.oldbuffer = reply[-1]   # dumps any extra readings
                    currenttime = starttime + timeout   # stop the loop
               else:
                    currenttime = utime.time()
          return status, buffer

          
     def addChksm(self,array):
          chksm = 0
          for b in array:
               chksm ^= b
          chksm ^= 0xFF
          array.append(chksm)  
          return array
          
     def init(self):
          self.tx = machine.Pin(self.txPin, machine.Pin.OUT)
          self.rx = machine.Pin(self.rxPin, machine.Pin.IN)
          self.tx.value(0)
          utime.sleep_ms(500)
          self.tx.value(1)
          self.uart.init(baudrate=2400, bits=8, parity=None, stop=1)
          self.writeIt(b'\x00')

     def type(self,sensorType):
          return self.addChksm(bytearray([CMD_Type, sensorType]))

     def defineBaud(self,baud):
          rate = baud.to_bytes(4, 'little')
          return self.addChksm(bytearray([CMD_Baud]) + rate) 

     def defineVers(self,hardware,software):
          hard = hardware.to_bytes(4, 'big')
          soft = software.to_bytes(4, 'big')
          return self.addChksm(bytearray([CMD_Vers]) + hard + soft)
          
     def padString(self,string, num, startNum):
          reply = bytearray([startNum])  # start with name
          reply += string
          exp = math.ceil(math.log(len(string),2)) if len(string)>0 else 0  # find the next power of 2
          size = 2**exp
          exp = exp<<3
          length = size - len(string)
          for i in range(length):
               reply += bytearray([0])
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num]) + reply)

     def buildFunctMap(self,mode, num, Type):
          exp = 1 << 3
          mapType = mode[0]
          mapOut = mode[1]
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num, Type, mapType, mapOut]))

     def buildFormat(self,mode, num, Type):
          exp = 2 << 3
          sampleSize = mode[0] & 0xFF
          dataType = mode[1] & 0xFF
          figures = mode[2] & 0xFF
          decimals = mode[3] & 0xFF
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num, Type, sampleSize, dataType,figures,decimals]))
     
     def buildRange(self,settings, num, rangeType):
          exp = 3 << 3
          minVal = struct.pack('<f', settings[0])
          maxVal = struct.pack('<f', settings[1])
          return self.addChksm(bytearray([CMD_ModeInfo | exp | num, rangeType]) + minVal + maxVal)

     def defineModes(self,modes):
          length = (len(modes)-1) & 0xFF
          views = 0
          for i in modes:
               if (i[7]):
                    views = views + 1
          views = (views - 1) & 0xFF
          return self.addChksm(bytearray([CMD_Mode, length, views]))
          
     def setupMode(self,mode,num):
          self.writeIt(self.padString(mode[0],num,NAME)) # write name
          self.writeIt(self.buildRange(mode[2], num, RAW)) # write RAW range
          self.writeIt(self.buildRange(mode[3], num, Pct)) # write Percent range
          self.writeIt(self.buildRange(mode[4], num, SI)) # write SI range
          self.writeIt(self.padString(mode[5],num,SYM)) # write symbol
          self.writeIt(self.buildFunctMap(mode[6],num, FCT)) # write Function Map
          self.writeIt(self.buildFormat(mode[1],num, FMT)) # write format

     def initialize(self):
          self.connected = False
          self.sendTimer = pyb.Timer(self.txTimer, freq = self.freq)  # default is 200 ms
          self.init()
          self.writeIt(self.type(61))  # set type to 61
          self.writeIt(self.defineModes(modes))  # tell how many modes 
          self.writeIt(self.defineBaud(115200))
          self.writeIt(self.defineVers(2,2))

          num = len(modes) - 1
          for mode in reversed(modes):
               self.setupMode(mode,num)
               num -= 1
               utime.sleep_ms(5)
               
          self.writeIt(b'\x04')  #ACK
          # Check for ACK reply
          self.connected, buffer = self.waitFor(b'\x04')
          print('Success' if self.connected else 'Failed')

          # Reset Serial to High Speed
          # pull pin low
          self.uart.deinit()
          if self.connected:
               tx = machine.Pin(self.txPin, machine.Pin.OUT)
               tx.value(0)
               utime.sleep_ms(10)
               
               #change baudrate
               self.uart.init(baudrate=115200, bits=8, parity=None, stop=1)
               self.load_payload(2)
          
               #start callback  - MAKE SURE YOU RESTART THE CHIP EVERY TIME (CMD D) to kill previous callbacks running
               self.sendTimer.callback(self.sendCall)
          return
