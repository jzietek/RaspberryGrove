import random
import logging

class LightSensor(object):
    def __init__(self, analog_port_number = 0):
        self.__logger = logging.getLogger(__name__)
        self.__init_sensor()
        if (self.__grove_available):
            self.__sensor = GroveLightSensor(analog_port_number)
        else:
            self.__sensor = None

    def __init_sensor(self):
        try:
            from grove.grove_light_sensor_v1_2 import GroveLightSensor
            self.__logger.info('Grove light sensor is installed')
            (self.__grove_available) = True
        except ImportError:
            self.__logger.warning("Grove not supported. Using mocked light sensor instead.")
            (self.__grove_available) = False

    def read_light_intensity(self):
        if (self.__sensor is not None):
            return self.__sensor.light
        else:
            return random.random() * 100