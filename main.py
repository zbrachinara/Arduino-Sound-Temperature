import serial
import sys

port_name='undefined_os_behavior'
if sys.platform == 'linux':
    port_name = '/dev/ttyACM0'
elif sys.platform == 'win32':
    port_name = 'COM4'

arduino = serial.Serial(port=port_name, baudrate=9600, timeout=0.1)

def read():
    return arduino.readline()

while True:
    print(read())