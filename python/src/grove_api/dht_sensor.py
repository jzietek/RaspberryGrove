import random

try:
    from grove.grove_temperature_humidity_sensor import DHT
    groveAvailable = True
except ImportError:
    print("Grove not supported. Using mocks instead.")
    groveAvailable = False

class DhtSensor(object):
    def __init__(self):
        pass
    
    def ReadTemperatureAndHumidity(self):
        if groveAvailable:
            # Grove - Temperature&Humidity Sensor connected to port D5
            sensor = DHT('11', 5)
            humi, temp = sensor.read()
        else:
            temp = random.randint(1, 2)
            humi = 50
        return (temp, humi)