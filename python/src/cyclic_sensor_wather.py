import time
from value_changed_event import ValueChangedEvent

class CyclicSensorWatcher(object):
    def __init__(self, objMethod, interval, deltaTolerance, unit):
        self.objMethod = objMethod
        self.interval = interval
        self.tolerance = deltaTolerance
        self.unit = unit
        self.lastKnownValue = 0
        self.OnMeasurementChanged = ValueChangedEvent(self.unit)
        pass

    def AddSubscribersForMeasurementChangedEvent(self,objMethod):
        self.OnMeasurementChanged += objMethod
         
    def RemoveSubscribersForMeasurementChangedEvent(self,objMethod):
        self.OnMeasurementChanged -= objMethod

    def MeasurementChanged(self, measuredValue):
        previousValue = self.lastKnownValue
        self.lastKnownValue = measuredValue
        delta = measuredValue - previousValue
        self.OnMeasurementChanged(previousValue, measuredValue, delta, self.OnMeasurementChanged.measurementUnit)

    def RunLoop(self):        
        while (True):
            measuredValue = self.objMethod()
            if (abs(measuredValue - self.lastKnownValue) > self.tolerance):
                self.MeasurementChanged(measuredValue)
            
            time.sleep(self.interval)
