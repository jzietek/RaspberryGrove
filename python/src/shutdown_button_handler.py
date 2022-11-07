#!/usr/bin/env python3

import os
import time
import logging
import logging_setup
from watcher_args_parser import EventWatcherArgsParser
from grove_api.led_button import LedButton


class ShutdownButtonHandler(object):
    def __init__(self, args):
        logger_name = os.path.basename(__file__)
        self.__logger = logging.getLogger(logger_name)
        self.__button = LedButton(args.digitalPortUsed)
        self.__button.button_pressed_event += self.__handle_single_press
        self.__button.button_double_pressed_event += self.__handle_double_press
        self.__button.button_long_pressed_event += self.__handle_long_press
        self.__button.enable_light(True)
        self.__countdown_senconds = None


    def run_loop(self):    
        while True:
            if (self.__countdown_senconds is not None):
                if (self.__countdown_senconds > 0):
                    self.__countdown_senconds = self.__countdown_senconds - 1
                    self.__button.toggle_ligth()
                    self.__logger.info(f"Shutdown in: {self.__countdown_senconds} s")
                else:
                    self.__logger.info(f"Shutting down")
                    #TODO the actual shutdown
                    self.abort_shutdown()
            time.sleep(1)


    def abort_shutdown(self):
        if (self.__countdown_senconds is not None):
            self.__countdown_senconds = None
            self.__logger.info(f"Shutdown countdown aborted")


    def __handle_single_press(self, sender: LedButton):
        self.abort_shutdown()


    def __handle_double_press(self, sender: LedButton):
        self.abort_shutdown()

    def __handle_long_press(self, sender: LedButton):
        self.__logger.info(f"Shutdown countdown begins")
        self.__countdown_senconds = 30


#python3 watcher_led_button.py http://raspberrypi:8080 --idx 110
if __name__ == "__main__":
    parser = EventWatcherArgsParser("Button events watcher", idx = 110, digital_port = 5)
    args = parser.parse_args()

    logging_setup.initialize('logging.yaml')
    watcher = ShutdownButtonHandler(args)
    watcher.run_loop()