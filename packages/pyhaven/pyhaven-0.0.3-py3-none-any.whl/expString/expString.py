#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pyhaven import *
import base64
import pyhaven
import re
import pyperclip
import types
import unicodedata
import pypinyin
s = "为什么所有APP都解决不了这个小问题？效率工具无法掌控真实生活。"
pinyin_str = pypinyin.pinyin(s, style=pypinyin.TONE)
print(pinyin_str)
'''
输出：[['wèi'], ['shén'], ['me'], ['suǒ'], ['yǒu'], ['APP'], ['dōu'], ['jiě'], ['jué'], ['bù'], ['liǎo'], ['zhè'], ['gè'], ['xiǎo'], ['wèn'], ['tí'], ['？'], ['xiào'], ['lǜ'], ['gōng'], ['jù'], ['wú'], ['fǎ'], ['zhǎng'], ['kòng'], ['zhēn'], ['shí'], ['shēng'], ['huó'], ['。']]
'''


# In[27]:


line = '单（chán匈奴族首领）于只(abc)会骑马'
pinyin_str = [['dān'], ['（chán'], ['xiōng'], ['nú'], ['zú'], ['shǒu'], [
    'lǐng'], ['）'], ['yú'], ['zhǐ'], ['(abc)'], ['huì'], ['qí'], ['mǎ']]

pypinyin模块会将line中的标点符号识别为英语单词，所以在使用pypinyin.pinyin之后，
使用正则分割pinyin_str中的标点符号和英语单词，
比如pinyin_str = [['dān'], ['（chán'], ['xiōng'], ['nú'], ['zú'], ['shǒu'], ['lǐng'], ['）'], ['yú'], ['zhǐ'], ['(abc)'], ['huì'], ['qí'], ['mǎ']]分割为
pinyin_str = [['dān'], ['（'], ['chán'], ['xiōng'], ['nú'], ['zú'], ['shǒu'], [
    'lǐng'], ['）'], ['yú'], ['zhǐ'], ['('], ['abc'], [')'], ['huì'], ['qí'], ['mǎ']]


# In[ ]:


在这一行代码之前，处理line中的含有声调的字母，去除声调，比如"á"变为"a"，注意标点符号保持原样。


# In[55]:

line = '单（chán匈奴族首领）于只(abc)会骑马'
# line = "".join(
#     c
#     for c in unicodedata.normalize("NFKD", line)
#     if not unicodedata.combining(c)
# )

pinyin_str = pypinyin.pinyin(line, style=pypinyin.TONE)
print(f"{pinyin_str=}")


# In[2]:


