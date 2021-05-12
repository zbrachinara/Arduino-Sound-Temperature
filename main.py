
from datastore import read

if __name__ == '__main__':
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
