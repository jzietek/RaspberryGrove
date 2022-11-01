from grove_api.event import Event


class ValueChangedEvent(Event):
    def __init__(self, measurement_unit):
        self._eventHandlers = []
        self.measurementUnit = measurement_unit