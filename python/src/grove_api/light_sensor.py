import random

from grove_api.polling_sensor import PollingSensor
from grove_api.value_changed_event import ValueChangedEvent

class LightSensor(PollingSensor):
    """
    This is an API for the Grove Light Sensor v1.2:
    https://seeeddoc.github.io/Grove-Light_Sensor_v1.2/
    """
    def __init__(self, analog_port_number, interval, delta_tolerance):
        PollingSensor.__init__(self, __name__, interval, delta_tolerance)
        self.light_changed_event = ValueChangedEvent("Lux")
        try:
            from grove.grove_light_sensor_v1_2 import GroveLightSensor
            self._logger.info('Grove light sensor is installed')
            self._sensor = GroveLightSensor(analog_port_number)
        except ImportError:
            self._logger.warning("Grove not supported. Using mocked light sensor instead.")


    """
    Reads current luminosity in LUX units measured by the sensor.
    If no sensor is installed, random value will be returned from range 0 .. 100.
    """
    def read_light_intensity(self):
        if (self._sensor is not None):
            return self._sensor.light
        else:
            return random.random() * 100


    def run_loop(self):
        self._log_loop_started()
        while (True):
            light = self.read_light_intensity()
            if(self._change_significant(light, self._previous_value)):
                delta = light - self._previous_value
                self.light_changed_event(self._previous_value, light, delta, self.light_changed_event.measurementUnit)
                self._previous_value = light

            self._wait_polling_interval()