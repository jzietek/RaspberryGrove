#!/usr/bin/env python3
import os
import time
import logging
import logging_setup
from grove_api.led_button import LedButton
from watcher_args_parser import EventWatcherArgsParser
from domoticz_api_notifier import DomoticzApiNotifier


class ButtonWatcher(object):
    def __init__(self, args):
        watcher_name = os.path.basename(__file__)
        self.__logger = logging.getLogger(watcher_name)
        self.__domoticz_notifier = DomoticzApiNotifier(args.domoticzHost, args.idx)
        self.__button = LedButton(args.digitalPortUsed)
        self.__button.button_pressed_event += self.__handle_single_press
        self.__button.button_double_pressed_event += self.__handle_double_press
        self.__button.button_long_pressed_event += self.__handle_long_press


    def run(self):    
        while True:
            time.sleep(1)


    def __handle_single_press(self, sender: LedButton):
        self.__logger.info(f"Button event: single press")
        self.__domoticz_notifier.notify_button_pressed()


    def __handle_double_press(self, sender: LedButton):
        self.__logger.info(f"Button event: double press")


    def __handle_long_press(self, sender: LedButton):
        self.__logger.info(f"Button event: long press")


#python3 watcher_led_button.py http://raspberrypi:8080 --idx 110
if __name__ == "__main__":
    logging_setup.initialize('logging.yaml')
    parser = EventWatcherArgsParser("Button events watcher", idx = 110, digital_port = 5)
    watcher = ButtonWatcher(parser.parse_args())
    watcher.run()