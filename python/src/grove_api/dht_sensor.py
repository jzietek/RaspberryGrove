import random

try:
    from grove.grove_temperature_humidity_sensor import DHT
    grove_available = True
except ImportError:
    print("Grove not supported. Using mocked temperature/humidity sensor instead.")
    grove_available = False

class DhtSensor(object):
    def __init__(self, digital_port_number = 5):
        self.__digital_port_number = digital_port_number
        pass
    
    def read_temperature_and_humidity(self):
        if grove_available:
            # Grove - Temperature&Humidity Sensor connected to port D5
            sensor = DHT('11', self.__digital_port_number)
            humi, temp = sensor.read()
        else:
            temp = random.randint(10, 20)
            humi = random.randint(20, 80)
        return (temp, humi)

    def read_temperature(self):
        return self.read_temperature_and_humidity()[0]

    def read_humidity(self):
        return self.read_temperature_and_humidity()[1]