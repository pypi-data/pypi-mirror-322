# coding: utf-8
r"""
字符串处理:
mingEncode - 自定义编码器
charInfo - 字符信息
deleteTab - 删除制表符
replaceSpace - 替换空格
replaceComma - 替换逗号
replaceLineFeed - 替换换行
text2pinyin - 获取文本的拼音列表
delSpacelines - 删除字符串text中空行
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
import pypinyin
import unicodedata


def mingEncode(s="", encoding="utf-8", errors="strict") -> bytes:
    """
    返回编码为 bytes 的字符串。

    encoding 默认为 'utf-8' ；请参阅 标准编码 了解其他可能的值。

    errors 控制如何处理编码错误。 如为 'strict' (默认值)，则会引发 UnicodeError。
    """
    pass
    # UTF-16BE	4E 00	01001110 00000000
    #                   0100 111000 000000
    # UTF-8	 E4 B8 80	1110,0100 10,111000 10,000000


"""
    范围                             编码
    U-00000000 ... U-0000007F        0xxxxxxx
    U-00000080 ... U-000007FF        110xxxxx 10xxxxxx
    U-00000800 ... U-0000FFFF        1110xxxx 10xxxxxx 10xxxxxx
    U-00010000 ... U-0010FFFF        11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

    0 0000 0000 0000 0000 0000:0000
    0 0000 0000 0000 0111 1111:007f

    0 0000 0000 0000 1000 0000:0080
    0 0000 0000 0111 1111 1111:07ff

    0 0000 0000 1000 0000 0000:0800
    0 0000 1111 1111 1111 1111:ffff

    0 0001 0000 0000 0000 0000:010000
    1 0000 1111 1111 1111 1111:10ffff
"""


def charInfo(char="") -> dict:
    """
    编码	     hex	       dec (bytes)	     dec	    binary
    UTF-8	    E4 B8 80	   228 184 128	     14989440	11100100 10111000 10000000
    UTF-16BE	4E 00	       78 0	             19968	    01001110 00000000
    UTF-16LE	00 4E	       0 78	             78	        00000000 01001110
    UTF-32BE	00 00 4E 00	   0 0 78 0	         19968	    00000000 00000000 01001110 00000000
    UTF-32LE	00 4E 00 00	   0 78 0 0	         5111808	00000000 01001110 00000000 00000000

    """
    pass


def deleteTab():
    """
    去除\t符号
    """
    text = pyperclip.paste()
    # text = """
    #         - 本课主题：运算符
    #         - 本课内容：学习算术、逻辑、关系三大运算符等知识用它们来帮我们解决一些实际生活中的问题。
    #         - 总体评价：本节课铠涵学习了c++中的运算符以及运算符的规则。并且每种运算符都做了足够的练习，这为以后的学习打下了坚实的基础。铠涵，希望你下次上课可以多做笔记。

    # """
    # print("-----output------")
    text = text.replace("\t", "")
    text = text.replace(" ", "")

    pyperclip.copy(text)
    return text

    # print('\t',ord('\t'))


def replaceSpace():
    """
    replace header's space and minus sign to comma.
    """
    text = pyperclip.paste()
    text = text.replace("\n        -", ",")
    text = text.replace("        -", "")
    text = text.replace(" ", "")

    pyperclip.copy(text)
    return text


def replaceComma():
    """
    replace English comma to Chinese comma.
    """
    text = pyperclip.paste()
    text = text.replace(",", "，")
    text = text.replace(".", "。")
    text = text.replace(":", "：")

    pyperclip.copy(text)
    return text


def auto_LF(text="", width=80):
    """
    自动换行，会在标点符号处优先换行

    参数:
        text (str): 要处理的文本，默认为空字符串
        width (int): 每行最大字符数，默认80个字符

    返回:
        str: 处理后的文本
    """
    if not text:
        text = pyperclip.paste()

    # 定义中文标点符号
    punctuation = r"[，。！？；：、）》」』】\n\r]"

    result = []
    current_line = []
    current_length = 0

    # 将文本按字符分割
    words = list(text.strip())

    for i, char in enumerate(words):
        char_width = 2 if "\u4e00" <= char <= "\u9fff" else 1
        next_char = words[i + 1] if i + 1 < len(words) else ""

        # 如果当前行加上新字符超过限制
        if current_length + char_width > width:
            result.append("".join(current_line))
            current_line = []
            current_length = 0

        current_line.append(char)
        current_length += char_width

        # 在标点符号后换行的条件：
        # 1. 当前是标点符号
        # 2. 当前行长度超过width-10
        # 3. 不是行尾
        if (
            re.match(punctuation, char)
            and current_length > width - 10
            and i < len(words) - 1
        ):
            result.append("".join(current_line))
            current_line = []
            current_length = 0

    # 添加最后一行
    if current_line:
        result.append("".join(current_line))

    # 合并所有行
    formatted_text = "\n".join(result)

    # 复制到剪贴板
    pyperclip.copy(formatted_text)

    return formatted_text


def auto_ordered_list(
    text="",
    search=r"\d\u3001",
):
    """
    自动换行
    """
    if text == "":
        text = pyperclip.paste()

    textList = re.sub(f"({search})", "\n", text).split()
    text = "\n".join([f"{i + 1}. {textList[i]}" for i in range(len(textList))])

    pyperclip.copy(text)
    return text


