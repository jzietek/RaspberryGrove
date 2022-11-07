import logging
import time

class PollingSensor(object):
    def __init__(self, logger_name, interval, delta_tolerance):
        self._interval = interval
        self._delta_tolerance = delta_tolerance
        self._logger = logging.getLogger(logger_name)
        self._sensor = None
        self._previous_value = 0

    def _log_loop_started(self):
        self._logger.info("Starting measurement loop")
        self._logger.info(f'Change tolerance: {self._delta_tolerance}')
        self._logger.info(f'Polling interval: {self._interval} seconds')

    def _change_significant(self, current, previous):
        if (abs(current - previous) > self._delta_tolerance):
            return True
        else:
            return False

    def _wait_polling_interval(self):
        time.sleep(self._interval)