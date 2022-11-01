#!/usr/bin/env python3

from grove_api.dht_sensor import DhtSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier


def run(args):
    sensor = DhtSensor(args.digitalPortUsed)
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()
    handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_humidity_changed]
    sensor_watcher = CyclicSensorWatcher(sensor.read_humidity, handlers, args.interval, args.deltaTolerance, "%")    
    sensor_watcher.run_loop()

#python3 watcher_humidity.py http://raspberrypi:8080 --interval 3 --deltaTolerance 1 --idx 105
if __name__ == "__main__":
    parser = WatcherArgsParser("Humidity measurement watcher", idx=105, digital_port=5)
    run(parser.parse_args())