#!/usr/bin/env python3

import logging_setup
from domoticz_api_notifier import DomoticzApiNotifier
from grove_api.aht20_sensor import TemperatureHumiditySensor
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import CyclicWatcherArgsParser

def run():
    parser = CyclicWatcherArgsParser("Temperature measurement watcher", idx=104)
    args = parser.parse_args()    
    
    logging_setup.initialize()
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    sensor = TemperatureHumiditySensor(args.interval, args.deltaTolerance)
    sensor.temperature_changed_event += measurement_change_printer.print_measurement_change
    sensor.temperature_changed_event += domoticz_notifier.notify_temperature_changed
    sensor.humidity_changed_event += measurement_change_printer.print_measurement_change
    sensor.humidity_changed_event += domoticz_notifier.notify_humidity_changed
    sensor.run_loop()

#python3 watcher_temperature_humidity.py http://raspberrypi:8080 --interval 1 --deltaTolerance 0.5 --idx 104
if __name__ == "__main__":
    run()