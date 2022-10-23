class ValueChangedEvent(object):
    def __init__(self, measurement_unit):
        self.__eventHandlers = []
        self.measurementUnit = measurement_unit
    
    def __iadd__(self, handler):
        self.__eventHandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventHandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for event_handler in self.__eventHandlers:
            event_handler(*args, **keywargs)