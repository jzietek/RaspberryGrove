#!/usr/bin/env python3

import os
import logging_setup
from grove_api.light_sensor import LightSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run(args):
    watcher_name = os.path.basename(__file__)
    sensor = LightSensor(args.analogPortUsed)
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_light_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_light_intensity, handlers, args.interval, args.deltaTolerance, "Lux", watcher_name)    
    sensor_watcher.run_loop()

#python3 watcher_light.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 106
if __name__ == "__main__":
    logging_setup.initialize()
    parser = WatcherArgsParser("Light measurement watcher", idx=106, analog_port=0) 
    run(parser.parse_args())