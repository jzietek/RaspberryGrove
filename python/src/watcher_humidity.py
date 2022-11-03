#!/usr/bin/env python3

import os
import logging_setup
from grove_api.aht20_sensor import TemperatureHumiditySensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import CyclicWatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier


def run(args):
    watcher_name = os.path.basename(__file__)
    sensor = TemperatureHumiditySensor()
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_humidity_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_humidity, handlers, args.interval, args.deltaTolerance, "%", watcher_name)    
    sensor_watcher.run_loop()


#python3 watcher_humidity.py http://raspberrypi:8080 --interval 3 --deltaTolerance 1 --idx 105
if __name__ == "__main__":
    logging_setup.initialize()
    parser = CyclicWatcherArgsParser("Humidity measurement watcher", idx=105)
    run(parser.parse_args())