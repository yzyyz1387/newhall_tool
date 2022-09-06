# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/9/6 20:10
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : utils_net.py
# @Software: PyCharm
import os
from typing import Dict, Optional, List, Union

import httpx
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from login_check.login_check import login_check

from utils import *


logger = log()


async def browser_init(**kwargs) -> Optional[Browser]:
    global _browser
    try:
        browser = await async_playwright().start()
        _browser = await browser.chromium.launch(**kwargs)
        return _browser
    except NotImplementedError:
        logger.warning("windows环境下 初始化playwright失败，相关功能将被限制....")
    except Exception as e:
        logger.warning(f"启动chromium发生错误 {type(e)}：{e}")
        try:
            if _browser:
                await _browser.close()
        except NameError:
            logger.info("正在安装浏览器...")
            os.system("playwright install chromium")
    return None


async def httpx_get(url: str, cookies: Dict[str, str] = None) -> Optional[str]:
    """
    httpx get请求
    :param url: 请求地址
    :param cookies: cookies
    :return:
    """
    try:
        async with httpx.AsyncClient(cookies=cookies) as client:
            r = await client.get(url)
            return r.text
    except Exception as e:
        logger.warning(f"请求失败 {type(e)}：{e}")
        return None


async def httpx_post(
        url: str,
        headers: Dict[str, str] = None,
        cookies: Dict[str, str] = None,
        data: Dict[str, str] = None,
        type_: str = "json",
) -> Optional[str]:
    """
    httpx post请求
    :param headers: headers
    :param url: 请求地址
    :param cookies: cookies
    :param data: post数据
    :param type_: 返回类型
    :return:
    """
    try:
        async with httpx.AsyncClient(cookies=cookies, headers=headers) as client:
            r = await client.post(url, data=data)
            if type_ == "json":
                return r.json()
            else:
                return r.text
    except Exception as e:
        logger.warning(f"请求失败 {type(e)}：{e}")
        return None


async def get_main_cookies(
        account: str,
        password: str,
    ) -> Optional[
    list[
        Union[
            str,
            dict[str, str],
            Page,
            Page,
            BrowserContext,
            Browser
            ]
        ]
    ]:
    """
    获取主站cookies
    :param password: 账号
    :param account: 密码
    :return:
    """
    status = await login_check(account, password)
    browser = await browser_init()
    context = await browser.new_context(locale="zh-CN")
    if status == -1:
        logger.warning("首次验证账号或密码错误，正在进行第二次尝试...")
        page = await playwright_login(context, account, password)
        if not page:
            logger.warning("账号或密码错误")
            return None
    else:
        page = await playwright_login(context, account, password)
        logger.info("正在获取关键信息")
        await page.wait_for_url(
            "https://newehall.nwafu.edu.cn/ywtb-portal/Lite/index.html?browser=no#/work_bench/Lite_workbench")
        name_selector = (await page.query_selector(
            "//html/body/div[2]/div/div/div/div[2]/header/div/div/div/div[1]/div[3]/div/span/div/span"))
        name = (await name_selector.inner_text())
        logger.info(f"欢迎您，{name}")
        await page.goto(
            "https://newehall.nwafu.edu.cn/ywtb-portal/Lite/index.html?browser=no#/work_bench/Lite_workbench")
        await page.locator("text=本科教务系统").click()
        await page.locator("text=成绩中心").click()
        async with page.expect_popup(timeout=600000) as popup_info:
            await page.locator("text=成绩查询").nth(1).click()
        page1 = await popup_info.value
        await page1.goto('https://newehall.nwafu.edu.cn/jwapp/sys/cjcx/*default/index.do')
        await page1.locator("li[role=\"tab\"]:has-text(\"全部\")").click()
        cookies = list(await context.cookies())
        _WEU = ""
        MOD_AUTH_CAS = ""
        cookies_r = {}
        for i in cookies:
            if i['name'] == '_WEU':
                _WEU = i['value']
            if i['name'] == 'MOD_AUTH_CAS':
                MOD_AUTH_CAS = i['value']
        if _WEU and MOD_AUTH_CAS:
            cookies_r['_WEU'] = _WEU
            cookies_r['MOD_AUTH_CAS'] = MOD_AUTH_CAS
            logger.info("获取关键信息成功！")
            logger.debug(f"cookies: {cookies_r}")
            return [name, cookies_r, page, page1, context, browser]
        else:
            logger.warning("获取cookies失败")
            return None


async def playwright_login(context: BrowserContext, account, password) -> Optional[Page]:
    page = await context.new_page()
    await page.goto(
        "https://authserver.nwafu.edu.cn/authserver/login?service=https%3A%2F%2Fnewehall.nwafu.edu.cn%3A443"
        "%2Flogin%3Fservice%3Dhttps%3A%2F%2Fnewehall.nwafu.edu.cn%2Fywtb-portal%2FLite%2Findex.html%3Fbrowser"
        "%3Dno%23%2Fwork_bench%2FLite_workbench")
    await page.locator("[placeholder=\"请输入学号\\/工号\"]").click()
    await page.locator("[placeholder=\"请输入学号\\/工号\"]").fill(account)
    await page.locator("[placeholder=\"请输入密码\"]").click()
    await page.locator("[placeholder=\"请输入密码\"]").fill(password)
    await page.locator("#login_submit").click()
    await page.wait_for_timeout(100)
    content = await page.content()
    if "冻结" in content:
        logger.warning("账号被冻结，请注意查看手机短信，并在解冻后手动登录一次")
        logger.warning("账号被冻结，请注意查看手机短信，并在解冻后手动登录一次")
        logger.warning("账号被冻结，请注意查看手机短信，并在解冻后手动登录一次")
        return None
    elif "错误" in content:
        logger.warning("账号或密码错误，请检查后重试")
        return None
    else:
        return page
