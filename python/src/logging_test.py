import logging
import logging.config
import time
import logging_setup

def main():
    #logging.basicConfig(filename='x.log', level=logging.INFO)
    logging_setup.initialize('logging.yaml')
    
    logger = logging.getLogger('simpleExample')
    #logger = logging.getLogger()

    logger.info('Started')
    time.sleep(1)
    logger.debug('debug level stuff')
    time.sleep(1)
    logger.info('Finished')

if __name__ == '__main__':
    main()