#!/usr/bin/env python

import random

try:
    from grove.grove_light_sensor_v1_2 import GroveLightSensor
    (grove_available) = True
except ImportError:
    print("Grove not supported. Using mocked light sensor instead.")
    (grove_available) = False


class LightSensor(object):
    def __init__(self, analog_port_number = 0):
        if (grove_available):
            self.__sensor = GroveLightSensor(analog_port_number)
        else:
            self.__sensor = None

    def read_light_intensity(self):
        if (self.__sensor is not None):
            return self.__sensor.light
        else:
            return random.random()