import time
import logging


class LedLight(object):
    def __init__(self, digital_port_number):
        self.__logger = logging.getLogger(__name__)
        try:
            from grove.grove_led import GroveLed
            self.__logger.info('Grove LED Light is installed')
            self.__light = GroveLed(digital_port_number)
        except:
            self.__logger.warning("Grove not supported. LED light not installed.")
            self.__light = None
        self.enable_light(True)


    def enable_light(self, isEnabled):
        self.is_light_on = isEnabled
        self.__logger.info("LED Light ON" if isEnabled else "LED Light OFF")
        if (self.__light is not None):
            self.__light.On() if isEnabled else self.__light.off()
    

    def toggle_ligth(self):
        self.enable_light(not self.is_light_on)

    def blink(self, interval_milliseconds = 1000):
        while True:
            self.toggle_ligth()
            time.sleep(interval_milliseconds * 0.001)

        
if (__name__ == '__main__'):
    led_light = LedLight(16)
    led_light.blink(250)
