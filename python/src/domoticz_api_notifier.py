import requests
import logging

class DomoticzApiNotifier(object):
    """
    Sends POST requests to the Domoticz commnad API,
    which is documented here:
    https://www.domoticz.com/wiki/Domoticz_API/JSON_URL
    """
    
    def __init__(self, domoticz_url, idx):
        self.__domoticz_url = domoticz_url
        self.__idx = idx
        self.__logger = logging.getLogger(__name__)
        self.__logger.info(f'{__name__} initialized with Domoticz URL of: {self.__domoticz_url} and IDX: {self.__idx}')


    def _post_value_changed(self, query):
        try:
            requestQuery = f'{self.__domoticz_url}{query}'
            self.__logger.debug(requestQuery)
            response = requests.post(requestQuery)
            self.__logger.debug(response.text)
        except:
            self.__logger.error(f'Exception when sending POST request: {requestQuery}')


    def notify_temperature_changed(self, previous_value, current_value, delta, unit):
        self._post_value_changed(f'/json.htm?type=command&param=udevice&idx={self.__idx}&nvalue=0&svalue={current_value}')


    def notify_humidity_changed(self, previous_value, current_value, delta, unit):
        status_value = 0 #normal
        if (current_value < 30):
            status_value = 2 #dry
        elif (current_value > 40 and current_value < 60):
            status_value = 1 #comfortable
        elif (current_value > 70):
            status_value = 3 #wet
        self._post_value_changed(f'/json.htm?type=command&param=udevice&idx={self.__idx}&nvalue={current_value}&svalue={status_value}')


    def notify_light_changed(self, previous_value, current_value, delta, unit):
        self._post_value_changed(f'/json.htm?type=command&param=udevice&idx={self.__idx}&nvalue=0&svalue={current_value}')


    def notify_distance_changed(self, previous_value, current_value, delta, unit):
        self._post_value_changed(f'/json.htm?type=command&param=udevice&idx={self.__idx}&nvalue=0&svalue={current_value}')


    def notify_motion_detection_changed(self, previous_value, current_value, delta, unit):
        if current_value == 0:
            text = "No motion"
            level = 1
        else:
            level = 4
            text = "Motion detected"
        self._post_value_changed(f'/json.htm?type=command&param=udevice&idx={self.__idx}&nvalue={level}&svalue={text}')


    def notify_moisture_changed(self, previous_value, current_value, delta, unit):
        self._post_value_changed(f'/json.htm?type=command&param=udevice&idx={self.__idx}&nvalue={current_value}')


    def notify_button_pressed(self):
        self._post_value_changed(f'/json.htm?type=command&param=switchlight&idx={self.__idx}&switchcmd=Toggle')
    