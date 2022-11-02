#!/usr/bin/env python3

import os
from domoticz_api_notifier import DomoticzApiNotifier
from grove_api.aht20_sensor import TemperatureHumiditySensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run(args):
    watcher_name = os.path.basename(__file__)
    sensor = TemperatureHumiditySensor()
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_temperature_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_temperature, handlers, args.interval, args.deltaTolerance, "°C", watcher_name)
    sensor_watcher.run_loop()


#python3 watcher_temperature.py http://raspberrypi:8080 --interval 30 --deltaTolerance 0.5 --idx 104 -d 5
if __name__ == "__main__":
    parser = WatcherArgsParser("Temperature measurement watcher", idx=104)   
    run(parser.parse_args())