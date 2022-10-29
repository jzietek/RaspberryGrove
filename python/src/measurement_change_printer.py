import logging

class MeasurementChangePrinter(object):
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        pass

    def print_measurement_change(self, previous_value, current_value, delta, unit):
        self.__logger.info(f'Value has changed from {previous_value} to {current_value} {unit}')