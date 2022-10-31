import random
import logging

class LightSensor(object):
    """
    This is an API for the Grove Light Sensor v1.2:
    https://seeeddoc.github.io/Grove-Light_Sensor_v1.2/
    """
    def __init__(self, analog_port_number = 0):
        self.__logger = logging.getLogger(__name__)
        try:
            from grove.grove_light_sensor_v1_2 import GroveLightSensor
            self.__logger.info('Grove light sensor is installed')
            self.__sensor = GroveLightSensor(analog_port_number)
        except ImportError:
            self.__logger.warning("Grove not supported. Using mocked light sensor instead.")
            self.__sensor = None

    """
    Reads current luminosity in LUX units measured by the sensor.
    If no sensor is installed, random value will be returned from range 0 .. 100.
    """
    def read_light_intensity(self):
        if (self.__sensor is not None):
            return self.__sensor.light
        else:
            return random.random() * 100