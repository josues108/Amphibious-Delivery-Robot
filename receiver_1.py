"""
This code will be the first version of the final receiver section of the project.
PICO W MUST BE FLASHED WITH CIRCUITPYTHON (Adafruit V.10.0.3)
Upload this code to the Raspberry Pico W on board the ADR Bot.


This code has a simple task: Receive (X,Y) direction vector over radio, actuate motors and movement

Something important to note is that the MAX package size is 60 bytes!!!

"""

import board
import busio
import digitalio
import time
import pwmio

import adafruit_rfm69

#Start of RFM radio set up

#Radio freq definition
RADIO_FREQ_MHZ = 433.0

#Radio pin object definition
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP20)

#starting SPI bus
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
print(f"Frequency: {rfm69.frequency_mhz}mhz")

#End of RFM radio set up


#water sensor defining
water_sensor = digitalio.DigitalInOut(board.GP28)
water_sensor.direction = digitalio.Direction.INPUT
water_sensor.pull = digitalio.Pull.DOWN


#initializing Motor control PWM GPIO object

#Left motor
land_in1 = digitalio.DigitalInOut(board.GP0)  # IN1
land_in2 = digitalio.DigitalInOut(board.GP1)  # IN2
land_in1.direction = digitalio.Direction.OUTPUT
land_in2.direction = digitalio.Direction.OUTPUT

land_enable1 = pwmio.PWMOut(board.GP2, frequency=1000, duty_cycle=0)

#Right motor
land_in3 = digitalio.DigitalInOut(board.GP3)  # IN1
land_in4 = digitalio.DigitalInOut(board.GP4)  # IN2
land_in3.direction = digitalio.Direction.OUTPUT
land_in4.direction = digitalio.Direction.OUTPUT

land_enable2 = pwmio.PWMOut(board.GP5, frequency=1000, duty_cycle=0)


#Stating the same^^ but for propellors
#Left motor
water_in5 = digitalio.DigitalInOut(board.GP6)  # IN1 for boat
water_in6 = digitalio.DigitalInOut(board.GP7)  # IN2 for boat
water_in5.direction = digitalio.Direction.OUTPUT
water_in6.direction = digitalio.Direction.OUTPUT

water_enable3 = pwmio.PWMOut(board.GP8, frequency=1000, duty_cycle=0)

#Right motor
water_in7 = digitalio.DigitalInOut(board.GP10)  # IN1 for boat
water_in8 = digitalio.DigitalInOut(board.GP11)  # IN2 for boat
water_in7.direction = digitalio.Direction.OUTPUT
water_in8.direction = digitalio.Direction.OUTPUT

water_enable4 = pwmio.PWMOut(board.GP12, frequency=1000, duty_cycle=0)

#End of motor control PWM GPIO object definition



#Defining motor control functions

#By choosing a value between 0-65535 we set speed
def land_left_motor(speed):  
    land_in1.value = True
    land_in2.value = False
    land_enable1.duty_cycle = speed

def land_right_motor(speed):
    land_in3.value = True
    land_in4.value = False
    land_enable2.duty_cycle = speed
    
def land_off():
    land_enable1.duty_cycle = 0
    land_enable2.duty_cycle = 0
    land_in1.value = False
    land_in2.value = False
    land_in3.value = False
    land_in4.value = False
    
def water_left(speed):
    water_in5.value = True
    water_in6.value = False
    water_enable3.duty_cycle = speed

def water_right(speed):
    water_in7.value = True
    water_in8.value = False
    water_enable4.duty_cycle = speed

def water_off():
    water_enable3.duty_cycle = 0
    water_enable4.duty_cycle = 0
    water_in5.value = False
    water_in6.value = False
    water_in7.value = False
    water_in8.value = False
    
#End of defining motor control functions


current_left_motor = land_left_motor
current_right_motor = land_right_motor


def decode_signed(byte_val):
    """Convert 0–255 to signed int8 (-128..127)"""
    if byte_val > 127:
        return byte_val - 256
    return byte_val

#Library of different states the motor controllers are in depending on joystick input
command_table = {
    (0,0): lambda: (current_left_motor(0), current_right_motor(0)),
    (0,1): lambda: (current_left_motor(33000), current_right_motor(33000)),
    (0,2): lambda: (current_left_motor(65535), current_right_motor(65535)),
    
    (1,0): lambda: (current_left_motor(33000), current_right_motor(0)),
    (1,1): lambda: (current_left_motor(50000), current_right_motor(33000)),
    (1,2): lambda: (current_left_motor(65535), current_right_motor(50000)),
    
    (2,0): lambda: (current_left_motor(65535), current_right_motor(0)),
    (2,1): lambda: (current_left_motor(65535), current_right_motor(33000)),
    (2,2): lambda: (current_left_motor(65535), current_right_motor(50000)),
    
    (-1,0): lambda: (current_left_motor(0), current_right_motor(33000)),
    (-1,1): lambda: (current_left_motor(33000), current_right_motor(50000)),
    (-1,2): lambda: (current_left_motor(33000), current_right_motor(65535)),
    
    (-2,0): lambda: (current_left_motor(0), current_right_motor(65535)),
    (-2,1): lambda: (current_left_motor(33000), current_right_motor(65535)),
    (-2,2): lambda: (current_left_motor(50000), current_right_motor(65535)),
}

DIRECTION = (0,0)

while True:
    #This section focuses on decoding package and spitting out easy (X,Y) form
    packet = rfm69.receive()
    

    if packet is not None and len(packet) == 2:
        x = decode_signed(packet[0])
        y = decode_signed(packet[1])
        DIRECTION = (x, y)
        print("Direction:", DIRECTION)

    elif packet is not None:
        print("Unexpected packet length:", len(packet))

    if water_sensor.value:
        # WATER MODE
        print("WATER MODE")
        land_off()
        current_left_motor = water_left
        current_right_motor = water_right
    else:
        # LAND MODE
        print("LAND MODE")
        water_off()
        current_left_motor = land_left_motor
        current_right_motor = land_right_motor
        
    command = command_table.get(DIRECTION) #(0,1) (2,0)
    command()   # execute it
            
    #print("done")
    time.sleep(0.1)

