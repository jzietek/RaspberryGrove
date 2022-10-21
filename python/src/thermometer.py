import time
from grove_api.dht_sensor import DhtSensor
from value_changed_event import ValueChangedEvent

class Thermometer(object):
    def __init__(self):
        self.OnTemperatureChanged = ValueChangedEvent("°C")
        self.lastKnownTemperature = 0
    
    def AddSubscribersForTemperatureChangedEvent(self,objMethod):
        self.OnTemperatureChanged += objMethod
         
    def RemoveSubscribersForTemperatureChangedEvent(self,objMethod):
        self.OnTemperatureChanged -= objMethod

    def TemperatureChanged(self, newTemperature):
        previousTemperature = self.lastKnownTemperature
        self.lastKnownTemperature = newTemperature
        delta = newTemperature - previousTemperature
        self.OnTemperatureChanged(previousTemperature, newTemperature, delta, self.OnTemperatureChanged.measurementUnit)

    def RunLoop(self):
        sensor = DhtSensor()
        while (True):
            (temperature, humidity) = sensor.ReadTemperatureAndHumidity()

            if (temperature != self.lastKnownTemperature):
                self.TemperatureChanged(temperature)
            
            time.sleep(3)


class TemperatureChangePrinter(object):
    def __init__(self):
        pass

    def PrintTemperatureChange(self, previousTemperature, currentTemperature, delta, unit):
        print(f'Temperatue has changed from {previousTemperature} to {currentTemperature} {unit}')

def Run():
    temperatureObserver = TemperatureChangePrinter()
    #temperatureRestCaller = ToDo()
    thermometer = Thermometer()
    thermometer.AddSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)
    #thermometer.AddSubscribersForTemperatureChangedEvent(temperatureRestCaller.DoRestCall)

    try:
        thermometer.RunLoop()
    finally:
        thermometer.RemoveSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)

if __name__ == "__main__":
    Run()

