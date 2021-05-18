import sys
import serial

from threading import Thread

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

class Buffer:

    def __init__(self, size):
        self.size = size
        self.contents = ([], [])

    def __str__(self):
        return f'x: {self.contents[0]}\ny: {self.contents[1]}'

    def __iter__(self):
        for i in self.contents:
            yield i

    def append(self, x, y):
        self.contents[0].append(x)
        self.contents[1].append(y)

        cutoff = x - self.size

        for i in self.contents[0]:
            if i > cutoff:
                break
            self.contents[0].pop(0)
            self.contents[1].pop(0)


class Data:

    def __init__(self):
        self.read_thread = Thread(target=self.update, daemon=True, name="read_thread")

        self.temperature_dat = ([], [])
        self.humidity_dat = ([], [])
        self.an_dat = []

        self.g_temperature_dat = Buffer(10)
        self.g_humidity_dat = Buffer(10)

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

                temp, hum, time = (float(i) for i in content.split(':'))
                self.temperature_dat[0].append(time)
                self.temperature_dat[1].append(temp)
                self.humidity_dat[0].append(time)
                self.humidity_dat[1].append(hum)

                self.g_temperature_dat.append(time, temp)
                self.g_humidity_dat.append(time, hum)

            elif prefix == r'\x01':  # Anemometer Read
                # print("An_cycle:", end='')
                self.an_dat.append(content)
