class MeasurementChangePrinter(object):
    def __init__(self):
        pass

    def print_measurement_change(self, previous_value, current_value, delta, unit):
        print(f'Value has changed from {previous_value} to {current_value} {unit}')