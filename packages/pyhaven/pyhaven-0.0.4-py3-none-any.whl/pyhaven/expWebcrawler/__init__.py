# coding: utf-8
r"""
网络爬虫Webcrawler
        weatherForecast - 天气预报
        searchPoetry - 搜索诗词
        todayPoetry - 获取今日诗词
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
import datetime
import time
import re
import pyperclip
import requests
import json
import os
import sys
from bs4 import BeautifulSoup


def priceCalculate():
    """
    获取命令行参数或用户输入的.md文件路径,解析该.md文件中的价格信息,计算总价格,并将总价格复制到剪贴板。
    print: 打印
    """
    # import sys  # 导入系统模块
    # import os  # 导入OS模块
    # import re
    # import pyperclip
    # from sqlalchemy import false

    def getCMDargv():  # 获取命令行参数

        cmd_argv = sys.argv  # 获取命令行参数                    #存储命令行参数
        py_executable = sys.executable  # 存储Python解释器路径

        if sys.stdin.isatty():  # 判断是否在终端运行
            # 如果在终端运行
            if len(cmd_argv) > 1:  # 如果命令行参数大于1个
                path = cmd_argv[1]  # 取第一个命令行参数作为.md文件路径
        else:
            # 如果在.py文件或Notebook中运行
            # print('Running in .py file or Notebook')
            path = None
        return path  # 返回.md文件路径

    def diyPC(markdownPath):  # 解析.md文件中的价格信息并计算总价格
        try:  # 尝试打开.md文件并解析
            isExists = os.path.exists(markdownPath)  # 判断文件路径是否存在
            isFile = os.path.isfile(markdownPath)  # 判断文件路径是否为文件
        except Exception as e:  # 捕获所有异常，并且把错误信息给e
            # print(e)
            while True:
                markdownPath = input(
                    "Please input Markdown file path.\n"
                )  # 提示输入文件路径
                isExists = os.path.exists(markdownPath)  # 判断文件路径是否存在
                isFile = os.path.isfile(markdownPath)  # 判断文件路径是否为文件

                if isExists and isFile:  # 如果路径存在并且是文件
                    break

        with open(markdownPath, "r", encoding="utf-8") as f:  # 打开.md文件
            mdrows = f.readlines()  # 读取.md文件所有行

        prices = []  # 初始化价格列表
        for row in mdrows:  # 遍历.md文件每行
            exculde = re.findall(r"\u603b\u4ef7", row)  # 查找每行是否包含"总价"
            result = re.findall(r"(?<=\¥)[\d]+", row)  # 查找每行价格信息
            # print(exculde,result)
            if bool(exculde) == True and exculde[0] == "\u603b\u4ef7":
                continue  # 如果包含"总价",跳过当前行

            if bool(result) == False:
                continue  # 如果当前行不包含价格,跳过当前行
            prices.append(result)  # 将当前行价格添加到 prices 列表

        # print(prices)
        totalPrice = sum(
            [int(p[0], 10) for p in prices]
        )  # 汇总prices列表中的所有价格,计算总价格

        return totalPrice  # 返回总价格

    # path = r"P:\MyNutstore\StarryNight299792458\装备\个人计算机\0_整机\配置单\4_Intel Core i7-12700K\Intel Core i7-12700K(市场价).md"
    path = getCMDargv()  # 获取.md文件路径
    totalPrice = diyPC(path)  # 调用diyPC函数解析.md文件并计算总价格
    pyperclip.copy(totalPrice)  # 将总价格复制到剪贴板
    print(totalPrice)  # 打印总价格


# priceCalculate()


def generate_markdown_link(text, anchorTextPattern=""):
    """Markdown超链接生成(自动根据url生成Markdown格式的超链接,包含文字和链接)
    :param text: 输入的文本,一定要包含url
    :return : Markdown格式的超链接
    """
    # import re  # 导入正则表达式库
    # import requests  # 导入HTTP请求库
    # from bs4 import BeautifulSoup  # 导入BeautifulSoup4库
    # text = '''PassMark Software - PC Benchmark and Test Software
    # https://www.passmark.com/'''
    # text = 'https://www.passmark.com/'
    text = re.sub(r"\r", "", text)  # windows的换行符是\r\n ，提前删除\r
    resultMatch = re.search(
        r"(https?)://[\w\-]+(\.[\w\-]+)+(/[\w\- ./?%&=]*)?", text
    )  # 使用正则表达式搜索文本中的URL
    anchorText = [t for t in text.split("\n") if t]  # 把文本按行分割，并且去除空字符串
    try:  # 尝试提取URL和链接文本
        url = resultMatch.group()  # 提取URL
        if len(anchorText) > 1:  # 判断链接文本是否为多行
            anchorText = anchorText[0]  # 取第一行作为链接文本
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
                # 定义请求头部
            }
            response = requests.get(url, headers=headers)  # 发出HTTP请求
            soup = BeautifulSoup(response.text, "lxml")  # 解析请求的HTML内容
            anchorText = soup.head.title.text  # 提取标题作为链接文本

        if anchorTextPattern:
            # 匹配指定文本
            anchorTextList = re.findall(anchorTextPattern, anchorText)
            if len(anchorTextList) > 1:
                # print(anchorTextList)
                # ['【微星MAG B550M MORTAR MAX WIFI', '【行情 报价 价格 评测']
                # 第一个匹配到的文本作为标题
                anchorText = anchorTextList[0][1:]

        markdownHref = f"[{anchorText}]({url} )"  # 生成Markdown格式超链接
    except AttributeError as err:
        markdownHref = ""
        print("没有找到URL")  # 打印提示信息
    return markdownHref  # 返回Markdown格式超链接
    """
    re: 正则表达式
    requests: 发出HTTP请求
    bs4:BeautifulSoup4 网页解析
    """


# text = 'https://www.passmark.com/'
# print(generate_markdown_link(text))


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
        data = json.loads(
            response.text
        )  # json.loads() 将json格式的字符串转换为python对象

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
        data = json.loads(
            response.text
        )  # json.loads() 将json格式的字符串转换为python对象
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


def searchPoetry(cacheTime_Minutes=0.1):
    """
    搜索古诗文网络资料并解析内容
    print: 打印
    requests: 网络请求库
    bs4:BeautifulSoup4 解析库
    os: 操作系统接口
    re: 正则表达式库
    json: 用于python对象与JSON格式数据的转换
    time:时间处理库
    """
    # import requests
    # from bs4 import BeautifulSoup
    # import os
    # import re
    # import json
    # import time

    # 发送网络请求搜索古诗文

    # 伪装请求头
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    }
    url = "https://so.gushiwen.cn/shiwenv_630c04c81858.aspx"
    # 搜索关键词
    keyword = "观沧海"
    # 输入搜索关键词
    keyword = input("请输入搜索关键词:")

    # 拼接搜索URL
    searchURL = (
        f"https://so.gushiwen.cn/search.aspx?value={keyword}&valuej={keyword[0]}"
    )
    # 提取URL前缀
    prefixURL = re.match(r"(http|https)://+[a-zA-Z\.\-0-9]+", url)[0]

    # 缓存函数
    def cacheFile(url, filename, cacheTime_Minutes):
        # 如果存在缓存文件则判断是否更新,否则直接写入新内容
        if os.path.isfile(filename):  # 如果 存在缓存文件
            nowTime = time.time()
            modifyTime = os.path.getmtime(filename)
            if nowTime - modifyTime > int(cacheTime_Minutes * 60):
                # 如果缓存文件超过1分钟未更新，则强制更新
                # print(time.localtime(modifyTime))
                with open(filename, "wb") as f:
                    response = requests.get(url, headers=headers)
                    #             print(f"{type(response.text)=}")  # <class 'str'>
                    #             print(f"{type(response.content)=}") # <class 'bytes'>
                    f.write(response.content)
            else:  # 缓存文件更新于3分钟之内；则读取
                with open(filename, "rb") as f:
                    response = f.read()
        else:  # 否则不存在缓存文件，则写入
            with open(filename, "wb") as f:
                response = requests.get(url, headers=headers)
                #             print(f"{type(response.text)=}")  # <class 'str'>
                #             print(f"{type(response.content)=}") # <class 'bytes'>
                f.write(response.content)
        if isinstance(response, bytes):
            responseContent = response.decode("utf-8")
            htmldata = BeautifulSoup(responseContent, "lxml")
        else:
            htmldata = BeautifulSoup(response.text, "lxml")
        return htmldata

    # 创建缓存文件夹poetryCache
    # print(os.getcwd())
    os.makedirs(os.path.join(os.getcwd(), "poetryCache"), exist_ok=True)
    # 调用缓存文件函数
    htmldata = cacheFile(
        searchURL,
        os.path.join(
            os.getcwd(),
            "poetryCache",
            "gushiwen.html",
        ),
        cacheTime_Minutes=cacheTime_Minutes,
    )
    #     print(htmldata)
    # print(help(htmldata.find))
    # print(help(htmldata.findAll))
    # print(len(htmldata.findAll('div', class_="cont")))
    poetryDict = dict()

    # 存储搜索关键词
    poetryDict["keyword"] = keyword

    # 存储搜索结果
    poetryDict["poems"] = []

    # 遍历每首诗词信息
    for poetry in htmldata.findAll("div", class_="cont"):
        poetryMultiTag_p = poetry.findAll("p")
        length = len(poetryMultiTag_p)
        #         print('-------')
        #         print(f"{length=}")
        if poetryMultiTag_p and length > 1:

            #             print(f"{poetryMultiTag_p=}")

            verseDict = dict()
            # 提取诗词标题
            verseDict["poetryTitle"] = "".join(poetryMultiTag_p[0].text.split())
            # 提取诗词详情页链接
            verseDict["poetry_href"] = prefixURL + poetryMultiTag_p[0].a.get("href")
            NDIndex = 1
            for i in range(length):
                #                 print(f"poetryMultiTag_p[{i}]:{poetryMultiTag_p[i]}")
                ahrefValue = poetryMultiTag_p[i].a.get("href")
                #                 print(f"-----{ahrefValue=}-----")
                if isinstance(ahrefValue, list):
                    ahrefValue = ahrefValue[0]
                #                 -----None-----
                #                 -----['source']-----
                if ahrefValue and re.search(r"authorv", ahrefValue):
                    NDIndex = i
                    break
            # 提取名字和朝代
            NameAndDynasty = poetryMultiTag_p[NDIndex].text.split()[0]
            #             print(NameAndDynasty)
            pattern = r"(\[|〔).*(〕|\])"
            reResult = re.search(pattern, NameAndDynasty)
            # 提取诗人姓名
            verseDict["authorName"] = reResult.group()
            # 提取诗人朝代
            verseDict["authorDynasty"] = NameAndDynasty[: reResult.start()]

            # 存储每首诗词信息
            poetryDict["poems"].append(verseDict)
    # python对象转换为json文本
    JavaScriptObjectNotation = json.dumps(poetryDict)
    # print(JavaScriptObjectNotation)
    # print(poetryDict)

    # 遍历输出搜索结果
    poems = poetryDict["poems"]
    for i in range(len(poems)):
        print(
            f"""{i+1}. {poems[i]['poetryTitle']} --- {poems[i]['authorName']+poems[i]['authorDynasty']}"""
        )

    try:
        select = int(input("请输入编号选择诗词:"))
    except ValueError:
        select = 1
    select -= 1

    # 提取选择的诗词详情页链接
    url = poems[select]["poetry_href"]

    # 解析详情页内容
    htmldata = cacheFile(
        url,
        os.path.join(
            os.getcwd(), "poetryCache", f"{poems[select]['poetryTitle']}.html"
        ),
        cacheTime_Minutes=cacheTime_Minutes,
    )

    # 存储详情页内容
    verseContentDict = dict()

    # 提取标题
    verseContentDict["Title"] = poems[select]["poetryTitle"]

    # 提取诗人姓名
    verseContentDict["Author"] = poems[select]["authorName"]

    # 提取诗人朝代
    verseContentDict["Dynasty"] = poems[select]["authorDynasty"]
    verseNumber = re.findall(r"(?<=_)[^\.]+", poems[select]["poetry_href"])[0]
    verseId = f"""contson{verseNumber}"""
    try:
        # 提取诗词内容
        verseContent = str((htmldata.findAll("div", class_="contson", id=verseId)[0]).p)
        if verseContent:
            raise IndexError

        # 去除<p> </p>
        verseContent = re.sub(r"(\<p\>|\<\/p\>)", "", verseContent)

    # 异常处理
    except IndexError:
        verseContent = str((htmldata.findAll("div", class_="contson", id=verseId)[0]))
        verseContent = re.sub(
            r"(\<div.*\>|\<\/div\>)", "", verseContent
        )  # 去除<div> </div>

    verseContent = re.sub(r"\s", "", verseContent)  # 去除空白字符
    verseContent = re.sub(r"(\<p\>)", "", verseContent)  # 去除<p>
    verseContent = re.sub(r"\<br\/\>", "\n", verseContent)  # 替换<br/>为换行
    verseContent = re.sub(r"\<\/p\>", "\n", verseContent)  # 替换</p>为换行

    # 存储诗词内容
    verseContentDict["Content"] = verseContent
    return "\n" + "\n".join(verseContentDict.values())


def todayPoetry():
    """
    今日诗词
    """
    # import json, requests
    # from bs4 import BeautifulSoup

    url = "https://www.1saying.com/"
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    today_poetry_container = soup.find_all("div", class_="today-poetry-container")
    # print(today_poetry_container,type(today_poetry_container))
    today_poetry = str(today_poetry_container[0].text)
    return "\n".join(today_poetry.split())


# 📜 定义模块的公开接口
__all__ = [
    # 🔍 遍历全局变量字典
    name
    for name, obj in globals().items()
    # ✅ 只选择不以下划线开头的变量
    if not name.startswith("_")
    # ✅ 排除类型为模块的对象
    and not isinstance(obj, types.ModuleType)
    # ✅ 排除在集合里的变量
    and name not in {"wantobjects", "types"}
]


if __name__ == "__main__":
    print(todayPoetry())
    print(searchPoetry(cacheTime_Minutes=60))
    for i in range(3):
        print(
            weatherForecast(
                cityName="南山",
                apikey="e1f15c34780348edba48ae1c24dbda46",
                daysAfterToday=i,
            )
        )
        time.sleep(1)
