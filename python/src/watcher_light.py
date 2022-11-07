#!/usr/bin/env python3

import logging_setup
from grove_api.light_sensor import LightSensor
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import CyclicWatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run():
    parser = CyclicWatcherArgsParser("Light measurement watcher", idx=106, analog_port=0) 
    args = parser.parse_args()

    logging_setup.initialize()
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    sensor = LightSensor(args.analogPortUsed, args.interval, args.deltaTolerance)
    sensor.light_changed_event += measurement_change_printer.print_measurement_change
    sensor.light_changed_event += domoticz_notifier.notify_light_changed
    sensor.run_loop()

#python3 watcher_light.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 106 -a 0
if __name__ == "__main__":
    run()