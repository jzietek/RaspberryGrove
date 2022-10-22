import time
import argparse
import requests
from grove_api.dht_sensor import DhtSensor
from value_changed_event import ValueChangedEvent

class Thermometer(object):
    def __init__(self, interval, tolerance):
        self.OnTemperatureChanged = ValueChangedEvent("°C")
        self.lastKnownTemperature = 0
        self.interval = interval
        self.tolerance = tolerance
    
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

            if (abs(temperature - self.lastKnownTemperature) > self.tolerance):
                self.TemperatureChanged(temperature)
            
            time.sleep(self.interval)

class TemperatureChangeDomoticzNotifier(object):
    def __init__(self, domoticzHost, idx):
        self.domoticzHost = domoticzHost
        self.idx = idx        

    def NotifyTemperatureChanged(self, previousTemperature, currentTemperature, delta, unit):
        requestQuery = f'{self.domoticzHost}/json.htm?type=command&param=udevice&idx={self.idx}&nvalue=0&svalue={currentTemperature}'
        print(requestQuery)
        response = requests.post(requestQuery)
        print(response.text)


class TemperatureChangePrinter(object):
    def __init__(self):
        pass

    def PrintTemperatureChange(self, previousTemperature, currentTemperature, delta, unit):
        print(f'Temperatue has changed from {previousTemperature} to {currentTemperature} {unit}')

def Run(args):
    temperatureObserver = TemperatureChangePrinter()
    domoticzNotifier = TemperatureChangeDomoticzNotifier(args.domoticzHost, args.idx)
    thermometer = Thermometer(args.interval, args.deltaTolerance)
    thermometer.AddSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)
    thermometer.AddSubscribersForTemperatureChangedEvent(domoticzNotifier.NotifyTemperatureChanged)

    try:
        thermometer.RunLoop()
    finally:
        thermometer.RemoveSubscribersForTemperatureChangedEvent(temperatureObserver.PrintTemperatureChange)
        thermometer.RemoveSubscribersForTemperatureChangedEvent(domoticzNotifier.NotifyTemperatureChanged)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temperature measurement handling.")
    parser.add_argument('domoticzHost', default="http://192.168.0.188:8080", help='Location of the Domoticz server. <IP/Hostname>:<PORT>')

    parser.add_argument('-i','--interval', type=int, default=30, help='Measurement interval time in seconds.')
    parser.add_argument('-t', '--deltaTolerance', default=0.5, type=float, help='Measurement change is reported, if previous measurement differs by more than this delta tolerance value.')
    parser.add_argument('-x', '--idx', type=int, help='Domoticz IDX number assigned to the related virtual device.')

    args = parser.parse_args()    
    Run(args)

#python3 thermometer.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 104

