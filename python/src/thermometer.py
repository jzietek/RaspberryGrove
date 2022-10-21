import time
from grove_api.dht_sensor import DhtSensor
from value_changed_event import ValueChangedEvent

class Thermometer(object):
    def __init__(self):
        self.OnTemperatureChanged = ValueChangedEvent("°C")
        self.OnHumidityChanged = ValueChangedEvent("%")
        self.lastKnwonTemperature = 0
        self.lastKnownHumidity = 0
    
    def AddSubscribersForTemperatureChangedEvent(self,objMethod):
        self.OnTemperatureChanged += objMethod
         
    def RemoveSubscribersForTemperatureChangedEvent(self,objMethod):
        self.OnTemperatureChanged -= objMethod

    def AddSubscribersForHumidityChangedEvent(self,objMethod):
        self.OnHumidityChanged += objMethod
         
    def RemoveSubscribersForHumidityChangedEvent(self,objMethod):
        self.OnHumidityChanged -= objMethod

    def TemperatureChanged(self, newTemperature):
        previousTemperature = self.lastKnwonTemperature
        self.lastKnwonTemperature = newTemperature
        delta = newTemperature - previousTemperature
        self.OnTemperatureChanged(previousTemperature, newTemperature, delta, self.OnTemperatureChanged.measurementUnit)

    def HumidityChanged(self, newHumidity):
        previousHumidity = self.lastKnownHumidity
        self.lastKnownHumidity = newHumidity
        delta = newHumidity - previousHumidity
        self.OnTemperatureChanged(previousHumidity, newHumidity, delta, self.OnHumidityChanged.measurementUnit)

    def RunLoop(self):
        sensor = DhtSensor()
        while (True):
            (temperature, humidity) = sensor.ReadTemperatureAndHumidity()

            if (temperature != self.lastKnwonTemperature):
                self.TemperatureChanged(temperature)
            
            if (humidity != self.lastKnwonTemperature):
                self.HumidityChanged(humidity)
            
            time.sleep(30)


class TemperatureChangePrinter(object):
    def __init__(self):
        pass

    def PrintTemperatureChange(self, previousTemperature, currentTemperature, delta, unit):
        print(f'Temperatue has changed from {previousTemperature} to {currentTemperature} {unit}')

    def PrintHumidityChange(self, previousHumidity, currentHumidity, delta, unit):
        print(f'Humidity has changed from {previousHumidity} to {currentHumidity} {unit}')


def Run():
    temperatureObserver = TemperatureChangePrinter()
    #temperatureRestCaller = ToDo()
    thermometer = Thermometer()
    thermometer.AddSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)
    thermometer.AddSubscribersForHumidityChangedEvent(temperatureObserver.PrintHumidityChange)
    #thermometer.AddSubscribersForTemperatureChangedEvent(temperatureRestCaller.DoRestCall)

    try:
        thermometer.RunLoop()
    finally:
        thermometer.RemoveSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)
        thermometer.RemoveSubscribersForHumidityChangedEvent(temperatureObserver.PrintHumidityChange)

if __name__ == "__main__":
    Run()