def text2pinyin(Text, splitPattern=True, paragraphWidth=10):
    """
    获取文本的拼音列表，保证汉字与拼音对齐，根据拼音字母数量调整间隔
    """

    def split_pinyin_list(pinyin_list):
        result = []

        for item in pinyin_list:
            current = item[0]  # 获取当前拼音项

            # 检查是否包含括号和拼音/英文的组合
            if re.search(r"[（\(].+|.+[\)）]", current):
                # 分离括号
                parts = re.findall(
                    r"([（\(])|([a-záéíóúüāēīōūǖáéíóúǎěǐǒǔǚàèìòùǜ]+)|([a-zA-Z]+)|([\)）])",
                    current,
                )

                for part in parts:
                    # 找到非空的部分
                    matched = next((x for x in part if x), "")
                    if matched:  # 只添加非空匹配
                        result.append([matched])
            else:
                # 如果不包含括号组合，直接添加原始项
                result.append([current])

        return result

    def remove_tone_marks(text):
        """去除拼音中的声调，保留标点符号"""
        # 使用正则表达式分离拼音和标点
        parts = re.findall(
            r"([a-záéíóúüāēīōūǖáéíóúǎěǐǒǔǚàèìòùǜ]+)|([^a-záéíóúüāēīōūǖáéíóúǎěǐǒǔǚàèìòùǜ])",
            text,
        )
        result = ""
        for pinyin, punct in parts:
            if pinyin:
                # 对拼音部分进行去声调处理
                normalized = unicodedata.normalize("NFKD", pinyin)
                # 只保留基本字母
                normalized = "".join(
                    c for c in normalized if not unicodedata.combining(c)
                )
                result += normalized
            if punct:
                # 标点符号保持不变
                result += punct
        return result

    Text = Text.strip()
    Text = re.sub(r"\n+", "\n", Text)
    allList = []

    for line in Text.split("\n"):
        if not line.strip():
            allList.append("\n")
            continue
        # 去除声调
        line = remove_tone_marks(line)
        tokens = re.findall(
            r"[\u4e00-\u9fff]|[a-zA-Z]+|[^\u4e00-\u9fffa-zA-Z]", line)
        pinyin_str = pypinyin.pinyin(line, style=pypinyin.TONE)
        pinyin_str = split_pinyin_list(pinyin_str)
        current_pinyin_idx = 0
        pinyins = []
        chars = []
        is_punctuation = []
        is_chinese_punct = []

        for token in tokens:
            if re.match(r"[\u4e00-\u9fff]", token):
                pinyins.append(pinyin_str[current_pinyin_idx][0])
                chars.append(token)
                is_punctuation.append(False)
                is_chinese_punct.append(False)
                current_pinyin_idx += 1
            elif token.isalpha():
                pinyins.append(" " * len(token))
                chars.append(token)
                is_punctuation.append(False)
                is_chinese_punct.append(False)
                current_pinyin_idx += 1
            else:
                pinyins.append("")
                chars.append(token)
                is_punctuation.append(True)
                is_chinese = ord(token) > 255
                is_chinese_punct.append(is_chinese)
                current_pinyin_idx += 1

        if pinyins:
            pinyin_line = ""
            for i, (py, is_punct, is_cn_punct) in enumerate(
                zip(pinyins, is_punctuation, is_chinese_punct)
            ):
                if not is_punct:
                    if py.strip():
                        pinyin_line += py
                    else:
                        pinyin_line += " " * len(chars[i])
                    if i < len(pinyins) - 1:
                        # 根据拼音长度决定间隔
                        spaces = 2 if len(py.strip()) == 1 else 1
                        pinyin_line += " " * spaces
                else:
                    pinyin_line += " " * (2 if is_cn_punct else 1)
                    if i < len(pinyins) - 1:
                        pinyin_line += " " * 2

            allList.append(pinyin_line + "\n")

            char_line = ""
            for i, (char, is_punct) in enumerate(zip(chars, is_punctuation)):
                if is_punct:
                    char_line += char + "  "
                else:
                    if i < len(chars) - 1:
                        if pinyins[i].strip():
                            # 根据拼音长度决定间隔
                            spaces = 2 if len(pinyins[i].strip()) == 1 else 1
                            char_line += char + " " * \
                                (len(pinyins[i]) + spaces - 2)
                        else:
                            # 字母不需要根据拼音长度决定间隔，直接指定一个空格
                            char_line += char + " "
                    else:
                        char_line += char

            allList.append(char_line.rstrip() + "\n\n")
        else:
            allList.append(line + "\n\n")

    return "".join(allList)


# 测试文本
s = '''中国加油'''
s = '''
磁额铁额B额一直后退直到不碰到磁铁A
磁额铁额ABC额一直后退直到不碰到磁铁A
我额是你
蛾儿雪柳黄金缕
单（chán匈奴族首领）于只会骑马
'''
s = '''
青玉案 元夕
朝代:宋
作者:辛弃疾
体裁:词

东风夜放花千树，
更吹落，星如雨。
宝马雕车香满路。
凤箫声动，玉壶光转，
一夜鱼龙舞。

蛾儿雪柳黄金缕，
笑语盈盈暗香去。
众里寻他千百度，
蓦然回首，那人却在，
灯火阑珊处。
'''

result = text2pinyin(s)
print(result)


# In[ ]:


# In[ ]:


# In[14]:


