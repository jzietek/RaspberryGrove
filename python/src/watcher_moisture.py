#!/usr/bin/env python3

import os
import logging_setup
from grove_api.moisture_sensor import SoilMoistureSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import CyclicWatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run(args):
    watcher_name = os.path.basename(__file__)
    sensor = SoilMoistureSensor(args.analogPortUsed)
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_moisture_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_moisture, handlers, args.interval, args.deltaTolerance, "%", watcher_name)    
    sensor_watcher.run_loop()

#python3 watcher_moisture.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 109 -a 2
if __name__ == "__main__":
    logging_setup.initialize()
    parser = CyclicWatcherArgsParser("Moisture measurement watcher", idx=109, analog_port=2) 
    run(parser.parse_args())