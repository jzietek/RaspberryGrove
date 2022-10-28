import logging
import logging.config
import time
import os
import yaml
import coloredlogs

def setup_logging(path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')


def main():
    #logging.basicConfig(filename='x.log', level=logging.INFO)
    #logging.config.fileConfig('logging.conf')
    setup_logging('logging.yaml')
    
    logger = logging.getLogger('simpleExample')

    logger.info('Started')
    time.sleep(1)
    logger.debug('debug level stuff')
    time.sleep(1)
    logger.info('Finished')

if __name__ == '__main__':
    main()