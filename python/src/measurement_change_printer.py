class MeasurementChangePrinter(object):
    def __init__(self):
        pass

    def PrintMeasurementChange(self, previousValue, currentValue, delta, unit):
        print(f'Value has changed from {previousValue} to {currentValue} {unit}')