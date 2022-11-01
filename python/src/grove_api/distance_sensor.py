import random
import logging

class DistanceSensor(object):
    """
    This is an API for Grove Ultrasonic Ranger sensor:
    https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
    """
    def __init__(self, digital_port_number):
        self.__logger = logging.getLogger(__name__)
        try:
            from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
            self.__logger.info('Grove ultrasonic range sensor is installed')
            self.__sensor = GroveUltrasonicRanger(digital_port_number)
        except ImportError:
            self.__logger.warning("Grove not supported. Using mocked ultrasonic range sensor instead.")
            self.__sensor = None


    def read_distance(self):
        """ 
        Reads distance measurement in centimeters.
        Operational range is 2 - 350 cm.
        If no sensor is installed a random value will be provided.
        """
        if (self.__sensor is not None):
            return self.__sensor.get_distance()
        else:
            return random.random() * 100