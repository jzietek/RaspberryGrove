import requests

class DomoticzApiNotifier(object):
    def __init__(self, domoticz_url, idx):
        self.__domoticz_url = domoticz_url
        self.__idx = idx

    def _post_value_changed(self, query):
        try:
            requestQuery = f'{self.__domoticz_url}{query}'
            print(requestQuery)
            response = requests.post(requestQuery)
            print(response.text)
        except:
            print(f'Exception when sending POST request: {requestQuery}')

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
