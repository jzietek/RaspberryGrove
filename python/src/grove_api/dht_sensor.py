import random
import logging

class DhtSensor(object):
    def __init__(self, digital_port_number = 5):
        self.__logger = logging.getLogger(__name__)
        try:
            from grove.grove_temperature_humidity_sensor import DHT
            self.__sensor = DHT('11', digital_port_number)
        except ImportError:
            self.__logger.warn("Grove not supported. Using mocked temperature/humidity sensor instead.")
            self.__sensor = None


    def __read_temperature_and_humidity(self):
        if (self.__sensor is not None):
            humi, temp = self.__sensor.read()
        else:
            temp = random.randint(10, 20)
            humi = random.randint(20, 80)
        return (temp, humi)

    def read_temperature(self):
        return self.__read_temperature_and_humidity()[0]

    def read_humidity(self):
        return self.__read_temperature_and_humidity()[1]