# text = 'https://www.passmark.com/'
text = pyperclip.paste()
# text = """【微星MAG B550M MORTAR MAX WIFI】微星(MSI)MAG B550M MORTAR MAX WIFI迫击炮电脑主板 支持CPU5600X5800X5600G （AMD B550Socket AM4)【行情 报价 价格 评测】-京东
# https://item.jd.com/100034383960.html"""
markdownHref = (pyhaven.expWebcrawler.generate_markdown_link(
    text, anchorTextPattern=r'\【[^\】]*'))
print(markdownHref)
pyperclip.copy(markdownHref)


# In[1]:


def generate_markdown_link(text):
    '''Markdown超链接生成(自动根据url生成Markdown格式的超链接,包含文字和链接)
    :param text: 输入的文本,一定要包含url
    :return : Markdown格式的超链接
    '''
    import re  # 导入正则表达式库
    import requests  # 导入HTTP请求库
    from bs4 import BeautifulSoup  # 导入BeautifulSoup4库
    # text = '''PassMark Software - PC Benchmark and Test Software
    # https://www.passmark.com/'''
    # text = 'https://www.passmark.com/'
    text = re.sub(r'\r', '', text)  # windows的换行符是\r\n ，提前删除\r
    resultMatch = re.search(
        r'(https?)://[\w\-]+(\.[\w\-]+)+(/[\w\- ./?%&=]*)?', text)  # 使用正则表达式搜索文本中的URL
    anchorText = [t for t in text.split('\n') if t]  # 把文本按行分割，并且去除空字符串
    print(anchorText)
    try:  # 尝试提取URL和链接文本
        url = (resultMatch.group())  # 提取URL
        if len(anchorText) > 1:  # 判断链接文本是否为多行
            anchorText = anchorText[0]  # 取第一行作为链接文本
        else:
            headers = {
                # 定义请求头部
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
            }
            response = requests.get(url, headers=headers)  # 发出HTTP请求
            soup = BeautifulSoup(response.text, 'lxml')  # 解析请求的HTML内容
            anchorText = soup.head.title.text  # 提取标题作为链接文本
        markdownHref = f"[{anchorText}]({url})"  # 生成Markdown格式超链接
    except AttributeError as err:
        markdownHref = ''
        print('没有找到URL')  # 打印提示信息

    return markdownHref  # 返回Markdown格式超链接
    '''
    re: 正则表达式
    requests: 发出HTTP请求
    bs4:BeautifulSoup4 网页解析
    '''


text = """
DaVinci Resolve 18  Blackmagic Design 
https://www.blackmagicdesign.com/products/davinciresolve
"""
text = pyperclip.paste()
print(generate_markdown_link(text))


# In[4]:


# 编码:使用base64.b64encode()方法,传入要编码的字节串,返回编码后的字符串.


encoded = base64.b64encode(b"Hello")
print(encoded)
# b'SGVsbG8='


# In[9]:


