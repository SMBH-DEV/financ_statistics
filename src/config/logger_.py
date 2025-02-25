import loguru
from loguru import logger
from pathlib import Path


class _RecordsFilter:

    @staticmethod
    def by_level(level: str):

        def _wrap(record: 'loguru.Record'):
            return record['level'].name == level

        return _wrap


def init():
    _levels = ["SUCCESS", "ERROR", "INFO", "DEBUG", "CRITICAL", "TOTAL", "WARNING"]
    format_ = "{time:DD-MM-YYYY at HH:mm:ss} | {level: <8} | file: {file: ^20} | func: {function: ^20} | line: {line: >3} | message: {message}"
    LOGS_DIR = Path(__file__).parent.parent / 'logs'
    
    for level in _levels:
        logger.add(LOGS_DIR / f'{level.lower()}.log',
                   format=format_,
                   filter=_RecordsFilter.by_level(level) if level != "TOTAL" else None,
                   diagnose=True,
                   rotation='10MB',
                   retention=5,
                   compression='zip'
                   )