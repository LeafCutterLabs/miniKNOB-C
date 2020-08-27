import board
import digitalio
import time
from adafruit_debouncer import Debouncer
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import usb_hid

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

#button setup
button = digitalio.DigitalInOut(board.D10)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
switch = Debouncer(button)

#encoder setup
rot_a = digitalio.DigitalInOut(board.D9)
rot_a.direction = digitalio.Direction.INPUT
rot_a.pull = digitalio.Pull.UP
rotA = Debouncer(rot_a)

rot_b = digitalio.DigitalInOut(board.D8)
rot_b.direction = digitalio.Direction.INPUT
rot_b.pull = digitalio.Pull.UP
rotB = Debouncer(rot_b)

keyboard = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# the counter counts up and down, it can roll over! 16-bit value
encoder_counter = 0

clockWISE = False
rotmove = False

while True:
    switch.update()
    rotA.update()
    rotB.update()

    #truth table
    #CW
    #[1,1][1,0][0,0][0,1][1,1]
    #CCW
    #[1,1][0,1][0,0][1,0][1,1]
    if rotA.fell:
        rotmove=True
        if not rotB.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 24:
                encoder_counter = 0
            print("%d AF-CW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = True
        if rotB.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -24:
                encoder_counter = 0
            print("%d AF-CCW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = False
    if rotB.fell:
        rotmove=True
        if not rotA.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -24:
                encoder_counter = 0
            print("%d BF-CCW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = False
        if rotA.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 24:
                encoder_counter = 0
            print("%d BF-CW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = True
    if rotA.rose:
        rotmove=True
        if not rotB.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -24:
                encoder_counter = 0
            print("%d AR-CCW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = False
        if rotB.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 24:
                encoder_counter = 0
            print("%d AR-CW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = True
    if rotB.rose:
        rotmove=True
        if not rotA.value:
            #cw
            encoder_counter += 1
            if encoder_counter == 24:
                encoder_counter = 0
            print("%d BR-CW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = True
        if rotA.value:
            #ccw
            encoder_counter -= 1
            if encoder_counter == -24:
                encoder_counter = 0
            print("%d BR-CCW" % encoder_counter, rotA.value, rotB.value)
            clockWISE = False

    if ((rotmove == True) and ((encoder_counter%2) == 0)):
        if clockWISE:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        if not clockWISE:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        rotmove = False

    # Button was 'just pressed'
    if switch.fell:
        print("Button pressed!")
        led.value = True
        #keyboard.press(Keycode.A)
        cc.send(ConsumerControlCode.MUTE)
    if switch.rose:
        print("Button Released!")
        led.value = False
        #keyboard.release(Keycode.A)  # ..."Release"!