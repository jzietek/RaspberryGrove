#!/usr/bin/env python3

import os
import logging_setup
from grove_api.led_button import LedButton
from event_sensor_watcher import EventSensorWatcher
from measurement_change_printer import MeasurementChangePrinter
from watcher_args_parser import WatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier


def test1():
    print('test1')

def run(args):
    watcher_name = os.path.basename(__file__)
    button = LedButton(args.digitalPortUsed)
    #domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
    #measurement_change_printer = MeasurementChangePrinter()
    #handlers = [measurement_change_printer.print_measurement_change, domoticz_notifier.notify_light_changed]
    handlers = [test1]
    button_watcher = EventSensorWatcher(button.button_pressed_event, handlers, watcher_name)  
    button_watcher.run_listener()


#python3 watcher_led_button.py http://192.168.0.188:8080 --idx 110
if __name__ == "__main__":
    logging_setup.initialize()
    parser = WatcherArgsParser("Button events watcher", idx=110, digital_port=0) 
    run(parser.parse_args())