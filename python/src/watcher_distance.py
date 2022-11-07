#!/usr/bin/env python3

import logging_setup
from grove_api.distance_sensor import DistanceSensor
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import CyclicWatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run():
    parser = CyclicWatcherArgsParser("Distance measurement watcher", idx=107, digital_port=5)
    args = parser.parse_args()

    logging_setup.initialize()
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    sensor = DistanceSensor(args.digitalPortUsed, args.interval, args.delta_tolerance)
    sensor.distance_changed_event += measurement_change_printer.print_measurement_change
    sensor.distance_changed_event += domoticz_notifier.notify_distance_changed
    sensor.run_loop()


#python3 watcher_light.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 107 -d 5
if __name__ == "__main__":
    run()