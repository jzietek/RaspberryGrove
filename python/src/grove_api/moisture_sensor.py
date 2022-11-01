import random
import logging

class SoilMoistureSensor(object):
    """
    This is an API for the Soil Moisture Sensor v1.4:
    https://www.seeedstudio.com/Grove-Moisture-Sensor.html
    """
    def __init__(self, analog_port_number = 2):
        self.__logger = logging.getLogger(__name__)
        try:
            from grove.grove_moisture_sensor import GroveMoistureSensor
            self.__logger.info('Grove moisture sensor is installed')
            self.__sensor = GroveMoistureSensor(analog_port_number)
        except ImportError:
            self.__logger.warning("Grove not supported. Using mocked moisture sensor instead.")
            self.__sensor = None

    """
    Reads current moisture in % units measured by the sensor.
    If no sensor is installed, random value will be returned from range 0 .. 100.
    """
    def read_moisture(self):
        if (self.__sensor is not None):
            return self.__sensor.moisture
        else:
            return random.random() * 100