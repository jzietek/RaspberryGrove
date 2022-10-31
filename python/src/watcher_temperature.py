#!/usr/bin/env python3

from domoticz_api_notifier import DomoticzApiNotifier
from grove_api.dht_sensor import DhtSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run(args):
    sensor = DhtSensor(args.digitalPortUsed)
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_temperature_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_temperature, handlers, args.interval, args.deltaTolerance, "°C")
    sensor_watcher.run_loop()

#python3 watcher_temperature.py http://192.168.0.188:8080 --interval 30 --deltaTolerance 0.5 --idx 104 -d 5
if __name__ == "__main__":
    parser = WatcherArgsParser("Temperature measurement watcher", idx=104, digital_port=5)   
    run(parser.parse_args())