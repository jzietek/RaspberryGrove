import logging
import time
from value_changed_event import ValueChangedEvent

class CyclicSensorWatcher(object):
    def __init__(self, sensor_read_func, sensor_event_handlers, interval, delta_tolerance, unit, watcher_name = None):
        self.__sensor_read_func = sensor_read_func
        self.__interval = interval
        self.__tolerance = delta_tolerance
        self.__unit = unit
        self.__last_known_value = 0
        self.on_sensor_event = ValueChangedEvent(self.__unit)
        
        if (watcher_name is None):
            self.__logger = logging.getLogger()
        else:
            self.__logger = logging.getLogger(watcher_name)

        if (sensor_event_handlers is None):
            self.__sensor_event_handlers = []
        else:
            self.__sensor_event_handlers = sensor_event_handlers 


    def add_sensor_event_subscriber(self,sensor_event_handler):
        self.on_sensor_event += sensor_event_handler

         
    def remove_sensor_event_subscriber(self,sensor_event_handler):
        self.on_sensor_event -= sensor_event_handler


    def run_loop(self):
        self.__log_loop_started()
        for handler in self.__sensor_event_handlers:
            self.add_sensor_event_subscriber(handler)

        try:
            while (True):
                measured_value = self.__sensor_read_func()
                if (abs(measured_value - self.__last_known_value) > self.__tolerance):
                    self.__measurement_changed(measured_value)
                self.__logger.debug(f"Waiting for {self.__interval} s")
                time.sleep(self.__interval)
        finally:
            for handler in self.__sensor_event_handlers:
                self.remove_sensor_event_subscriber(handler)


    def __measurement_changed(self, measured_value):
        previous_value = self.__last_known_value
        self.__last_known_value = measured_value
        delta = measured_value - previous_value
        self.on_sensor_event(previous_value, measured_value, delta, self.on_sensor_event.measurementUnit)


    def __log_loop_started(self):
        self.__logger.info("Starting loop")
        self.__logger.info(f'Initial value: {self.__last_known_value} {self.__unit}')
        self.__logger.info(f'Change tolerance: {self.__tolerance}')
        self.__logger.info(f'Check interval: {self.__interval} seconds')