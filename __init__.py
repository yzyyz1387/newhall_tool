# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 13:53
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py
# @Software: PyCharm
from pathlib import Path
from . import score, utils, path
from path import *
logger = utils.log()
Path.mkdir(local) if not Path.exists(local) else ...


