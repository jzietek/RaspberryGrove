import logging
import time
from value_changed_event import ValueChangedEvent

class CyclicSensorWatcher(object):
    def __init__(self, obj_method, interval, delta_tolerance, unit, watcher_name = None):
        self.__obj_method = obj_method
        self.__interval = interval
        self.__tolerance = delta_tolerance
        self.__unit = unit
        self.__last_known_value = 0
        self.on_sensor_event = ValueChangedEvent(self.__unit)
        if (watcher_name is not None):
            self.__logger = logging.getLogger(watcher_name)
        else:
            self.__logger = logging.getLogger()
        pass

    def add_sensor_event_subscriber(self,obj_method):
        self.on_sensor_event += obj_method
         
    def remove_sensor_event_subscriber(self,obj_method):
        self.on_sensor_event -= obj_method

    def measurement_changed(self, measured_value):
        previous_value = self.__last_known_value
        self.__last_known_value = measured_value
        delta = measured_value - previous_value
        self.on_sensor_event(previous_value, measured_value, delta, self.on_sensor_event.measurementUnit)

    def log_loop_started(self):
        self.__logger.info("Starting loop")
        self.__logger.info(f'Initial value: {self.__last_known_value} {self.__unit}')
        self.__logger.info(f'Change tolerance: {self.__tolerance}')
        self.__logger.info(f'Check interval: {self.__interval} seconds')

    def run_loop(self):
        self.log_loop_started()        
        while (True):
            measured_value = self.__obj_method()
            if (abs(measured_value - self.__last_known_value) > self.__tolerance):
                self.measurement_changed(measured_value)
            self.__logger.debug(f"Waiting for {self.__interval} s")
            time.sleep(self.__interval)
