"""
This code will be the first version of the final transmitter section of the project.
Upload this code to the Adafruit RP20240 feather. This will be the transmitter piece.

This code has a simple task: Read joystick commands, linearize it and send it over the radio

Something important to note is that the MAX package size is 60 bytes!!!

"""

import board
import busio
import digitalio
import time
import analogio


import adafruit_rfm69

#Start of RFM radio set up

#Radio freq definition
RADIO_FREQ_MHZ = 433.0

#Radio pin object definition
CS = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)

#starting SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initializing RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)
print(f"Frequency: {rfm69.frequency_mhz}mhz")

#End of RFM radio set up

# Defining analog objects for joystick
x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)

def read_axis(pin):
    # Convert 16-bit ADC value into a simple 0–65535
    return pin.value

def linearize(value):
    """
    Convert raw ADC (0–65535) into a signed range -2 to 2.
    Middle (~32768) becomes 0.
    """
    # convert to float range 0.0 → 1.0
    norm = value / 65535  
    
    # scale to -1.0 → +1.0
    scaled = (norm * 2.0) - 1.0
    
    # finally scale to -5 → +5
    output = scaled * 2
    
    return int(round(output))

#This is just to VISUALLY see whats being sent, can be deleted when uploaded to feather
def decode_packet(packet):
    # Unsigned values (0–255)
    unsigned = list(packet)
    # Convert to signed int8
    signed = [(b - 256) if b > 127 else b for b in unsigned]
    #print("X:", signed[0], "Y:", signed[1])

while True:
    x = read_axis(x_axis) #should be in range of 0-65535
    y = read_axis(y_axis)
    
    
    x_val = linearize(x)
    y_val = linearize(y)
    if y_val < 0:
        y_val = 0
        
    packet = bytes([x_val & 0xFF, y_val & 0xFF]) #converting integer to bytes, & 0xFF converts it into an unsigned byte
    rfm69.send(packet)
    
    decode_packet(packet)
    time.sleep(0.05)