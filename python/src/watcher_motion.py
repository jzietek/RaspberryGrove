#!/usr/bin/env python3

import time
import logging_setup
from grove_api.motion_sensor import MotionSensor
from watcher_args_parser import CyclicWatcherArgsParser
#from measurement_change_printer import MeasurementChangePrinter
#from domoticz_api_notifier import DomoticzApiNotifier

class MotionWatcher(object):
    def __init__(self, args):
        #self.__domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
        #self.__measurement_change_printer = MeasurementChangePrinter()
        self.__sensor = MotionSensor(args.digitalPortUsed)
        self.__sensor.motion_detection_event += self.__handle_motion_detected

    def __handle_motion_detected(self, sender: MotionSensor):
        self.__logger.info(f"Motion detected!")
        #self.__domoticz_notifier.notify_motion_detection_changed()
        #self.__measurement_change_printer.print_measurement_change()

    
    def run_loop(self):
        while(True):
            time.sleep(1)


#python3 watcher_light.py http://raspberrypi:8080 --interval 1 --deltaTolerance 1 --idx 108 -d 16
if __name__ == "__main__":
    parser = CyclicWatcherArgsParser("Motion detection watcher", idx=108, digital_port=16)
    args = parser.parse_args()

    logging_setup.initialize()
    watcher = MotionWatcher(args)
    watcher.run_loop()