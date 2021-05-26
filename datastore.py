import sys
import serial
from os import getenv, mkdir
from time import sleep

from threading import Thread

####################################################################
#                   SERIAL PORT INITIALIZATION                     #
####################################################################
# note: for port autodetect, no mac support
# sorry, apple users

arduino = None

port_name = getenv("ARDUINO_SERIAL_DEFAULT")
if port_name is None:
    port_name = "default_not_set"

for i in range(0, 21):
    try:
        arduino = serial.Serial(port=port_name, baudrate=9600, timeout=0.1)
        if arduino is not None:
            break
    except serial.serialutil.SerialException:
        pass

    if sys.platform == 'linux':
        port_name = f'/dev/ttyACM{i}'
    elif sys.platform == 'win32':
        port_name = f'COM{i}'

if arduino is None:
    sys.exit("SerialException: Problem getting port")

sleep(1)  # Hotfix to allow the arduino to reset its connection

####################################################################
#                        EXPOSED ELEMENTS                          #
####################################################################


def read():
    out = str(arduino.readline())
    out = out.split('\'')[1].split('\\r')[0]  # so basically:
    # arduino.readline() will return a string of form:
    #   b'[content]\r\n'
    # that line there exists to strip all of that off
    return out


def write_csv(data, filename):
    with open(filename, "a") as file:
        for dat in zip(*data):
            file.write(", ".join(str(i) for i in dat) + "\n")


class Buffer:

    def __init__(self, size):
        self.size = size
        self.contents = ([], [])

    def __str__(self):
        return f'x: {self.contents[0]}\ny: {self.contents[1]}'

    def __iter__(self):
        for i in self.contents:
            yield i

    def __getitem__(self, item):
        return self.contents[item]

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
        self.read_thread = Thread(
            target=self.update,
            daemon=True,
            name="read_thread"
        )

        self.latest_DHT = 0

        self.temp_dat = ([], []) # Temperature data [Time], [Temperature]
        self.hum_dat = ([], []) # Humidity data [Time], [Humidity]
        self.an_dat = []

        # These store the latest 20 seconds of data from the arduino
        self.g_temp_dat = Buffer(20)
        self.g_hum_dat = Buffer(20)

        self.read_thread.start()

    def write(self):

        # TODO: Signal read_thread to pause

        try:
            mkdir('data')
        except FileExistsError:
            pass

        write_csv(self.temp_dat, 'data/temperature.csv')
        self.temp_dat = ([], [])

        write_csv(self.hum_dat, 'data/humidity.csv')
        self.hum_dat = ([], [])

    def update(self):
        def dht_process():
            temp, hum, time = (float(i) for i in content.split(':'))
            self.temp_dat[0].append(time)
            self.temp_dat[1].append(temp)

            self.hum_dat[0].append(time)
            self.hum_dat[1].append(hum)


            self.g_temp_dat.append(time, temp)
            self.g_hum_dat.append(time, hum)

            self.latest_DHT = time

        def an_process():
            self.an_dat.append(content)
            print("pinged at:", content)

        # read_thread EVENT LOOP
        while True:
            line = read()

            if line == '':
                continue

            prefix = line[:4]
            content = line[4:]

            if prefix == r'\x00':  # DHT Read
                dht_process()

            elif prefix == r'\x01':  # Anemometer Read
                an_process()

