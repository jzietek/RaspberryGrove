import logging
from datetime import date, datetime, timedelta

class MotionSensor(object):
    def __init__(self, digital_port_number):
        self.__logger = logging.getLogger(__name__)
        self.__init_sensor()        
        self.__last_detection_time = datetime.fromordinal(1)

        if (self.__grove_available):
            self.__sensor = GroveMiniPIRMotionSensor(digital_port_number)
            self.__sensor.on_detect = self.__on_detected
        else:
            self.__sensor = None
            self.__iteration_counter = 0

    def __init_sensor(self):
        try:            
            from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
            self.__logger.info('Grove motion sensor is installed')
            (self.__grove_available) = True
        except ImportError:
            self.__logger.warning("Grove not supported. Using mocked motion sensor instead.")
            (self.__grove_available) = False

    def __on_detected(self):        
        self.__last_detection_time = datetime.now()

    def is_motion_detected(self):
        now = datetime.now()
        if (self.__sensor is None):
            self.__iteration_counter = self.__iteration_counter + 1
            if (self.__iteration_counter > 3):
                self.__last_detection_time = datetime.now()
                self.__iteration_counter = 0

        detection_time_with_margin = self.__last_detection_time + timedelta(seconds=1)
        if (detection_time_with_margin > now):
            return 1

        return 0    