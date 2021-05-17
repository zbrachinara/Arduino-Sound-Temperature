
from datastore import Data
from time import sleep

data = Data()

if __name__ == '__main__':
    while True:
        print(*data.temperature_dat)
        print(*data.humidity_dat)
        print(data.an_dat)
        sleep(5)
        # data.print_buffer()

