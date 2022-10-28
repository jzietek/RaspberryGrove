#!/usr/bin/env python3

import logging
import logging.config
from grove_api.light_sensor import LightSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def run(args):
    sensor = LightSensor(args.analogPortUsed)
    sensor_watcher = CyclicSensorWatcher(sensor.read_light_intensity, args.interval, args.deltaTolerance, "Lux")    
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()

    sensor_watcher.add_sensor_event_subscriber(measurement_change_printer.print_measurement_change)
    sensor_watcher.add_sensor_event_subscriber(domoticz_notifier.notify_light_changed)

    try:
        sensor_watcher.run_loop()
    finally:
        sensor_watcher.remove_sensor_event_subscriber(measurement_change_printer.print_measurement_change)
        sensor_watcher.remove_sensor_event_subscriber(domoticz_notifier.notify_light_changed)

#python3 watcher_light.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 106
if __name__ == "__main__":
    parser = WatcherArgsParser("Light measurement watcher", idx=106, analog_port=0) 
    run(parser.parse_args())