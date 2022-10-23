import argparse
import requests
from grove_api.light_sensor import LightSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter

class LightChangeDomoticzNotifier(object):
    def __init__(self, domoticzHost, idx):
        self.domoticzHost = domoticzHost
        self.idx = idx        

    def NotifyValueChanged(self, previousValue, currentValue, delta, unit):
        requestQuery = f'{self.domoticzHost}/json.htm?type=command&param=udevice&idx={self.idx}&nvalue=0&svalue={currentValue}'
        print(requestQuery)
        response = requests.post(requestQuery)
        print(response.text)


def Run(args):
    sensor = LightSensor(args.analogPortUsed)
    sensorWatcher = CyclicSensorWatcher(sensor.ReadLightIntensity, args.interval, args.deltaTolerance, "Lux")    
    domoticzNotifier = LightChangeDomoticzNotifier(args.domoticzHost, args.idx)
    measurementChangePrinter = MeasurementChangePrinter()

    sensorWatcher.AddSubscribersForMeasurementChangedEvent(measurementChangePrinter.PrintMeasurementChange)
    sensorWatcher.AddSubscribersForMeasurementChangedEvent(domoticzNotifier.NotifyValueChanged)

    try:
        sensorWatcher.RunLoop()
    finally:
        sensorWatcher.RemoveSubscribersForMeasurementChangedEvent(measurementChangePrinter.PrintMeasurementChange)
        sensorWatcher.RemoveSubscribersForMeasurementChangedEvent(domoticzNotifier.NotifyValueChanged)

    

#python3 watcher_light.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 106
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temperature measurement handling.")
    parser.add_argument('domoticzHost', default="http://192.168.0.188:8080", help='Location of the Domoticz server. <IP/Hostname>:<PORT>')

    parser.add_argument('-i','--interval', type=int, default=30, help='Measurement interval time in seconds.')
    parser.add_argument('-t', '--deltaTolerance', default=0.5, type=float, help='Measurement change is reported, if previous measurement differs by more than this delta tolerance value.')
    parser.add_argument('-x', '--idx', type=int, default=106, help='Domoticz IDX number assigned to the related virtual device.')
    parser.add_argument('-a', '--analogPortUsed', type=int, default=0, help='Number of analog port on the device, where the sensor is pluged-in.')

    args = parser.parse_args()    
    Run(args)