# 解码:使用base64.b64decode()方法,传入要解码的字符串,返回解码后的原始字节串.
s = b'''bWFnbmV0Oj94dD11cm46YnRpaDoxMTcwMTJmM2VjN2ZhNjA3M2E0MzgwMWFlZmM4YzkxZjlmYWFiNGY2JmRuPUtleXMlMjAxNi4wLjIucmFyJnRyPXVkcCUzYSUyZiUyZnB1YmxpYy5wb3Bjb3JuLXRyYWNrZXIub3JnJTNhNjk2OSUyZmFubm91bmNlJnRyPWh0dHAlM2ElMmYlMmYxMDQuMjguMS4zMCUzYTgwODAlMmZhbm5vdW5jZSZ0cj1odHRwJTNhJTJmJTJmMTA0LjI4LjE2LjY5JTJmYW5ub3VuY2UmdHI9dWRwJTNhJTJmJTJmMTA3LjE1MC4xNC4xMTAlM2E2OTY5JTJmYW5ub3VuY2UmdHI9dWRwJTNhJTJmJTJmMTA5LjEyMS4xMzQuMTIxJTNhMTMzNyUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjExNC41NS4xMTMuNjAlM2E2OTY5JTJmYW5ub3VuY2UmdHI9aHR0cCUzYSUyZiUyZjEyNS4yMjcuMzUuMTk2JTNhNjk2OSUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjEyOC4xOTkuNzAuNjYlM2E1OTQ0JTJmYW5ub3VuY2UmdHI9aHR0cCUzYSUyZiUyZjE1Ny43LjIwMi42NCUzYTgwODAlMmZhbm5vdW5jZSZ0cj1odHRwJTNhJTJmJTJmMTU4LjY5LjE0Ni4yMTIlM2E3Nzc3JTJmYW5ub3VuY2UmdHI9aHR0cCUzYSUyZiUyZjE3My4yNTQuMjA0LjcxJTNhMTA5NiUyZmFubm91bmNlJnRyPWh0dHAlM2ElMmYlMmYxNzguMTc1LjE0My4yNyUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjE3OC4zMy43My4yNiUzYTI3MTAlMmZhbm5vdW5jZSZ0cj11ZHAlM2ElMmYlMmYxODIuMTc2LjEzOS4xMjklM2E2OTY5JTJmYW5ub3VuY2UmdHI9dWRwJTNhJTJmJTJmMTg1LjUuOTcuMTM5JTNhODA4OSUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjE4OC4xNjUuMjUzLjEwOSUzYTEzMzclMmZhbm5vdW5jZSZ0cj11ZHAlM2ElMmYlMmYxOTQuMTA2LjIxNi4yMjIlM2E4MCUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjE5NS4xMjMuMjA5LjM3JTNhMTMzNyUyZmFubm91bmNlJnRyPWh0dHAlM2ElMmYlMmYyMTAuMjQ0LjcxLjI1JTNhNjk2OSUyZmFubm91bmNlJnRyPWh0dHAlM2ElMmYlMmYyMTAuMjQ0LjcxLjI2JTNhNjk2OSUyZmFubm91bmNlJnRyPWh0dHAlM2ElMmYlMmYyMTMuMTU5LjIxNS4xOTglM2E2OTcwJTJmYW5ub3VuY2UmdHI9dWRwJTNhJTJmJTJmMjEzLjE2My42Ny41NiUzYTEzMzclMmZhbm5vdW5jZSZ0cj1odHRwJTNhJTJmJTJmMzcuMTkuNS4xMzklM2E2OTY5JTJmYW5ub3VuY2UmdHI9dWRwJTNhJTJmJTJmMzcuMTkuNS4xNTUlM2EyNzEwJTJmYW5ub3VuY2UmdHI9dWRwJTNhJTJmJTJmNDYuNC4xMDkuMTQ4JTNhNjk2OSUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjUuNzkuMjQ5Ljc3JTNhNjk2OSUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjUuNzkuODMuMTkzJTNhNjk2OSUyZmFubm91bmNlJnRyPXVkcCUzYSUyZiUyZjUxLjI1NC4yNDQuMTYxJTNhNjk2OSUyZmFubm91bmNlJnRyPWh0dHAlM2ElMmYlMmY1OS4zNi45Ni43NyUzYTY5NjklMmZhbm5vdW5jZSZ0cj11ZHAlM2ElMmYlMmY3NC44Mi41Mi4yMDklM2E2OTY5JTJmYW5ub3VuY2U'''
length = len(s)
padding = length % 4
s += padding*b'='
decoded = base64.b64decode(s)
print(decoded)
# b'Hello'


# In[1]:


pypinyin.pinyin('中国', style=pypinyin.NORMAL)
# ['zhong', 'guo']  # 无声调

pypinyin.pinyin('中国', style=pypinyin.TONE)
# ['zhōng', 'guó']   # 输出声调


# In[3]:


print(dir(pyhaven))
# print((exString.PinYinList(exWebcrawler.todayPoetry())))
# print((exString.PinYinList()))
# print(exWebcrawler.searchPoetry())
print((pyhaven.expString.PinYinList(pyhaven.expWebcrawler.searchPoetry())))


# In[14]:


