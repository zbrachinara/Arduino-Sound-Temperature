import serial

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=0.1)

def read():
    return arduino.readline()

while True:
    print(read())