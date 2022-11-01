import logging
from datetime import datetime, timedelta

class MotionSensor(object):
    """
    This is an API for the Grove Motion sensor:
    https://www.seeedstudio.com/Grove-mini-PIR-motion-sensor-p-2930.html
    """

    def __init__(self, digital_port_number):
        self.__logger = logging.getLogger(__name__)
        self.__last_detection_time = datetime.fromordinal(1)
        try:
            from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
            self.__logger.info('Grove motion sensor is installed')
            self.__sensor = GroveMiniPIRMotionSensor(digital_port_number)
            self.__sensor.on_detect = self.__on_detected
        except ImportError:
            self.__logger.warning("Grove not supported. Using mocked motion sensor instead.")
            self.__sensor = None
            self.__iteration_counter = 0


    def __on_detected(self):
        self.__last_detection_time = datetime.now()
        self.__logger.debug('Motion detected')


    def is_motion_detected(self):
        now = datetime.now()
        if (self.__sensor is None):
            self.__iteration_counter = self.__iteration_counter + 1
            if (self.__iteration_counter > 3):
                self.__last_detection_time = datetime.now()
                self.__iteration_counter = 0

        detection_time_with_margin = self.__last_detection_time + timedelta(seconds=5)
        if (detection_time_with_margin > now):
            return 1
        else:
            return 0    