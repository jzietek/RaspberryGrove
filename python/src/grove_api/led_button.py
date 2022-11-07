import time
import logging

from grove_api.event import Event


class LedButton(object):
    def __init__(self, digital_port_number):
        self._logger = logging.getLogger(__name__)
        self.__digital_port_number = digital_port_number
        self.button_pressed_event = Event()
        self.button_long_pressed_event = Event()
        self.button_double_pressed_event = Event()
        try:
            from grove.button import Button
            from grove.grove_ryb_led_button import GroveLedButton
            self._logger.info('Grove LED button is installed')
            self.__button = GroveLedButton(digital_port_number)
            self.__button_constants = Button()
            self.enable_light(False)
            self.__button.on_event = self._handle_button_event
        except:
            self._logger.warning("Grove not supported. LED button not installed.")
            self.__button = None


    def _handle_button_event(self, index, event, tm):
        if self.__button is not None:
            if event & self.__button_constants.EV_SINGLE_CLICK:
                self._logger.info(f'Button D{self.__digital_port_number} event: single click')                
                self.button_pressed_event(self)
            elif event & self.__button_constants.EV_LONG_PRESS:
                self._logger.info(f'Button D{self.__digital_port_number} event: long press')
                self.__button.led.light(False)
                self.button_long_pressed_event(self)
            elif event & self.__button_constants.EV_DOUBLE_CLICK:
                self._logger.info(f'Button D{self.__digital_port_number} event: double click')
                self.button_double_pressed_event(self)


    def enable_light(self, isEnabled):
        if (self.__button is not None):
            self.__button.led.light(isEnabled)
        self.is_light_on = isEnabled


    def toggle_ligth(self):
        self.enable_light(not self.is_light_on)
        

def handle_single_click(sender: LedButton):
    print('single click')
    if (sender is not None):
        sender.toggle_ligth()


if (__name__ == '__main__'):
    led_button = LedButton(5)
    led_button.button_pressed_event += handle_single_click
    while True:
        time.sleep(1)