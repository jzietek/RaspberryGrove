import random

from grove_api.polling_sensor import PollingSensor
from grove_api.value_changed_event import ValueChangedEvent

class DistanceSensor(PollingSensor):
    """
    This is an API for Grove Ultrasonic Ranger sensor:
    https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
    """
    def __init__(self, digital_port_number, interval, delta_tolerance):
        PollingSensor.__init__(self, __name__, interval, delta_tolerance)
        self.distance_changed_event = ValueChangedEvent("m")
        try:
            from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
            self._logger.info('Grove ultrasonic range sensor is installed')
            self._sensor = GroveUltrasonicRanger(digital_port_number)
        except ImportError:
            self._logger.warning("Grove not supported. Using mocked ultrasonic range sensor instead.")


    def read_distance(self):
        """ 
        Reads distance measurement in centimeters.
        Operational range is 2 - 350 cm.
        If no sensor is installed a random value will be provided.
        """
        if (self._sensor is not None):
            return self._sensor.get_distance()
        else:
            return random.random() * 100

    
    def run_loop(self):
        self._log_loop_started()
        while (True):
            distance = self.read_distance()
            if(self._change_significant(distance, self._previous_value)):
                delta = distance - self._previous_value
                self.distance_changed_event(self._previous_light, distance, delta, self.distance_changed_event.measurementUnit)
                self._previous_value = distance

            self._wait_polling_interval()