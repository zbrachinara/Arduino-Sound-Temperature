import sys
import serial

from threading import Thread
from queue import Queue

for i in range(0, 20):
    port_name = 'undefined_os_behavior'
    try:
        if sys.platform == 'linux':
            port_name = f'/dev/ttyACM{i}'
        elif sys.platform == 'win32':
            port_name = f'COM{i}'

        arduino = serial.Serial(port=port_name, baudrate=9600, timeout=0.1)
        break
    except serial.serialutil.SerialException:
        continue

if arduino is None:
    sys.exit("SerialException: Problem getting port")

def read():
    out = str(arduino.readline())
    if sys.platform == 'linux':
        out = out.split('\'')[1].split('\\r')[0]  # so basically:
    # arduino.readline() will return a string of form:
    #   b'[content]\r\n'
    # at least, on linux.
    # that line there exists to strip all of that off
    return out


class Data:

    def __init__(self):
        self.read_thread = Thread(target=self.update, daemon=True, name="read_thread")
        self.comm = Queue()

        self.temperature_dat = ([], [])
        self.humidity_dat = ([], [])
        self.an_dat = []

        self.read_thread.start()

    def update(self):
        while True:
            line = read()

            if line == '':
                continue

            prefix = line[:4]
            content = line[4:]

            if prefix == r'\x00':  # DHT Read
                # print("DHT:", end='')

                temp, hum, time = content.split(':')
                self.temperature_dat[0].append(time)
                self.temperature_dat[1].append(temp)
                self.humidity_dat[0].append(time)
                self.humidity_dat[1].append(hum)

            elif prefix == r'\x01':  # Anemometer Read
                # print("An_cycle:", end='')
                self.an_dat.append(content)

            self.comm.put(line)


    def print_buffer(self):
        if not self.comm.empty():
            line = self.comm.get()
            prefix = line[:4]
            content = line[4:]

            print(content)