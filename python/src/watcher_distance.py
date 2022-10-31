#!/usr/bin/env python3

import os
import logging_setup
from grove_api.distance_sensor import DistanceSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run(args):
    watcher_name = os.path.basename(__file__)
    sensor = DistanceSensor(args.digitalPortUsed)
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_distance_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_distance, handlers, args.interval, args.deltaTolerance, "m", watcher_name)
    sensor_watcher.run_loop()


#python3 watcher_light.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 107
if __name__ == "__main__":
    logging_setup.initialize()
    parser = WatcherArgsParser("Distance measurement watcher", idx=107, digital_port=5)
    run(parser.parse_args())