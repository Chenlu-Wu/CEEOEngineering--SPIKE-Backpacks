import LPF2Class,gc,utime
from pyb import LED
import sensor, time, image, os, nn
import micropython

micropython.alloc_emergency_exception_buf(200)

# Simle detection using Haar Cascade + CNN.
import sensor, time, image, os, nn

sensor.reset()                          # Reset and initialize the sensor.
sensor.set_contrast(2)
sensor.set_pixformat(sensor.RGB565)     # Set pixel format to RGB565
sensor.set_framesize(sensor.QVGA)       # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)


# Load smile detection network
net = nn.load('/smile.network')

face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# loop from -10 to 10

print("hi")

red_led=LED(1)
green_led=LED(3)
blue_led=LED(2)
blue_led.on()

print("light")

#lpf2 = LPF2Class.LPF2(1, 'P1', 'P0')    # OpenMV
# note: ultrasonic connector is hardwired into UART3
lpf2 = LPF2Class.LPF2(3, 'P4', 'P5')
lpf2.initialize()

print("initialized")

while True:
    if not lpf2.connected:
        utime.sleep(1)
        lpf2.initialize()
    else:
        blue_led.off()
        while lpf2.connected:
            red_led.off()
            green_led.off()
            gc.collect()
            
            # Capture snapshot
            img = sensor.snapshot()
            
            # Find faces.
            objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)
            print("hello")
            lpf2.send_value(2)
            
            # Detect smiles
            for r in objects:
                # Resize and center detection area
                r = [r[0]+10, r[1]+25, int(r[2]*0.70), int(r[2]*0.70)]
                img.draw_rectangle(r)
                out = net.forward(img, roi=r, softmax=True)
                print("got to this point")
                blue_led.off()
                if (out[0] > 0.8):
                    lpf2.send_value(1)
                    print("SMILE")
                    green_led.on()
                else:
                    lpf2.send_value(3)
                    print("FROWN")
                    red_led.on()
                utime.sleep_ms(200)
                img.draw_string(r[0], r[1], ':)' if (out[0] > 0.9) else ':(', color=(255), scale=2)
