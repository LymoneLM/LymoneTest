import wiringpi
import time
import sys

wiringpi.wiringPiSetup()
BASE = 64
A0 = BASE + 0
A1 = BASE + 1
wiringpi.htu21dSetup(BASE)

def get_temp():
    return wiringpi.analogRead(A0)

def get_hum():
    return wiringpi.analogRead(A1)

def main():
    while True:
        try:
            value = wiringpi.analogRead(A0)
            print("Temp value: {}".format(value / 10))
            value = wiringpi.analogRead(A1)
            print("Hum value: {}".format(value / 10))
            time.sleep(2)
        except KeyboardInterrupt:
            print('\nExit')
            sys.exit(0)

if __name__ == '__main__':
    main()