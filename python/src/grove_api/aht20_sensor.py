import smbus2

# Monkey patch for grove.py compatibility: 
# Maps missing .write() and .read() methods to native smbus2 I2C block operations.

if not hasattr(smbus2.SMBus, 'write'):
    def _fixed_write(self, address, data):
        if isinstance(data, int):
            return self.write_byte(address, data)
        elif len(data) == 1:
            return self.write_byte(address, data)
        else:
            return self.write_i2c_block_data(address, data[0], data[1:])
    
    smbus2.SMBus.write = _fixed_write

if not hasattr(smbus2.SMBus, 'read'):
    def _fixed_read(self, address, length):
        # AHT20 requires reading a block of bytes after sending a measurement request
        # Typically, we read the block from a "dummy" register 0 or directly from the address
        return self.read_i2c_block_data(address, 0, length)
    
    smbus2.SMBus.read = _fixed_read
# End of monkey patch


import random
from grove_api.polling_sensor import PollingSensor
from grove_api.value_changed_event import ValueChangedEvent

class TemperatureHumiditySensor(PollingSensor):
    """
    This is an API for the Grove AHT20 temperature and humidity sensor:
    https://wiki.seeedstudio.com/Grove-AHT20-I2C-Industrial-Grade-Temperature&Humidity-Sensor/
    https://www.seeedstudio.com/Grove-AHT20-I2C-Industrial-grade-temperature-and-humidity-sensor-p-4497.html
    """

    def __init__(self, interval, delta_tolerance):
        PollingSensor.__init__(self, __name__, interval, delta_tolerance)
        self.temperature_changed_event = ValueChangedEvent("°C")
        self.humidity_changed_event = ValueChangedEvent("%")
        self.__previous_temperature = 0
        self.__previous_humidity = 0
        try:
            from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
            self._sensor = GroveTemperatureHumidityAHT20()
        except ImportError as e:
            self._logger.warn(f"Grove not supported. Using mocked temperature/humidity sensor instead. Error: {e}")


    def read_temperature_and_humidity(self):
        if (self._sensor is not None):
            temp, humi = self._sensor.read()
        else:
            temp = random.randint(10, 20)
            humi = random.randint(20, 80)
        return (temp, humi)


    def run_loop(self):
        self._log_loop_started()
        while (True):
            temperature, humidity = self.read_temperature_and_humidity()
            if(self._change_significant(temperature, self.__previous_temperature)):
                delta = temperature - self.__previous_temperature
                self.temperature_changed_event(self.__previous_temperature, temperature, delta, self.temperature_changed_event.measurementUnit)
                self.__previous_temperature = temperature

            if(self._change_significant(humidity, self.__previous_humidity)):
                delta = humidity - self.__previous_humidity
                self.humidity_changed_event(self.__previous_humidity, humidity, delta, self.humidity_changed_event.measurementUnit)
                self.__previous_humidity = humidity

            self._wait_polling_interval()


def simple_test():
    sensor = TemperatureHumiditySensor(1, 0.5)
    while(True):
        temperature, humidity  = sensor.read_temperature_and_humidity()
        print('Temperature in Celsius is {:.2f} C'.format(temperature))
        print('Relative Humidity is {:.2f} %'.format(humidity))
        sensor._wait_polling_interval()


if __name__ == "__main__":
    simple_test()
