
<div align="center">  
<h1 id="教务系统工具"> 教务系统工具 </h1>

![](https://img.shields.io/badge/Python-3.7%2B-blue)
![](https://img.shields.io/badge/Playwright-chromium-yellow)
![](https://img.shields.io/badge/NWAFU--CP-%E8%A5%BF%E5%86%9C%E5%BC%80%E5%8F%91%E8%80%85%E8%81%94%E7%9B%9F-GREEN)

可查成绩、查通识选修完成情况等

</div>

此前一直没明白教务系统查成绩时的Cookie之一`_WEU` 是哪儿来的 (现在也没攻克)
故本项目通过playwright实现登录并抓取Cookie，虽然有点占内存，但能跑就行</p>

<!-- TOC -->
- [结构](#结构)
  - [login_check/login_check.py](#login_checklogin_checkpy)
  - [path.py](#pathpy)
  - [score.py](#scorepy)
  - [utils.py](#utilspy)
- [使用](#使用)
  - [克隆项目](#克隆项目)
  - [切换到项目目录](#切换到项目目录)
  - [安装依赖（豆瓣源）](#安装依赖豆瓣源)
  - [配置](#配置)
  - [运行](#运行)
    - [查成绩](#查成绩)
    - [查通识选修完成情况](#查通识选修完成情况)
- [日志](#日志)
- [成功运行示例](#成功运行示例)
  - [成绩](#成绩)
  - [选修](#选修)
- [TODO](#todo)
<!-- TOC -->

## 结构

### login_check/login_check.py

检查是否登录成功(用了打卡的登录系统，使用httpx比较快)

### path.py

文件路径

### score.py

通过playwright实现登录并抓取Cookie，而后提交各种请求查询数据

### utils.py

工具集

## 使用

### 克隆项目

```bash
git clone https://github.com/NWAFU-CP/newhall_tool.git
```

### 切换到项目目录

```bash
cd newhall_tool
```

### 安装依赖（豆瓣源）

```bash
pip install -r requirements.txt -i https://pypi.douban.com/simple/
```

### 配置

打开`config.yml`，修改配置：

```yaml
# 配置文件
# 学号： 密码
# 注意冒号后的空格
2019000000: 7355608
```

### 运行
#### 查成绩
```bash
python score.py
```
#### 查通识选修完成情况
```bash
python elective.py
```
## 日志
DEBUG级别日志储存在`nwafu.log`中

## 成功运行示例

### 成绩
```log
2022-08-14 20:43:13,942-INFO: 开始运行，将在1min内完成...
2022-08-14 20:43:14,292-INFO: 检查账号密码...
2022-08-14 20:43:14,292-INFO: 201901xxx-----密码验证成功
2022-08-14 20:43:29,932-INFO: 欢迎您，园长
2022-08-14 20:43:41,088-INFO: 201901xxx 的成绩储存完成
2022-08-14 20:43:41,088-INFO: 正在查询当前学期
2022-08-14 20:43:41,207-INFO: 当前学期为2022-2023学年 秋
2022-08-14 20:43:41,208-INFO: 获取201901xxx的总体成绩...
2022-08-14 20:43:41,889-INFO: 获取完成，正在储存201901xxx的总体成绩
2022-08-14 20:43:41,895-INFO: 201901xxx 的总体成绩储存完成
2022-08-14 20:43:42,055-INFO: 运行时间：28.112958908081055
2022-08-14 20:43:42,056-INFO: 当前学期还没有成绩，将查询最上学期的成绩
2022-08-14 20:43:42,056-INFO: 园长
2022-08-14 20:43:42,056-INFO: 
+----------+------+----------+----------+
| 专业排名  | GPA  | 学分成绩 | 班级排名   |
+----------+------+----------+----------+
|  196/196  | 0.01 |  0.11   |  30/30   |
+----------+------+----------+----------+
2022-08-14 20:43:42,057-INFO: 
+------------+------+----------+----------+----------+------+----------+
|    课程    | 成绩  |  平时成绩 | 期末成绩  | 课程性质  | 学分  | 学分绩点   |
+------------+------+----------+----------+----------+------+----------+
| 教学实习III | 00.0 |   000    |    00    |   必修   | 2.0  |   4.0    |
|   概率论I   | 00.0 |    00    |    00    |   必修   | 2.5  |   2.0    |
+------------+------+----------+----------+----------+------+----------+
```
### 选修

```log
2022-09-07 02:59:04,149-INFO: 开始查选修课，将在1min内完成...
09-07 02:59:04 [INFO] src | 检查账号密码...
09-07 02:59:04 [INFO] src | 2019000000-----密码验证成功
09-07 02:59:10 [INFO] src | 正在获取关键信息
09-07 02:59:11 [INFO] src | 欢迎您，园长
09-07 02:59:16 [INFO] src | 获取关键信息成功！
2022-09-07 02:59:16,983-INFO: 
+-----------------+-----------+----------+
|        类型      | 要求学分  | 已获学分  |
+--------------------+----------+--------+
| 传统文化与世界文明 |   1.0    |   1.0    |
| 人文素养与人生价值 |   1.0    |   1.0    |
| 农业发展与政策法规 |   1.0    |   1.0    |
|      公共艺术    |   1.0    |   1.0    |
|    创新创业教育   |   2.0    |   2.0    |
| 科技创新与社会发展 |   1.0    |   1.0    |
| 生态环境与人类命运 |   1.0    |   1.0    |
|     新生研讨课    |   1.0    |   1.0    |
+--------------------+----------+----------+
09-07 02:59:16 [INFO] src | 运行时间：12.83422565460205


```
## TODO
- [x] 查成绩
- [x] 通识选修
- [ ] 课表
- [ ] ...
