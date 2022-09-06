# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 16:34
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : login_check.py
# @Software: PyCharm
from typing import Optional
from utils import *
import httpx
import json

logger = log()
LOGIN_URL = r'https://app.nwafu.edu.cn/uc/wap/login/check'
headers = {'authority': 'app.nwafu.edu.cn', 'pragma': 'no-cache', 'cache-control': 'no-cache',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'sec-fetch-dest': 'document',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                     'application/signed-exchange;v=b3;q=0.9',
           'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate',
           'referer': 'https://app.nwafu.edu.cn/site/applicationSquare/index?sid=8',
           'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', }


async def login_check(account: str, password: str) -> Optional[int]:
    """
    登录检查
    :param account: 账号
    :param password: 密码
    :return: 1：成功， -1：账号密码错误
    """
    values = {
        'username': account,
        'password': password
    }
    sn = values["username"]
    async with httpx.AsyncClient() as client:
        login = (await client.post(LOGIN_URL, data=values, headers=headers))
        logger.info("检查账号密码...")
        logger.debug("登录返回信息： " + login.text)
        login_status: dict = json.loads(login.text)
        message = login_status['m']
        if message == "操作成功":
            logger.info(sn + "-----密码验证成功")
            return 1
        elif message == "账号或密码错误":
            logger.error(sn + "-----账号或密码错误")
            return -1
        elif message == "错误次数已达最大上限,请稍后再试":
            logger.error(sn + "-----错误次数已达最大上限,请稍后再试")
            return -1

