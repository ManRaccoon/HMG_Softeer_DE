import logging
import datetime as dt

# 로깅 기본설정
logging.basicConfig(
    filename = 'etl_project_log.txt',
    format = '%(message)s',
    level = logging.INFO,
    )

logger = logging.getLogger()

# 메세지 형식 지정하여 로깅 진행 함수
def message(msg):
    logtime = dt.datetime.now().strftime("%Y-%B-%d-%H-%M-%S")
    logger.info(f'{logtime}, {msg}')