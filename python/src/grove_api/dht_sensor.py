import random

try:
    from grove.grove_temperature_humidity_sensor import DHT
    groveAvailable = True
except ImportError:
    print("Grove not supported. Using mocked temperature sensor instead.")
    groveAvailable = False

class DhtSensor(object):
    def __init__(self, digitalPortNumber = 5):
        self.digitalPortNumber = digitalPortNumber
        pass
    
    def ReadTemperatureAndHumidity(self):
        if groveAvailable:
            # Grove - Temperature&Humidity Sensor connected to port D5
            sensor = DHT('11', self.digitalPortNumber)
            humi, temp = sensor.read()
        else:
            temp = random.randint(10, 20)
            humi = random.randint(20, 80)
        return (temp, humi)

    def ReadTemperature(self):
        return self.ReadTemperatureAndHumidity()[0]

    def ReadHumidity(self):
        return self.ReadTemperatureAndHumidity()[1]