class ValueChangedEvent(object):
    def __init__(self, measurementUnit):
        self.__eventHandlers = []
        self.measurementUnit = measurementUnit
    
    def __iadd__(self, handler):
        self.__eventHandlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__eventHandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for eventHandlers in self.__eventHandlers:
            eventHandlers(*args, **keywargs)