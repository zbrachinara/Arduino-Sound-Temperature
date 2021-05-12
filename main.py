import serial
import sys

port_name = 'undefined_os_behavior'
if sys.platform == 'linux':
    port_name = '/dev/ttyACM0'
elif sys.platform == 'win32':
    port_name = 'COM4'

arduino = serial.Serial(port=port_name, baudrate=9600, timeout=0.1)


def read():
    out = str(arduino.readline())
    if sys.platform == 'linux':
        out = out.split('\'')[1].split('\\r')[0]  # so basically:
    # arduino.readline() will return a string of form:
    #   b'[content]\r\n'
    # at least, on linux.
    # that line there exists to strip all of that off
    return out


while True:
    line = read()
    prefix = line[:4]
    content = line[4:]

    if prefix == '\\x00':
        print("Temperature: ", end='')
    elif prefix == '\\x01':
        print("Humidity: ", end='')
    elif prefix == '\\x02':
        print("Time: ", end='')

    if len(content) > 0:
        print(content)
