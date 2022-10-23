#!/usr/bin/env python

import random

try:
    from grove.grove_light_sensor_v1_2 import GroveLightSensor
    groveAvailable = True
except ImportError:
    print("Grove not supported. Using mocked light sensor instead.")
    groveAvailable = False


class LightSensor(object):
    def __init__(self, analogPortNumber = 0):
        if (groveAvailable):
            self.sensor = GroveLightSensor(analogPortNumber)
        else:
            self.sensor = None

    def ReadLightIntensity(self):
        if (self.sensor is not None):
            return self.sensor.light
        else:
            return random.random()