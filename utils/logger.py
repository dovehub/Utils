import os
import sys
import copy
from functools import wraps
from typing import Optional, Union

from loguru import logger as _logger

__all__ = [
    'Log',
]

_logger.remove()


def Log(prefix: str,
        path: Optional[str] = None,
        filename: Optional[str] = None,
        format: Optional[str] = None,
        level: Union[str, int] = 'WARNING',
        rotation: str = "00:00",
        retention: str = "30 days",
        enqueue: bool = False) -> _logger:
    """
    prefix: 标识
    `example: logger = Log('hello')
    logger.info('hi')`
    output: 2020-10-12 14:57:37.019 | DEBUG    | __main__:<module>:1 | heelo | hi
    path: log文件存储路径
    filename: log文件名，默认为prefix值
    format: log输出格式
    level: log文件记录的最低级别
    rotation retention enqueue 同 loguru
    """
    if path is None:  # log路径
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 定位到log日志文件
        path = os.path.join(basedir, 'logs')

    if filename is None:  # log文件名称
        filename = prefix
    if not filename.endswith('.log'):
        filename = filename + '.log'

    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, filename)
    if format is None:
        format = f"<red>[</red> <green>{{time:YYYY-MM-DD HH:mm:ss.SSS}}</green> | <level>{{level: <8}}</level> | <cyan>{{name}}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> | <fg #FFC0CB>{prefix}</fg #FFC0CB> <red>]</red> <level>{{message}}</level>"
    logger = copy.deepcopy(_logger)
    logger.add(sys.stdout, format=format, enqueue=enqueue)
    logger.add(file_path,
               format=format,
               level=level,
               rotation=rotation,
               retention=retention,
               enqueue=enqueue)
    return logger


def catch(*a, **kw):

    def _catch(func):  # 解决self.logger作为装饰器的问题

        @wraps(func)
        def out_wrapper(self, *args, **kwargs):
            logger = self.logger.opt(depth=1)

            @logger.catch(*a, **kw)
            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            return wrapper(self, *args, **kwargs)

        return out_wrapper

    return _catch
