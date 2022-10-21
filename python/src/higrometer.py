import time
from grove_api.dht_sensor import DhtSensor
from value_changed_event import ValueChangedEvent

class Higrometer(object):
    def __init__(self):
        self.OnHumidityChanged = ValueChangedEvent("%")
        self.lastKnownHumidity = 0

    def AddSubscribersForHumidityChangedEvent(self,objMethod):
        self.OnHumidityChanged += objMethod
         
    def RemoveSubscribersForHumidityChangedEvent(self,objMethod):
        self.OnHumidityChanged -= objMethod

    def HumidityChanged(self, newHumidity):
        previousHumidity = self.lastKnownHumidity
        self.lastKnownHumidity = newHumidity
        delta = newHumidity - previousHumidity
        self.OnHumidityChanged(previousHumidity, newHumidity, delta, self.OnHumidityChanged.measurementUnit)

    def RunLoop(self):
        sensor = DhtSensor()
        while (True):
            (temperature, humidity) = sensor.ReadTemperatureAndHumidity()
            
            if (humidity != self.lastKnownHumidity):
                self.HumidityChanged(humidity)
            
            time.sleep(3)


class HumidityChangePrinter(object):
    def __init__(self):
        pass

    def PrintHumidityChange(self, previousHumidity, currentHumidity, delta, unit):
        print(f'Humidity has changed from {previousHumidity} to {currentHumidity} {unit}')


def Run():
    temperatureObserver = HumidityChangePrinter()
    higrometer = Higrometer()
    higrometer.AddSubscribersForHumidityChangedEvent(temperatureObserver.PrintHumidityChange)

    try:
        higrometer.RunLoop()
    finally:
        higrometer.RemoveSubscribersForHumidityChangedEvent(temperatureObserver.PrintHumidityChange)

if __name__ == "__main__":
    Run()

