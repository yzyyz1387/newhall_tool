# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 13:17
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : utils.py
# @Software: PyCharm
import os
import sys
import logging
from typing import Optional

import aiofiles


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

