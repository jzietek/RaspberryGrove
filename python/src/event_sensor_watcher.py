import logging
import time
from value_changed_event import Event


# class EventSensorWatcher(object):
#     def __init__(self, event, sensor_event_handlers, watcher_name = None):
#         self.__event = event
        
#         if (watcher_name is not None):
#             self.__logger = logging.getLogger(watcher_name)
#         else:
#             self.__logger = logging.getLogger()

#         if (sensor_event_handlers is None):
#             self.__sensor_event_handlers = []
#         else:
#             self.__sensor_event_handlers = sensor_event_handlers 


#     def add_event_subscriber(self,sensor_event_handler):
#         self.__event += sensor_event_handler

         
#     def remove_event_subscriber(self,sensor_event_handler):
#         self.__event -= sensor_event_handler


#     def run_listener(self):
#         self.__logger.info('Starting LED button events watcher')
#         for handler in self.__sensor_event_handlers:
#             self.add_event_subscriber(handler)
#         try:            
#             while True:
#                 time.sleep(1)
#         finally:
#             for handler in self.__sensor_event_handlers:
#                 self.remove_event_subscriber(handler)