def PinYinList(Text, splitPattern=True, ParagraphWidth=10):
    """
    获取文本的拼音列表
    Args:
        Text: 输入文本
        splitPattern: 是否按标点分割
        ParagraphWidth: 段落宽度
    """
    # 预处理：删除首尾空白
    Text = Text.strip()

    # 检查是否是带标题的格式（包含〕或]后跟换行）
    title_match = re.search(r'(?<=(\]|〕))\n.*\n', Text)

    if title_match:
        # 处理带标题的文本
        contentStartIndex = title_match.end()
        TitleText = Text[:contentStartIndex]
        ContentText = Text[contentStartIndex:].replace('\n', '')

        # 分段处理
        if not (splitPattern) and ParagraphWidth > 0:
            TextList = TitleText.split('\n') + [
                ContentText[i:i+ParagraphWidth]
                for i in range(0, len(ContentText), ParagraphWidth)
            ]
        else:
            pattern = r"([\u3002\uff0c\uff1b\u3001\uff1a\u201c\u201d\uff01\uff1f])"
            ContentTextList = re.split(pattern, ContentText)
            ContentTextList = [
                ContentTextList[i] + ContentTextList[i+1]
                for i in range(0, len(ContentTextList)//2*2, 2)
            ]
            TextList = TitleText.split('\n') + ContentTextList
    else:
        # 处理普通文本
        TextList = Text.split('\n')

    allList = []
    # 处理每一行文本
    for line in TextList:
        if not line.strip():  # 跳过空行
            allList.append('\n')
            continue

        pinyin_str = pypinyin.pinyin(line, style=pypinyin.TONE)

        # 拼音行：用两个空格分隔
        pinyins = []
        for char, pin in zip(line, pinyin_str):
            if '\u4e00' <= char <= '\u9fff':  # 是汉字
                pinyins.append(pin[0])
        if pinyins:
            allList.append('  '.join(pinyins) + '\n')

            # 汉字行：对应拼音位置
            char_line = ''
            current_pos = 0
            for char in line:
                if '\u4e00' <= char <= '\u9fff':  # 是汉字
                    char_line += char + '  '
                else:  # 标点符号
                    char_line += char + ' '
            allList.append(char_line.rstrip() + '\n\n')
        else:
            allList.append(line + '\n\n')

    return ''.join(allList)


s = '''
青玉案 元夕
朝代:宋　作者:辛弃疾　体裁:词　

东风夜放花千树，
更吹落，星如雨。
宝马雕车香满路。
凤箫声动，玉壶光转，
一夜鱼龙舞。

蛾儿雪柳黄金缕，
笑语盈盈暗香去。
众里寻他千百度，
蓦然回首，那人却在，
灯火阑珊处。
'''

print(PinYinList(s))


# In[37]:


'''
获取文本的拼音列表
pypinyin: 拼音转换工具
re: 正则表达式 
'''


def PinYinList(Text, splitPattern=True, ParagraphWidth=10):
    print(repr(Text))
    # 中文标点符号
    pattern = r"([\u3002\uff0c\uff1b\u3001\uff1a\u201c\u201d\uff01\uff1f])"
    # 获取正文开始的索引
    contentStartIndex = re.search(r'(?<=(\]|〕))\n.*\n', Text).end()
    # 获取标题文本和正文文本
    TitleText = Text[:contentStartIndex]
    ContentText = Text[contentStartIndex:].replace('\n', '')

    # 如果不需要分割标点且段落宽度>0,则按段落宽度分割文本
    if not (splitPattern) and ParagraphWidth > 0:
        n = ParagraphWidth
        TextList = TitleText.split(
            '\n') + [ContentText[i:i+n] for i in range(0, len(ContentText), n)]
    else:
        # 否则根据标点符号分割文本
        ContentTextList = re.split(pattern, ContentText)
        ContentTextList = [ContentTextList[i]+ContentTextList[i+1]
                           for i in range(0, len(ContentTextList)//2*2, 2)]
        TextList = TitleText.split('\n') + ContentTextList
    allList = []
    PinYinList = []

#     print('-----')
#     print(TextList)
    # 获取每段文本的拼音列表
    for Text in TextList:
        pinyin_str = pypinyin.pinyin(Text, style=pypinyin.TONE)
        PinYinList = [item[0] for item in pinyin_str]

        # 如果拼音列表中包含〔〕\[\],则跳过
        if re.search(r"[〔〕\[\]]", ''.join(PinYinList)):
            pass
        else:
            for i in range(len(PinYinList)):
                # 如果是英文字母,左对齐宽度为6
                if PinYinList[i].isalpha():
                    allList.append(f"{PinYinList[i]:<6}")
                else:
                    # 否则补6个空格
                    allList.append(" "*6)
                    allList.append('')
        allList.append('\n')
        for i in range(len(Text)):
            # 添加文本内容,左对齐宽度为5
            allList.append(f"{Text[i]:<5}")
            allList.append('')
        allList.append('\n')

    return (''.join(allList))  # 返回拼音列表


# 示例1: 获取古诗词的拼音列表
print(PinYinList(expWebcrawler.searchPoetry(), splitPattern=True))
# 示例2: 获取今日诗词的拼音列表
# print(PinYinList(expWebcrawler.todayPoetry(),splitPattern=True))


# In[ ]:


# In[171]:


# python
def PinYinList(Text, splitPattern=True, ParagraphWidth=10):
    # 中文标点符号
    pattern = r"([\u3002\uff0c\uff1b\u3001\uff1a\u201c\u201d\uff01\uff1f])"
    contentStartIndex = re.search(r'(?<=\])\n.*\n', Text).end()

    TitleText = Text[:contentStartIndex]
    ContentText = Text[contentStartIndex:].replace('\n', '')

    if not (splitPattern) and ParagraphWidth > 0:
        n = ParagraphWidth
        TextList = TitleText.split(
            '\n') + [ContentText[i:i+n] for i in range(0, len(ContentText), n)]
    else:
        ContentTextList = re.split(pattern, ContentText)
        ContentTextList = [ContentTextList[i]+ContentTextList[i+1]
                           for i in range(0, len(ContentTextList)//2*2, 2)]

        TextList = TitleText.split('\n') + ContentTextList
    allList = []
    PinYinList = []

    for Text in TextList:
        pinyin_str = pypinyin.pinyin(Text, style=pypinyin.NORMAL)
        # [['zhōng'], ['xīn']]

        PinYinList = [item[0] for item in pinyin_str]

        if re.search(r"[〔〕\[\]]", ''.join(PinYinList)):
            pass
        else:
            for i in range(len(PinYinList)):
                if PinYinList[i].isalpha():
                    allList.append(f"{PinYinList[i]:<6}")
                else:
                    allList.append(" "*6)
                allList.append('')
        allList.append('\n')
        for i in range(len(Text)):
            allList.append(f"{Text[i]:<5}")
            allList.append('')
        allList.append('\n')

    return (''.join(allList))


# print(PinYinList(exWebcrawler.searchPoetry(),splitPattern=pattern))
print(PinYinList(exWebcrawler.todayPoetry(), splitPattern=True))


# In[132]:


s = exWebcrawler.todayPoetry()
print(re.search(r'(?<=\])\n.*\n', s))
print(s.end())


# In[123]:


ContentText = '李白牛渚西江夜，青天无片云。登舟望秋月，空忆谢将军。余亦能高咏，斯人不可闻。明朝挂帆席，枫叶落纷纷。'
splitPattern = r"([\u3002\uff0c\uff1b\u3001\uff1a\u201c\u201d\uff01\uff1f])"

print(re.split(splitPattern, ContentText))


# In[ ]:


# In[95]:


s = '八月秋高风怒号，卷我屋上三重茅。   〔    唐    代    〕  ]\n茅飞渡江洒江郊，高者挂罥长林梢，下者飘转沉塘坳。'
s = s.replace('\n', '')
print(re.search(r"[〕\]]", s).start())
print(s[34])
l = [s[i:i+2] for i in range(0, len(s), 2)]
print(l)
