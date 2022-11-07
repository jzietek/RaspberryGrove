import random
from grove_api.polling_sensor import PollingSensor
from grove_api.value_changed_event import ValueChangedEvent

class SoilMoistureSensor(PollingSensor):
    """
    This is an API for the Soil Moisture Sensor v1.4:
    https://www.seeedstudio.com/Grove-Moisture-Sensor.html
    """
    def __init__(self, analog_port_number, interval, delta_tolerance):
        PollingSensor.__init__(self, __name__, interval, delta_tolerance)
        self.moisture_changed_event = ValueChangedEvent("%")
        try:
            from grove.grove_moisture_sensor import GroveMoistureSensor
            self._logger.info('Grove moisture sensor is installed')
            self._sensor = GroveMoistureSensor(analog_port_number)
        except ImportError:
            self._logger.warning("Grove not supported. Using mocked moisture sensor instead.")


    """
    Reads current moisture in % units measured by the sensor.
    If no sensor is installed, random value will be returned from range 0 .. 100.
    """
    def read_moisture(self):
        if (self._sensor is not None):
            return self._sensor.moisture
        else:
            return random.random() * 100


    def run_loop(self):
        self._log_loop_started()
        while (True):
            moisture = self.read_moisture()
            if(self._change_significant(moisture, self._previous_value)):
                delta = moisture - self._previous_value
                self.moisture_changed_event(self._previous_value, moisture, delta, self.moisture_changed_event.measurementUnit)
                self._previous_value = moisture

            self._wait_polling_interval()