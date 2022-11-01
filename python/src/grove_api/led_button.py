import time
import logging
from value_changed_event import ButtonEvent

class LedButton(object):
    def __init__(self, digital_port_number, button_index = 0):
        self.__logger = logging.getLogger(__name__)
        self.button_pressed_event = ButtonEvent(button_index)
        self.button_long_pressed_event = ButtonEvent(button_index)
        self.button_double_pressed_event = ButtonEvent(button_index)
        try:
            from grove.button import Button
            from grove.grove_ryb_led_button import GroveLedButton
            self.__logger.info('Grove LED button is installed')
            self.__button = GroveLedButton(digital_port_number)
            self.enable_light(False)
            self.__button.on_event = self.__handle_button_event
        except:
            self.__logger.warning("Grove not supported. LED button not installed.")
            self.__button = None


    def __handle_button_event(self, index, event, tm):
        if event & Button.EV_SINGLE_CLICK:
            #self.__logger.info('single click')
            #self.__button.led.light(True)
            self.button_pressed_event()
        elif event & Button.EV_LONG_PRESS:
            #self.__logger.info('long press')
            #self.__button.led.light(False)
            self.button_long_pressed_event()
        elif event & Button.EV_DOUBLE_CLICK:
            self.button_double_pressed_event()


    def enable_light(self, isEnabled):
        if (self.__button is not None):
            self.__button.led.light(isEnabled)
            self.__is_light_on = isEnabled


    def is_light_on(self):
        return self.__is_light_on

    
    def toggle_ligth(self):
        self.enable_light(not self.is_light_on)
        

if (__name__ == '__main__'):
    led_button = LedButton(5)
    led_button.button_pressed_event += print('button pressed')
    led_button.button_long_pressed_event += print('button long pressed')    
    led_button.button_double_pressed_event += print('button double pressed')


    led_button.button_long_pressed_event += led_button.toggle_ligth

    while True:
        time.sleep(1)