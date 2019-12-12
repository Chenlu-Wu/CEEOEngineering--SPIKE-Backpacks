# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.


import machine, gc,utime
from pyb import LED
import sensor, image, time, math
import LPF2Class

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...

print("made it here")

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# The apriltag code supports up to 6 tag families which can be processed at the same time.
# Returned tag objects will have their tag family and id within the tag family.

tag_families = 0
tag_families |= image.TAG16H5 # comment out to disable this family
tag_families |= image.TAG25H7 # comment out to disable this family
tag_families |= image.TAG25H9 # comment out to disable this family
tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
tag_families |= image.ARTOOLKIT # comment out to disable this family

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"


print("hi")
red_led=LED(1)
red_led.on()
lpf2 = LPF2Class.LPF2(3, 'P4', 'P5')    # OpenMV
print("ugh")
lpf2.initialize()

print("initialized")

while True:
    if not lpf2.connected:
        red_led.on()
        utime.sleep(1)
        lpf2.initialize()

    else:
        red_led.off()
        while lpf2.connected:
            gc.collect()
            img = sensor.snapshot()
            for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
                img.draw_rectangle(tag.rect(), color = (255, 0, 0))
                img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
                print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
                print("APRIL TAG " + str(tag.id()))
            lpf2.send_value(int(tag.id()))
            utime.sleep(0.1)
