#!/usr/bin/env python3

import os
import logging_setup
from grove_api.motion_sensor import MotionSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run(args):
    watcher_name = os.path.basename(__file__)
    sensor = MotionSensor(args.digitalPortUsed)
    sensor_watcher = CyclicSensorWatcher(sensor.is_motion_detected, args.interval, args.deltaTolerance, "boolean", watcher_name)
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()

    sensor_watcher.add_sensor_event_subscriber(measurement_change_printer.print_measurement_change)
    sensor_watcher.add_sensor_event_subscriber(domoticz_notifier.notify_motion_detection_changed)

    try:
        sensor_watcher.run_loop()
    finally:
        sensor_watcher.remove_sensor_event_subscriber(measurement_change_printer.print_measurement_change)
        sensor_watcher.remove_sensor_event_subscriber(domoticz_notifier.notify_motion_detection_changed)
    pass

#python3 watcher_light.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 108
if __name__ == "__main__":
    logging_setup.initialize()
    parser = WatcherArgsParser("Motion detection watcher", idx=108, digital_port=16)
    run(parser.parse_args())