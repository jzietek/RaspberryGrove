import time
import logging
from event_sensor_watcher import Event

class LedButton(object):
    def __init__(self, digital_port_number):
        self.__logger = logging.getLogger(__name__)
        self.button_pressed_event = Event()        
        try:
            from grove.button import Button
            from grove.grove_ryb_led_button import GroveLedButton
            self.__logger.info('Grove LED button is installed')
            self.__button = GroveLedButton(digital_port_number)
            self.__button.on_event = self.__raise_button_event
        except:
            self.__logger.warning("Grove not supported. Using mocked LED button instead.")
            self.__button = None


    def __raise_button_event(self, index, event, tm):
        if event & Button.EV_SINGLE_CLICK:
            self.__logger.info('single click')
            self.__button.led.light(True)
        elif event & Button.EV_LONG_PRESS:
            self.__logger.info('long press')
            self.__button.led.light(False)
        self.button_pressed_event()
        



if (__name__ == '__main__'):
    led_button = LedButton(5)
    led_button.button_pressed_event += print('button pressed handled')
    while True:
        time.sleep(1)