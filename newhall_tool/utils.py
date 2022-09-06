# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 13:17
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : utils.py
# @Software: PyCharm
import os
import sys
import signal
import logging
from functools import wraps
from pathlib import Path
from typing import Optional, Dict, Any, Union

import aiofiles
import yaml


def log():
    """
    日志
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    console_handler.setLevel(logging.INFO)
    logfile = 'nwafu.log'
    File_handler = logging.FileHandler(logfile, mode='a', encoding='utf-8')
    File_handler.setFormatter(formatter)
    File_handler.setLevel(logging.DEBUG)
    if not logger.handlers:
        logger.addHandler(File_handler)
        logger.addHandler(console_handler)
        print(logger.handlers)
    return logger


async def yaml_load(path: Union[str, Path]) -> Dict[Any, Any]:
    """
    读取yaml文件
    :param path: 文件路径
    :return:
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


async def yaml_dump(path: Union[str, Path], data: dict) -> None:
    """
    写入yaml文件
    :param path: 文件路径
    :param data: 数据
    :return:
    """
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)


async def async_w(file, content) -> None:
    """
    异步写入文件
    :param file: 文件
    :param content: 内容
    :return:
    """
    async with aiofiles.open(file, 'w', encoding='utf-8') as f:
        await f.write(content)
        await f.close()


async def async_r(file):
    """
    异步读取文件
    :param file: 文件
    :return: 内容
    """
    async with aiofiles.open(file, 'r', encoding='utf-8') as f:
        content = await f.read()
        await f.close()
        return content


def time_log(func):
    logger = log()

    @wraps(func)
    async def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        data = await func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"运行时间：{end_time - start_time}")
        return data

    return wrapper


def signal_handler(signum, frame):
    print('signal_handler: caught signal ' + str(signum))
    if signum == signal.SIGINT.value:
        print('操作被用户停止...')
        sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)
