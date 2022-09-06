# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/9/6 22:40
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : elective.py
# @Software: PyCharm
from prettytable import PrettyTable

from utils_net import *
from user_agent import get_user_agent
from utils import *
from .path import *

logger = log()


@time_log
async def check_elective(account: str, password: str):
    """
    检查选课情况
    :param account: 账号
    :param password: 密码
    :return:
    """
    logger.info("开始查选修课，将在1min内完成...")
    main_list = await get_main_cookies(account, password)
    if main_list:
        name = main_list[0]
        page = main_list[2]
        page1 = main_list[3]
        context = main_list[4]
        browser = main_list[5]
        main_cookies = main_list[1]
        _WEU = main_cookies["_WEU"]
        MOD_AUTH_CAS = main_cookies["MOD_AUTH_CAS"]
        data = {"XH": account}
        headers = get_user_agent()
        headers["Cookie"] = f"_WEU={_WEU}; MOD_AUTH_CAS={MOD_AUTH_CAS}"
        url_pydm = 'https://newehall.nwafu.edu.cn/jwapp/sys/xywccx/modules/xywccx/grpyfacx.do'
        url_xqxn = 'https://newehall.nwafu.edu.cn/jwapp/sys/cjcx/modules/cjcx/cxdqxnxq.do'
        pydm_dict = await httpx_post(url_pydm, headers, main_cookies, data)
        semester = await httpx_post(url_xqxn, headers, main_cookies, data)
        semester_DM = semester["datas"]["cxdqxnxq"]["rows"][0]["DM"]
        if pydm_dict:
            pydm = pydm_dict["datas"]["grpyfacx"]["rows"][0]["PYFADM"]
            url_ele = 'https://newehall.nwafu.edu.cn/jwapp/sys/xywccx/modules/xywccx/cxscfakz.do'
            data_ = {
                'XH': account,
                'PYFADM': pydm,
                'BYNJDM': '-',
                'SCLBDM': '04',
                'XNXQDM': semester_DM,
            }
            ele_dict = await httpx_post(url_ele, headers, main_cookies, data_)
            if ele_dict:
                temp = []
                try:
                    row = ele_dict["datas"]["cxscfakz"]["rows"]
                    for detail in row:
                        if detail["KCXZDM_DISPLAY"] == "任选":
                            temp.append(detail)
                except KeyError:
                    logger.info("暂无选修课信息")
                if temp:
                    temp_dict = {}
                    temp_list = []
                    for detail in temp:
                        temp_dict[detail["KZM"]] = [detail["YQXF"], detail["WCXF"]]
                        temp_list.append([detail["KZM"], detail["YQXF"], detail["WCXF"]])
                    tb = PrettyTable()
                    tb.field_names = ["类型", "要求学分", "已获学分"]
                    tb.add_rows(temp_list)
                    logger.info('\n' + str(tb))
                    return temp_list
            await context.close()
            await browser.close()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    with open(config, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for i in data:
            loop.run_until_complete(check_elective(str(i), data[i]))
