# coding: utf-8
r"""
日期时间相关:
getTimeBuckets - 时间段计算
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


if __name__ == "__main__":
    print(getTimeBuckets("18:45"))



