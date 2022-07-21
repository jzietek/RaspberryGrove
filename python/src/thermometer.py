import time
from grove_api.dht_sensor import DhtSensor
from value_changed_event import ValueChangedEvent

class Thermometer(object):
    def __init__(self):
        self.OnTemperatureChanged = ValueChangedEvent("Celsius")
        self.lastKnwonTemperature = 0
    
    def AddSubscribersForTemperatureChangedEvent(self,objMethod):
        self.OnTemperatureChanged += objMethod
         
    def RemoveSubscribersForTemperatureChangedEvent(self,objMethod):
        self.OnTemperatureChanged -= objMethod

    def TemperatureChanged(self, newTemperature):
        previousTemperature = self.lastKnwonTemperature
        self.lastKnwonTemperature = newTemperature
        delta = newTemperature - previousTemperature
        self.OnTemperatureChanged(previousTemperature, newTemperature, delta)

    def RunLoop(self):
        sensor = DhtSensor()
        while (True):
            (temperature, humidity) = sensor.ReadTemperatureAndHumidity()
            if (temperature != self.lastKnwonTemperature):
                self.TemperatureChanged(temperature)
            time.sleep(1)


class TemperatureChangePrinter(object):
    def __init__(self):
        pass

    def PrintTemperatureChange(self, previousTemperature, currentTemperature, delta):
        print(f'Temperatue has changed from {previousTemperature} to {currentTemperature}')


def Run():
    temperatureObserver = TemperatureChangePrinter()
    thermometer = Thermometer()
    thermometer.AddSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)

    try:
        thermometer.RunLoop()
    finally:
        thermometer.RemoveSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)

if __name__ == "__main__":
    Run()

