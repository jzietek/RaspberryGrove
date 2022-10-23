from grove_api.dht_sensor import DhtSensor
from cyclic_sensor_watcher import CyclicSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier


def run(args):
    sensor = DhtSensor(args.digitalPortUsed)
    sensor_watcher = CyclicSensorWatcher(sensor.read_humidity, args.interval, args.deltaTolerance, "%")    
    domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    measurement_change_printer = MeasurementChangePrinter()

    sensor_watcher.add_sensor_event_subscriber(measurement_change_printer.print_measurement_change)
    sensor_watcher.add_sensor_event_subscriber(domoticz_notifier.notify_humidity_changed)

    try:
        sensor_watcher.run_loop()
    finally:
        sensor_watcher.remove_sensor_event_subscriber(measurement_change_printer.print_measurement_change)
        sensor_watcher.remove_sensor_event_subscriber(domoticz_notifier.notify_humidity_changed)

#python3 watcher_humidity.py http://192.168.0.188:8080 --interval 3 --deltaTolerance 1 --idx 105
if __name__ == "__main__":
    parser = WatcherArgsParser("Humidity measurement watcher", idx=105, digital_port=5)
    run(parser.parse_args())