import argparse
import requests
from grove_api.dht_sensor import DhtSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter

class TemperatureChangeDomoticzNotifier(object):
    def __init__(self, domoticzHost, idx):
        self.domoticzHost = domoticzHost
        self.idx = idx        

    def NotifyTemperatureChanged(self, previousTemperature, currentTemperature, delta, unit):
        requestQuery = f'{self.domoticzHost}/json.htm?type=command&param=udevice&idx={self.idx}&nvalue=0&svalue={currentTemperature}'
        print(requestQuery)
        response = requests.post(requestQuery)
        print(response.text)


def Run(args):
    sensor = DhtSensor(args.digitalPortUsed)
    sensorWatcher = CyclicSensorWatcher(sensor.ReadTemperature, args.interval, args.deltaTolerance, "°C")    
    domoticzNotifier = TemperatureChangeDomoticzNotifier(args.domoticzHost, args.idx)
    measurementChangePrinter = MeasurementChangePrinter()

    sensorWatcher.AddSubscribersForMeasurementChangedEvent(measurementChangePrinter.PrintMeasurementChange)
    sensorWatcher.AddSubscribersForMeasurementChangedEvent(domoticzNotifier.NotifyTemperatureChanged)

    try:
        sensorWatcher.RunLoop()
    finally:
        sensorWatcher.RemoveSubscribersForMeasurementChangedEvent(measurementChangePrinter.PrintMeasurementChange)
        sensorWatcher.RemoveSubscribersForMeasurementChangedEvent(domoticzNotifier.NotifyTemperatureChanged)

    

#python3 watcher_temperature.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 104
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temperature measurement handling.")
    parser.add_argument('domoticzHost', default="http://192.168.0.188:8080", help='Location of the Domoticz server. <IP/Hostname>:<PORT>')

    parser.add_argument('-i','--interval', type=int, default=30, help='Measurement interval time in seconds.')
    parser.add_argument('-t', '--deltaTolerance', default=0.5, type=float, help='Measurement change is reported, if previous measurement differs by more than this delta tolerance value.')
    parser.add_argument('-x', '--idx', type=int, default=104, help='Domoticz IDX number assigned to the related virtual device.')
    parser.add_argument('-d', '--digitalPortUsed', type=int, default=5, help='Number of digital port on the device, where the sensor is pluged-in.')

    args = parser.parse_args()    
    Run(args)