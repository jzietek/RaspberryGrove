#!/usr/bin/env python3

import logging_setup
from grove_api.moisture_sensor import SoilMoistureSensor
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import CyclicWatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

def run():
    parser = CyclicWatcherArgsParser("Moisture measurement watcher", idx=109, analog_port=2) 
    args = parser.parse_args()

    logging_setup.initialize()
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    sensor = SoilMoistureSensor(args.analogPortUsed, args.interval, args.deltaTolerance)
    sensor.moisture_changed_event += measurement_change_printer.print_measurement_change
    sensor.moisture_changed_event += domoticz_notifier.notify_moisture_changed
    sensor.run_loop()

#python3 watcher_moisture.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 109 -a 2
if __name__ == "__main__":
    run()