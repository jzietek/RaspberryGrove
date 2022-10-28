import logging
import time
from value_changed_event import ValueChangedEvent

class CyclicSensorWatcher(object):
    def __init__(self, obj_method, interval, delta_tolerance, unit):
        self.__obj_method = obj_method
        self.__interval = interval
        self.__tolerance = delta_tolerance
        self.__unit = unit
        self.__last_known_value = 0
        self.on_sensor_event = ValueChangedEvent(self.__unit)
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
        logging.info("Starting loop")
        logging.info(f'Initial value: {self.__last_known_value} {self.__unit}')
        logging.info(f'Change tolerance: {self.__tolerance}')
        logging.info(f'Check interval: {self.__interval} seconds')

    def run_loop(self):
        self.log_loop_started()        
        while (True):
            measured_value = self.__obj_method()
            if (abs(measured_value - self.__last_known_value) > self.__tolerance):
                self.measurement_changed(measured_value)
            
            time.sleep(self.__interval)
