# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/8/14 13:53
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py
# @Software: PyCharm
import signal
from . import score, utils, path, login_check, elective

from .utils import *
from .path import *
logger = utils.log()
Path.mkdir(local) if not Path.exists(local) else ...



