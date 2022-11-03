import argparse


class EventWatcherArgsParser(object):
    def __init__(self, description, idx = 0, digital_port = 0):
        self._parser = argparse.ArgumentParser(description=description)
        self._parser.add_argument('domoticzHost', default="http://raspberrypi:8080", help='Location of the Domoticz server. <IP/Hostname>:<PORT>')
        self._parser.add_argument('-x', '--idx', type=int, default=idx, help='Domoticz IDX number assigned to the related virtual device.')
        self._parser.add_argument('-d', '--digitalPortUsed', type=int, default=digital_port, help='Number of a digital port on the device, where the sensor is pluged-in.')

    def parse_args(self):
        return self.__parser.parse_args()


class CyclicWatcherArgsParser(EventWatcherArgsParser):
    def __init__(self, description, idx = 0, digital_port = 0, analog_port = 0):
        EventWatcherArgsParser.__init__(self, description, idx, digital_port)
        self._parser.add_argument('-i','--interval', type=int, default=1, help='Measurement interval time in seconds.')
        self._parser.add_argument('-t', '--deltaTolerance', default=0.5, type=float, help='Measurement change is reported, if previous measurement differs by more than this delta tolerance value.')
        self._parser.add_argument('-a', '--analogPortUsed', type=int, default=analog_port, help='Number of an analog port on the device, where the sensor is pluged-in.')