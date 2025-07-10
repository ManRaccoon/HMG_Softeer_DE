import logging
import datetime as dt

logging.basicConfig(
    filename = 'etl_project_log.txt',
    format = '%(message)s',
    level = logging.INFO,
    )

logger = logging.getLogger()

def start(work):
    logtime = dt.datetime.now().strftime("%Y-%B-%d-%H-%M-%S")
    logger.info(f'{logtime}, {work} 시작')

def end(work):
    logtime = dt.datetime.now().strftime("%Y-%B-%d-%H-%M-%S")
    logger.info(f'{logtime}, {work} 종료')