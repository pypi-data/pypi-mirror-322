from evomeai_utils import LogTimer, EConfig
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test')

async def test():
    with LogTimer('test'):
        print('hello, world')


if __name__ == '__main__':
    with LogTimer('test'):
        print('hello, world')

    test()

    LogTimer.output()

    app_config = EConfig.getConfig()
    log.info(app_config.sections())

    my_config = EConfig.getConfig('my.ini')
    log.info(my_config.sections())

    db_config = EConfig.getConfig('folder/db.ini')
    log.info(db_config.get('conn', 'host'))

