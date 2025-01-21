# coding: utf-8
r"""
自动化Automation
    randomAcknowledgement - 随机确认消息
    autoSend - 自动发送
    autoClassNotice - 自动发布课程通知
"""
__version__ = "0.1"
__author__ = "mingwe <shannonhacker@outlook.com>"
# __all__ = [
#     name
#     for name, obj in globals().items()
#     if all(
#         [
#             not name.startswith("_"),
#             not isinstance(obj, types.ModuleType),
#             name not in {"wantobjects"},
#         ]
#     )
# ]


import types
import re
import pyperclip
import datetime
import os
import sys
import requests
import json
import time
import calendar
import pyautogui

if sys.version_info.minor == 10:
    pass
else:
    # import win32gui
    pass


def randomAcknowledgement():
    return ""


def autoSend(friend_name="威威老师", messageList=str(datetime.datetime.today()).split()):
    """
    使用微信自动发送通知
    """
    #     import pyautogui
    #     import pyperclip
    #     import time
    #     import datetime
    # win + d 回到桌面
    pyautogui.hotkey("win", "d")
    # win + m 最小化
    # pyautogui.hotkey("win", "m")
    # 延迟等待1秒
    time.sleep(1)
    # shift + alt + s 打开微信
    pyautogui.hotkey("shift", "alt", "s")
    # 两个快捷键之间不需要延迟等待
    # 搜索好友
    pyautogui.hotkey("ctrl", "f")

    # 延迟等待0.2秒
    # time.sleep(0.2)
    # 复制好友昵称到粘贴板
    pyperclip.copy(friend_name)
    # 延迟等待0.2秒
    # time.sleep(0.2)
    # 模拟键盘 ctrl + v 粘贴
    pyautogui.hotkey("ctrl", "v")
    # 回车进入好友消息界面
    pyautogui.press(["enter", "enter"], interval=1)
    # 延迟等待0.2秒
    # time.sleep(1)
    # 发送消息
    # print(friend_name)
    # 复制前不能等待, 复制粘贴速度太快，所以需要添加一个前置字符串进行延迟等待
    messageList = ["_" * 4 + "我是分割线" + "_" * 4] * 2 + messageList
    for m in messageList:
        # 打印m
        # print(m)
        # 复制需要发送的内容到粘贴板, 复制前不能等待
        pyperclip.copy(m)
        # 延迟等待0.2秒
        # time.sleep(0.2)
        # 模拟键盘 ctrl + v 粘贴内容
        pyautogui.hotkey("ctrl", "v")
        # 发送消息
        # pyautogui.press("enter")
        pyautogui.hotkey("ctrl", "enter")
        # 延迟等待1秒
        # time.sleep(1)


