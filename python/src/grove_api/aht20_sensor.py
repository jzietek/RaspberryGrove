import random
import logging
import time

class TemperatureHumiditySensor(object):
    """
    This is an API for the Grove AHT20 temperature and humidity sensor:
    https://wiki.seeedstudio.com/Grove-AHT20-I2C-Industrial-Grade-Temperature&Humidity-Sensor/
    https://www.seeedstudio.com/Grove-AHT20-I2C-Industrial-grade-temperature-and-humidity-sensor-p-4497.html
    """

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        try:
            from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
            self.__sensor = GroveTemperatureHumidityAHT20()
        except ImportError:
            self.__logger.warn("Grove not supported. Using mocked temperature/humidity sensor instead.")
            self.__sensor = None


    def read_temperature_and_humidity(self):
        if (self.__sensor is not None):
            temp, humi = self.__sensor.read()
        else:
            temp = random.randint(10, 20)
            humi = random.randint(20, 80)
        return (temp, humi)

    def read_temperature(self):
        return self.read_temperature_and_humidity()[0]

    def read_humidity(self):
        return self.read_temperature_and_humidity()[1]


def test():
    sensor = TemperatureHumiditySensor()
    while(True):
        temperature, humidity  = sensor.read_temperature_and_humidity()
        print('Temperature in Celsius is {:.2f} C'.format(temperature))
        print('Relative Humidity is {:.2f} %'.format(humidity))
        time.sleep(1)


if __name__ == "__main__":
    test()