def text2pinyin(text, pinyin_style=pypinyin.TONE, width=80):
    """
    zì dòng shēng chéng hàn zì de pīn yīn
    自 动   生    成    汉  字 的 拼  音  ，

    gēn jù pīn yīn zì mǔ shù liàng tiáo zhěng jiàn gé
    根  据 拼  音  字 母 数  量    调   整    间   隔 。

    bǎo zhèng hàn zì yǔ pīn yīn duì qí
    保  证    汉  字 与 拼  音  对  齐 。
    """

    def auto_LF(text="", width=80):
        """
        自动换行，会在标点符号处优先换行

        参数:
            text (str): 要处理的文本，默认为空字符串
            width (int): 每行最大字符数，默认80个字符

        返回:
            str: 处理后的文本
        """

        # 定义中文标点符号
        punctuation = r"[，。！？；：、）》」』】\n\r]"

        result = []
        current_line = []
        current_length = 0

        # 将文本按字符分割
        words = list(text.strip())

        for i, char in enumerate(words):
            char_width = 2 if "\u4e00" <= char <= "\u9fff" else 1
            next_char = words[i + 1] if i + 1 < len(words) else ""

            # 如果当前行加上新字符超过限制
            if current_length + char_width > width:
                result.append("".join(current_line))
                current_line = []
                current_length = 0

            current_line.append(char)
            current_length += char_width

            # 在标点符号后换行的条件：
            # 1. 当前是标点符号
            # 2. 当前行长度超过width-10
            # 3. 不是行尾
            if (
                re.match(punctuation, char)
                and current_length > width - 10
                and i < len(words) - 1
            ):
                result.append("".join(current_line))
                current_line = []
                current_length = 0

        # 添加最后一行
        if current_line:
            result.append("".join(current_line))

        # 合并所有行
        formatted_text = "\n".join(result)

        return formatted_text

    def split_pinyin_list(pinyin_list):
        result = []

        for item in pinyin_list:
            current = item[0]  # 获取当前拼音项

            # 使用更简单的正则表达式来分割不同类型的字符
            parts = re.findall(
                r"([\d]+)|([a-zA-Záéíóúüāēīōūǖáéíóúǎěǐǒǔǚàèìòùǜ]+)|([（\(\)）])|([!\"#$%&\'*+,-./:;<=>?@^_`{|}\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b])",
                current,
            )
            # 打印分割后的部分
            # print(parts,current)
            if parts:
                for part in parts:
                    # 找到非空的部分
                    matched = next((x for x in part if x), "")
                    if matched:  # 只添加非空匹配
                        result.append([matched])
            else:
                # 如果没有匹配到任何部分，添加原始项
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

    # 如果输入为'test'，则返回彩蛋
    if text == "test":
        text = """
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
"""
    text = text.strip()
    text = re.sub(r"\n+", "\n", text)
    # 自动换行
    text = auto_LF(text=text, width=width)
    allList = []
    for line in text.split("\n"):
        if not line.strip():
            allList.append("")
            continue
        # 去除声调
        line = remove_tone_marks(line)

        # 去除空白字符
        line = re.sub(r"\s+", "", line)
        tokens = re.findall(
            r"[\u4e00-\u9fff]|[\d]+|[a-zA-Z]+|[^\s\u4e00-\u9fffa-zA-Z]", line
        )
        # print(f"{tokens=}, len:{len(tokens)}")

        pinyin_str = pypinyin.pinyin(line, style=pinyin_style)
        pinyin_str = split_pinyin_list(pinyin_str)
        # 打印拼音列表
        # print(f"pinyin_str:{pinyin_str}, len:{len(pinyin_str)}")
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
            elif token.isdigit():
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
                            char_line += char + " " * (len(pinyins[i]) + spaces - 2)
                        else:
                            # 字母不需要根据拼音长度决定间隔，直接指定一个空格
                            char_line += char + " "
                    else:
                        char_line += char

            allList.append(char_line.rstrip() + "\n")
        else:
            allList.append(line + "\n")

    return "".join(allList)


def delSpacelines(text: str = "") -> str:
    """
    删除字符串text中空行

    参数:
    text:输入的文本字符串

    返回:
    删除空行后的文本字符串
    """

    # 使用正则表达式匹配非中文、数字、字母、标点等的任意字符
    # 将其替换为换行符
    text = re.sub(r"[^\u4e00-\u9fff\x20\.\w\d\-_]+", "\n", text)

    return text


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
    poetry = "《夜泊牛渚怀古》\n[唐]\n李白\n牛渚西江夜，青天无片云。\n登舟望秋月，空忆谢将军。\n余亦能高咏，斯人不可闻。\n明朝挂帆席，枫叶落纷纷。"

    # 示例1: 获取古诗词的拼音列表
    # print(text2pinyin(expWebcrawler.searchPoetry(),splitPattern=pattern) )
    # 示例2: 获取今日诗词的拼音列表
    # poetry = "中,国A加，油"

    poetry = "为什么所有APP都解决不了这个小问题？"
    poetry = "单（chán匈奴族首领）于只会骑马"
    poetry = "sample( 序列,取样的个数 )  test )，返回的是列表"
    # poetry = "根  据  拼 音  字  母 数 量  调    整   间    隔"

    print(text2pinyin("test"))

# if __name__ == "__main__":
#     # import re
#     text = """
#     1、熟悉编程环境2、熟悉键鼠操作
# 3、掌握顺序执行、对象、方法、参数、整数
#     """
#     print("-----output------")
#     print(autoLf(text))
