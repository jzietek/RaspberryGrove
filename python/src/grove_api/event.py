class Event(object):
    def __init__(self):
        self._eventHandlers = []
    
    def __iadd__(self, handler):
        self._eventHandlers.append(handler)
        return self

    def __isub__(self, handler):
        self._eventHandlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for event_handler in self._eventHandlers:
            event_handler(*args, **keywargs)