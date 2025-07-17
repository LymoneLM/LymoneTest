import wiringpi
import time
import sys

class HTU21DReader:
    def __init__(self, base=64, full_dict=None):
        self.BASE = base
        self.A0 = self.BASE + 0  # Temperature channel
        self.A1 = self.BASE + 1  # Humidity channel

        self.full_dict = full_dict

        # Initialize the HTU21D sensor
        wiringpi.wiringPiSetup()
        wiringpi.htu21dSetup(self.BASE)

    def read_temperature(self):
        # Read the temperature value
        value_temp = wiringpi.analogRead(self.A0)
        return value_temp / 10  # Convert to Celsius

    def read_humidity(self):
        # Read the humidity value
        value_humi = wiringpi.analogRead(self.A1)
        return value_humi / 10  # Convert to percentage

    def run(self):
        # Run an infinite loop to read and display temperature and humidity
        try:
            while True:
                temp = self.read_temperature()
                humi = self.read_humidity()
                print(f"Temp value: {temp} C")
                print(f"Humi value: {humi} %")
                time.sleep(2)
        except KeyboardInterrupt:
            print('\nExit')
            sys.exit(0)

# If the script is executed, create an instance of HTU21DReader and run it
if __name__ == "__main__":
    sensor = HTU21DReader()
    sensor.run()