def autoClassNotice(aCN_daysAfterToday=1, boardcast=True):
    """
    上课通知autoClassNotice
    python.exe -c "import diyPackage;diyPackage.autoClassNotice(diyPackage)"
    """

    def getTimeBuckets(s: str, classHours=1.5):
        # import re
        #     s = '1845'
        # 拆分s为 (18,45)
        s = re.findall(r"([\d]{2})", s)
        s = (int(i) for i in s)

        # 获取当前日期时间datetime对象
        now = datetime.datetime.now()
        # 生成当前日期date对象
        d = datetime.date(*(now.year, now.month, now.day))
        # 生成上课时间time对象
        start = datetime.time(*s)
        # 合并当前日期和上课时间为startDT 日期时间对象
        startDT = datetime.datetime.combine(d, start)
        # 根据1.5 hours 生成timedelta对象 课程总时间
        class_totalTime = datetime.timedelta(hours=classHours)
        # 上课结束时间 = 上课开始时间 + 课程总时间
        endDT = startDT + class_totalTime
        # 转换为str
        class_timeBuckets = f"{startDT.strftime('%H:%M')}-{endDT.strftime('%H:%M')}"
        #     18:45-20:15
        return class_timeBuckets

    def searchTeacher(path):
        """
        parameter: Teacher's class directoies path.
        return: Each teacher's path for dict.
        """
        # 添加默认老师的path
        # teacherDict = {"威威老师": path}
        teacherDict = {}
        # 提取其他老师文件夹名otherTeacher
        files = os.listdir(path)
        if boardcast:  # 如果boardcast为真，群发
            otherTR_dir = [re.match(r"^(.+老师)$", s) for s in files]
        else:
            otherTR_dir = [re.match(r"^(威威老师)$", s) for s in files]

        otherTeachers = [r[0] for r in otherTR_dir if r is not None]
        for t in otherTeachers:
            teacherDict[t] = path + t + "\\"

        return teacherDict

    def classNotice(tr, path, weather, acknowledgement):
        # 当前path下的所有文件和文件夹
        files = os.listdir(path)

        # 提取班级文件夹名stu_className
        if tr == "威威老师":
            class_directories = [
                re.match(r"[\w]+[\d]{1}[\u4500-\u9fff\d\w]+", s) for s in files
            ]
        elif tr == "深深老师":
            class_directories = [
                re.match(r"[\u4500-\u9fff]+[\d]{1}\-[\d]{4}", s) for s in files
            ]
        else:
            class_directories = [
                re.match(r"[\u4500-\u9fff]+.+[\u4500-\u9fff]+", s) for s in files
            ]
        stu_className = [r[0] for r in class_directories if r is not None]

        days = datetime.timedelta(days=aCN_daysAfterToday)
        today = datetime.timedelta(days=0)
        tomorrow = datetime.timedelta(days=1)
        if days == today:
            day_str = "今天"
        elif days == tomorrow:
            day_str = "明天"
        # print((str(datetime.date.today()+days)).split('-'))
        zh_weekdays = {
            0: "周一",
            1: "周二",
            2: "周六",
            3: "周四",
            4: "周五",
            5: "周六",
            6: "周日",
        }
        zhDigit_weekdays = {
            0: "周1",
            1: "周2",
            2: "周3",
            3: "周4",
            4: "周5",
            5: "周6",
            6: "周7",
        }
        n_weekday = calendar.weekday(
            *[int(s) for s in str(datetime.date.today() + days).split("-")]
        )
        if tr == "深深老师":
            zh_weekday = zhDigit_weekdays[n_weekday]
        else:
            zh_weekday = zh_weekdays[n_weekday]
        date = f"{datetime.date.today()+days:%m月%d日}"

        #     print(f"{stu_className=}")

        notices = []
        trClassList = []
        for s in stu_className:
            if bool(re.findall(zh_weekday, s)):
                if tr == "威威老师" or tr == "深深老师":
                    time = "".join(re.findall(r"([\d]{4})", s)[0])
                    time = time[:2] + ":" + time[2:]
                    t = int(time[:2])
                    if bool(re.findall(r"noip", s)):
                        timebucket = getTimeBuckets(time, classHours=3)
                    else:
                        timebucket = getTimeBuckets(time, classHours=1.5)
                    if t < 10:
                        phase = "早上"
                    elif t < 12:
                        phase = "上午"
                    elif t < 18:
                        phase = "下午"
                    else:
                        phase = "晚上"
                else:
                    time = "".join(re.findall(r"([\d]+.+[\d]+)", s)[0])
                    time = time[:2] + ":" + time[2:7] + ":" + time[7:]
                    t = int(time[:2])
                    if t < 10:
                        phase = "早上"
                    elif t < 12:
                        phase = "上午"
                    elif t < 18:
                        phase = "下午"
                    else:
                        phase = "晚上"

                stuCount = [
                    re.findall(r"[\S]+\.md", f) for f in os.listdir(path + "\\" + s)
                ]
                stuCount = [m[0] for m in stuCount if m]
                stuCount = len(stuCount)
                plural = "们" if stuCount > 1 else ""
                if tr == "威威老师":
                    text = f"""【上课通知🎈】
家长{plural}好，{day_str}{phase}{time}孩子{plural}有课，请提前10分钟来校区。
【注意事项❗】
请携带：护照、课本、水杯；
【天气预报{uni_icon}】
{weather}
【课题📖】code4-1-1 chapterName
【时间⏰】{date}{timebucket}
【教室🏫】斯坦星球花园城校区牛津大学
【教师💯】{tr}
请家长{plural}收到消息后回复一下。{acknowledgement}"""
                elif tr == "深深老师":
                    text = f"""【上课通知🎈】
家长{plural}好，{day_str}{phase}孩子{plural}有课，请提前10分钟来校区。
【注意事项❗】
请携带：护照、课本、水杯；
【天气预报{uni_icon}】
{weather}
【时间⏰】{date}{timebucket}
【教室🏫】斯坦星球花园城校区哈佛大学
【教师💯】{tr}
请家长{plural}收到消息后回复一下🌈"""
                else:
                    text = f"""【上课通知✨】
家长们好，{day_str}{phase}有课噢，请提前10分钟来校区。
【注意事项❗】
请携带：护照、课本、水杯
【天气预报{uni_icon}】：{weather}
【课题📖】：
【时间⏰】：{date}\n{time}
【教室🏫】：北京大学
【教师💯】：{tr}"""
                #             notices.append(f"{tr}\n{s}{text}\n")
                notices.append(f"{text}\n")
                trClassList.append(f"{tr}\n{s}")
        #             print(s)
        #         print(os.listdir(path+'\\'+s))
        #             print(text)

        return zip(trClassList, notices)

    def findAndSet(ForegroundWindowName="企业微信"):
        # 查找窗口句柄Window handle
        hwnd = win32gui.FindWindow(None, ForegroundWindowName)
        WindowTitle = ""
        if hwnd != 0:
            # 获取窗口标题
            WindowTitle = win32gui.GetWindowText(hwnd)
        while WindowTitle != "企业微信":
            # 查找窗口句柄Window handle
            hwnd = win32gui.FindWindow(None, ForegroundWindowName)
            WindowTitle = ""
            if hwnd != 0:
                # 获取窗口标题
                WindowTitle = win32gui.GetWindowText(hwnd)
        #     3280500 企业微信
        #     print(hwnd,WindowTitle)
        time.sleep(3)
        # 获取窗口句柄
        hwnd = win32gui.GetForegroundWindow()
        # 获取窗口标题
        WindowTitle = win32gui.GetWindowText(hwnd)
        if WindowTitle != "企业微信":
            # 发送按键给其他屏幕
            pyautogui.hotkey("alt")
            # 设置当前窗口
            win32gui.SetForegroundWindow(hwnd)
            return hwnd
        else:
            return True

    def weatherForecast(
        cityName="南山",
        apikey="e1f15c34780348edba48ae1c24dbda46",
        daysAfterToday=1,
    ):
        """
        import requests
        import json
        import time
        GeoAPI请求URL:
        https://geoapi.qweather.com/v2/city/lookup?location=南山&adm=深圳&key=这里替换成你的key
        免费订阅请求URL:
        https://devapi.qweather.com/v7/weather/7d?location=101280604&key=这里替换成你的key
        空气质量每日预报:
        https://devapi.qweather.com/v7/air/5d?location=101280604&key=这里替换成你的key
        """

        def city_lookup(cityName, apikey, administrator=""):
            """
            requests.get(url, params=params)是使用HTTP GET方法向指定的url发送请求，
            并将参数params作为查询字符串附加到url中。这是一种常见的向API发送请求的方法。
            你也可以使用&连接参数，但是这样的话，你需要自己构建查询字符串，这可能会比较麻烦。
            使用params参数可以让requests库自动构建查询字符串，这样更加方便。

            response.json()和json.loads(response.text)的效果是一样的，
            都是将API返回的json格式的字符串转换为python对象。
            response.json()是requests库提供的一个方法，可以直接将API返回的json格式的字符串
            转换为python对象。
            json.loads(response.text)是使用python内置的json库将json格式的字符串转换为python对象。
            """
            url = "https://geoapi.qweather.com/v2/city/lookup"
            parameters = {
                "location": cityName,
                "adm": administrator,
                "key": apikey,
            }
            header = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
            }
            response = requests.get(url, headers=header, params=parameters)
            #     print(response.text)
            data = json.loads(response.text)  # json.loads() 将json格式的字符串转换为python对象

            cityID = data["location"][0]["id"]  #  "id":"101280604",
            cityAdm = data["location"][0]["adm2"]  #  "adm2":"深圳",
            # 该地区的天气预报网页链接，便于嵌入你的网站或应用
            # https://www.qweather.com/weather/nanshan-101280604.html
            fxLink = data["location"][0]["fxLink"]
            return cityID, cityAdm, fxLink

        def getQweatherTextEmoji(iconCodeDay):
            # tr是HTML表格中的行，全称是Table Row
            # td是HTML表格中的单元格，全称是Table Data
            # th是HTML表格中的表头单元格，全称是Table Header
            """
            当我们使用Python访问网页时，我们需要使用requests库来发送HTTP请求并获取响应。
            在这个代码中，url是我们要访问的网址。
            我们使用requests.get(url)方法来发送GET请求并获取响应。
            响应是一个包含服务器响应的对象，我们可以使用response.content属性来获取响应的内容。
            响应的内容通常是HTML或JSON格式的数据。在这个代码中，我们使用BeautifulSoup库来解析HTML并获取数据。
            soup是一个包含HTML文档的对象，我们可以使用soup.find_all方法来查找HTML元素。
            """
            import requests
            from bs4 import BeautifulSoup

            url = "https://dev.qweather.com/docs/resource/icons/"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            # <tr>
            # <th>图标代码</th>  tds[0]
            # <th>天气</th>      tds[1]
            # <th>白天</th>      tds[2]
            # <th>夜晚</th>      tds[3]
            # </tr>
            # print(soup.find_all('tr')[1:-9])
            textEmoji = {}
            emoji = {
                "100": "☀️",
                "101": "🌥️",
                "102": "🌤️",
                "103": "🌤️☀️",
                "104": "☁️",
                "300": "🌦️",
                "301": "🌧️",
                "302": "⛈️",
                "303": "🌩️",
                "304": "🌩️❄️",
                "305": "🌧️",
                "306": "🌧️",
                "307": "🌧️☔",
                "308": "🌧️☔",
                "309": "🌧️",
                "310": "🌧️☔",
                "311": "🌧️☔",
                "312": "🌧️☔",
                "313": "🌧️❄️",
                "314": "🌧️",
                "315": "🌧️",
                "316": "🌧️☔",
                "317": "🌧️☔",
                "318": "🌧️☔",
                "399": "🌧️",
                "400": "❄️",
                "401": "❄️",
                "402": "❄️",
                "403": "❄️",
                "404": "🌨️",
                "405": "🌨️🌧️",
                "406": "🌨️🌧️",
                "407": "❄️",
                "408": "❄️",
                "409": "❄️",
                "410": "❄️",
                "499": "❄️",
                "500": "🌫️",
                "501": "🌫️",
                "502": "🌫️",
                "503": "🌪️",
                "504": "🌪️",
                "507": "🌪️",
                "508": "🌪️",
                "509": "🌫️",
                "510": "🌫️",
                "511": "🌫️",
                "512": "🌫️",
                "513": "🌫️",
                "514": "🌫️",
                "515": "🌫️",
                "900": "🔥",
                "901": "❄️",
                "999": "❓",
            }
            for item in soup.find_all("tr")[1:-9]:
                tds = item.find_all("td")
                if tds[2].text == "✅":  # 只需要白天的图标
                    #         print(tds)
                    textEmoji[tds[0].text] = (
                        tds[1].text,
                        emoji.get(tds[0].text, "default❓"),
                    )
            #     print(len(emoji),len(textEmoji))
            return textEmoji.get(iconCodeDay, "default❓")

        def airDailyForecast(cityID, apikey, daysAfterToday):
            if daysAfterToday > 4:  # 空气质量预报5天(0,1,2,3,4) ，天气预报7天
                daysAfterToday = 4
            url = "https://devapi.qweather.com/v7/air/5d"
            parameters = {
                "location": cityID,
                "key": apikey,
            }
            response = requests.get(url, params=parameters)
            #     print(response.text)
            data = json.loads(response.text)  # json.loads() 将json格式的字符串转换为python对象
            weather = data["daily"][daysAfterToday]  # dict
            airQuality = weather["aqi"]  # "aqi": "46",
            airQualityLevel = weather["category"]  # "category": "优",

            return airQuality, airQualityLevel

        def weather_now(cityID, apikey, fxLink):
            import requests
            from bs4 import BeautifulSoup

            url = fxLink
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            current_abstract = soup.find_all("div", class_="current-abstract")[
                0
            ].text.strip()
            return current_abstract

        if daysAfterToday > 6:  # 天气预报7天(0,1,2,3,4,5,6)
            daysAfterToday = 6
        # 深圳南山明天
        cityID, cityAdm, fxLink = city_lookup(cityName, apikey)
        # 当前实时天气摘要
        current_abstract = weather_now(cityID, apikey, fxLink)
        # 天气预报：多云
        url = "https://devapi.qweather.com/v7/weather/7d"
        params = {
            "key": apikey,
            "location": cityID,
        }
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        #     print(response.text)

        weather = data["daily"][daysAfterToday]  # dict
        weatherTextEmoji = getQweatherTextEmoji(weather["iconDay"])  # "iconDay": "100",

        # daily.fxDate 预报日期
        daysAfterTodayList = [
            "今天",
            "明天",
            "后天",
        ]
        if daysAfterToday < 3:
            fxDate = daysAfterTodayList[daysAfterToday]
        else:
            fxDate = str(weather["fxDate"][-2:]) + "日"

        weatherForecast_textDay = weather["textDay"]
        tempMax = weather["tempMax"]
        tempMin = weather["tempMin"]
        windDir = weather["windDirDay"]
        windScale = weather["windScaleDay"]

        # 空气质量每日预报
        airQuality, airQualityLevel = airDailyForecast(cityID, apikey, daysAfterToday)
        # 天气文字加图标weatherTextEmoji,('大雨', '🌧️☔')
        # 深圳南山明天多云，阴晴之间，谨防紫外线侵扰，20℃到26℃，东南风3级，空气质量46优
        formatString = f"{cityAdm}{cityName}{fxDate}{weatherTextEmoji[0]}，{tempMax}℃到{tempMin}℃，{windDir}{windScale}级，空气质量{airQuality}{airQualityLevel}"
        return weatherTextEmoji[1], formatString, current_abstract

    # import os
    # import re
    # import datetime
    # import calendar

    # 获取%stuEvaluationsPath%
    path = os.environ["stuEvaluationsPath"] + "\\"
    uni_icon, weather, current_abstract = weatherForecast(
        cityName="南山",
        apikey="e1f15c34780348edba48ae1c24dbda46",
        daysAfterToday=1,
    )

    # 致谢语
    acknowledgement = randomAcknowledgement()

    # 打开企业微信
    os.startfile(r"C:\Program Files (x86)\WXWork\WXWork.exe")
    # 等待或者判断
    if sys.version_info.minor == 10:
        # 等待30秒
        time.sleep(1)
    else:
        (findAndSet(ForegroundWindowName="企业微信"))

    text = ""
    for TR, TRpath in searchTeacher(path).items():
        # 威威老师 P:\MyNutstore\stemStar\stuEvaluations\威威老师\
        # print(TR, TRpath)
        # [('威威老师\nnoip1周六上午9点整', '\n【上课通知✨】\n')]
        # print(list(classNotice(TR, TRpath, weather)))

        noticeList = []
        for n in classNotice(TR, TRpath, weather, acknowledgement):
            noticeList.append(n[1])
            text += n[0] + "\n" + n[1]

        autoSend(friend_name=TR, messageList=noticeList)
    # 复制上课通知
    # pyperclip.copy(text)
    return text


if __name__ == "__main__":
    msg = autoClassNotice(boardcast=False)

