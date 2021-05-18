
from datastore import Data
from time import sleep

data = Data()

if __name__ == '__main__':
    while True:
        print(*data.g_temperature_dat)
        print(*data.g_humidity_dat)
        # print(data.an_dat)
        sleep(5)


