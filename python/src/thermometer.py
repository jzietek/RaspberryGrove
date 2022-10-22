import time
import argparse
import requests
from grove_api.dht_sensor import DhtSensor
from value_changed_event import ValueChangedEvent

class TemperatureChangeDomoticzNotifier(object):
    def __init__(self, domoticzHost, idx):
        self.domoticzHost = domoticzHost
        self.idx = idx        

    def NotifyTemperatureChanged(self, previousTemperature, currentTemperature, delta, unit):
        requestQuery = f'{self.domoticzHost}/json.htm?type=command&param=udevice&idx={self.idx}&nvalue=0&svalue={currentTemperature}'
        print(requestQuery)
        response = requests.post(requestQuery)
        print(response.text)


class CyclicSensorWatcher(object):
    def __init__(self, sensor, interval, deltaTolerance, unit):
        self.sensor = sensor
        self.interval = interval
        self.tolerance = deltaTolerance
        self.unit = unit
        self.lastKnownValue = 0
        self.OnMeasurementChanged = ValueChangedEvent(self.unit)
        pass

    def AddSubscribersForMeasurementChangedEvent(self,objMethod):
        self.OnMeasurementChanged += objMethod
         
    def RemoveSubscribersForMeasurementChangedEvent(self,objMethod):
        self.OnMeasurementChanged -= objMethod

    def MeasurementChanged(self, measuredValue):
        previousValue = self.lastKnownValue
        self.lastKnownValue = measuredValue
        delta = measuredValue - previousValue
        self.OnMeasurementChanged(previousValue, measuredValue, delta, self.OnMeasurementChanged.measurementUnit)

    def RunLoop(self):
        sensor = DhtSensor(5)
        while (True):
            (temperature, humidity) = sensor.ReadTemperatureAndHumidity()
            measuredValue = temperature

            if (abs(measuredValue - self.lastKnownValue) > self.tolerance):
                self.MeasurementChanged(measuredValue)
            
            time.sleep(self.interval)


class MeasurementChangePrinter(object):
    def __init__(self):
        pass

    def PrintMeasurementChange(self, previousValue, currentValue, delta, unit):
        print(f'Value has changed from {previousValue} to {currentValue} {unit}')


def Run(args):
    sensor = DhtSensor(5)
    #sensorWatcher = CyclicSensorWatcher(sensor.ReadTemperature, args.interval, args.deltaTolerance, "°C")
    sensorWatcher = CyclicSensorWatcher(DhtSensor(5), args.interval, args.deltaTolerance, "°C")
    domoticzNotifier = TemperatureChangeDomoticzNotifier(args.domoticzHost, args.idx)
    measurementChangePrinter = MeasurementChangePrinter()

    sensorWatcher.AddSubscribersForMeasurementChangedEvent(measurementChangePrinter.PrintMeasurementChange)
    sensorWatcher.AddSubscribersForMeasurementChangedEvent(domoticzNotifier.NotifyTemperatureChanged)

    try:
        sensorWatcher.RunLoop()
    finally:
        sensorWatcher.RemoveSubscribersForMeasurementChangedEvent(measurementChangePrinter.PrintMeasurementChange)
        sensorWatcher.RemoveSubscribersForMeasurementChangedEvent(domoticzNotifier.NotifyTemperatureChanged)

    

#python3 thermometer.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 104
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temperature measurement handling.")
    parser.add_argument('domoticzHost', default="http://192.168.0.188:8080", help='Location of the Domoticz server. <IP/Hostname>:<PORT>')

    parser.add_argument('-i','--interval', type=int, default=30, help='Measurement interval time in seconds.')
    parser.add_argument('-t', '--deltaTolerance', default=0.5, type=float, help='Measurement change is reported, if previous measurement differs by more than this delta tolerance value.')
    parser.add_argument('-x', '--idx', type=int, help='Domoticz IDX number assigned to the related virtual device.')

    args = parser.parse_args()    
    Run(args)