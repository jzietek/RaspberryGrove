#!/usr/bin/env python3

import os
import time
import argparse
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


    def __handle_shutdown_countdown(self):
        if (self.__countdown_senconds is None):
            return False
        else:
            self.__button.blink(0.2)
            while(self.__countdown_senconds is not None and self.__countdown_senconds > 0):
                self.__logger.info(f"Shutdown in: {self.__countdown_senconds} s")
                self.__countdown_senconds = self.__countdown_senconds - 1
                time.sleep(1)
            #Check the case when the countdown has been aborted
            if (self.__countdown_senconds is None):
                return False
            else:
                return True


    def shutdown(self):
        self.__countdown_senconds = None
        self.__logger.info(f"Shutting down")
        try:
            os.system("shutdown -h now")
        except Exception as ex:
            self.__logger.error(ex)
        


    def run_loop(self):    
        while True:
            if (self.__handle_shutdown_countdown()):
                self.shutdown()
            time.sleep(1)


    def abort_shutdown(self):
        if (self.__countdown_senconds is not None):
            self.__countdown_senconds = None
            self.__button.enable_light(True)
            self.__logger.info(f"Shutdown countdown aborted")


    def __handle_single_press(self, sender: LedButton):
        self.abort_shutdown()


    def __handle_double_press(self, sender: LedButton):
        self.abort_shutdown()


    def __handle_long_press(self, sender: LedButton):
        self.__logger.info(f"Shutdown countdown begins")
        self.__countdown_senconds = 30


#sudo -E python3 shutdown_button_handler.py -d 5
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shutdown button")
    parser.add_argument('-d', '--digitalPortUsed', type=int, default=5, help='Number of a digital port on the device, where the device is pluged-in.')
    args = parser.parse_args()

    logging_setup.initialize('logging.yaml')
    watcher = ShutdownButtonHandler(args)
    watcher.run_loop()