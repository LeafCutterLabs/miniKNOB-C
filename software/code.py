import board
import digitalio
import time
from adafruit_debouncer import Debouncer
import neopixel

pixels = neopixel.NeoPixel(
    board.D2, 12, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB
)

pixelcolor = [100,100,100,100,100,100,100,100,100,100,100,100]

def pixel_display():
    for x in range(0,len(pixelcolor)):
       pixels[x]=(pixelcolor[x],0,0)

pixelposition = 0

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

#button setup
button = digitalio.DigitalInOut(board.D5)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
switch = Debouncer(button)

#encoder setup
rot_a = digitalio.DigitalInOut(board.D9)
rot_a.direction = digitalio.Direction.INPUT
rot_a.pull = digitalio.Pull.UP
rotA = Debouncer(rot_a)

rot_b = digitalio.DigitalInOut(board.D10)
rot_b.direction = digitalio.Direction.INPUT
rot_b.pull = digitalio.Pull.UP
rotB = Debouncer(rot_b)

# the counter counts up and down, it can roll over! 16-bit value
encoder_counter = 0

while True:
    pixel_display()
    pixels[int(encoder_counter/4)]=(0,0,255)
    pixels.show()
    switch.update()
    rotA.update()
    rotB.update()

    #truth table
    #CW
    #[1,1][1,0][0,0][0,1][1,1]
    #CCW
    #[1,1][0,1][0,0][1,0][1,1]
    if rotA.fell:
        if rotB.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -48:
                encoder_counter = 0
            print("%d ccw" % encoder_counter)
        elif not rotB.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 48:
                encoder_counter = 0
            print("%d cw" % encoder_counter)
    if rotB.fell:
        if rotA.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 48:
                encoder_counter = 0
            print("%d cw" % encoder_counter)
        elif not rotA.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -48:
                encoder_counter = 0
            print("%d ccw" % encoder_counter)
    """
    if rotA.rose:
        if rotB.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 48:
                encoder_counter = 0
            print("%d cw" % encoder_counter)
        elif not rotB.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -48:
                encoder_counter = 0
            print("%d ccw" % encoder_counter)
    if rotB.rose:
        if rotA.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -48:
                encoder_counter = 0
            print("%d ccw" % encoder_counter)
        elif not rotA.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 48:
                encoder_counter = 0
            print("%d cw" % encoder_counter)
    """
    # Button was 'just pressed'
    if switch.fell:
        print("Button pressed!")
        led.value = True
        encoder_counter = 0
        print ("reset encoder",    encoder_counter)
    if switch.rose:
        print("Button Released!")
        led.value = False