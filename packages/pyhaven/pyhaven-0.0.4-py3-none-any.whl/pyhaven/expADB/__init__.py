# coding: utf-8
r"""
explore Android Debug Bridge
探索 ADB 命令

checkDelapp - 检查app文件中是否存在delapp文件中的应用
get_cwd - 获取当前工作目录
pull_all_apkfile - 导出手机所有应用名称和安装包
"""

__version__ = "0.1"
__author__ = "mingwe <shannonhacker@outlook.com>"


import subprocess
import types
import os
import re


def checkDelapp(app: str, delapp: str):
    """
    检查app文件中是否存在delapp文件中的应用

    参数:
    - app:存放应用列表的文件
    - delapp:存放需要检查的应用列表的文件

    功能:
    - 读取两个文件中的应用列表
    - 清理delapp文件中的应用名格式
    - 检查每个需要检查的应用是否存在于app文件中
    - 如果存在,打印应用名和在app列表中的位置
    """
    with open(app, "r", encoding="utf-8") as f:
        applist = f.read()

    with open(delapp, "r", encoding="utf-8") as f:
        delapplist = f.read()

    # 使用正则表达式清理delapplist中的应用名格式
    delapplist = re.sub(r'[^\u4e00-\u9fff\x20\.\w\d\-_]+', '\n', delapplist)
    delapplist = re.findall(r'com[\S]+', delapplist)

    # 遍历需要检查的应用
    for a in delapplist:
        result = applist.find(a)
        if result != -1:
            # 如果存在,打印应用名和位置
            print(a, result)


def get_cwd():
    """
    获取当前工作目录

    返回一个元组,包含:
    - 当前工作目录
    - 当前Python文件所在的目录
    """

    cwd = os.getcwd()
    # 使用os.getcwd()获取当前工作目录

    file_path = os.path.abspath(__file__)
    # 获取当前Python文件绝对路径

    file_dir = os.path.dirname(file_path)
    # 从文件路径中提取目录部分

    return cwd
    # 返回一个包含当前工作目录和文件目录的元组


def pull_all_apkfile():
    """
    pull_all_apkfile - 导出手机所有应用名称和安装包
    """
    # 获取当前工作目录
    cwd = os.getcwd()
    saveDirPath = os.path.join(cwd, "apks")
    # 创建apk保存目录apks
    if not os.path.exists(saveDirPath):
        os.makedirs(saveDirPath)

    # 获取包信息
    p1 = subprocess.Popen(
        "adb shell pm list packages -f", stdout=subprocess.PIPE, shell=True
    )
    out1 = p1.stdout.read().decode()

    # 清理空行
    # out1 = re.sub(r"[^\u4e00-\u9fff\x20\.\w\d\-_]+", "\n", out1)
    out1 = re.sub(r"\s+", "\n", out1)

    # 保存原始数据到apps.txt
    with open("apps.txt", "w") as f:
        f.write(out1)

    # 解析每行包信息
    with open("apps.txt") as f:
        for line in f:
            # 提取apk路径
            filePath = re.findall(r"(?<=package:).*\.apk", line)[0]

            # 提取包名
            package_name = re.findall(r"(?<=\.apk=)[\w\.]*", line)[0]

            # 拉取apk到保存目录saveDirPath
            saveFilePath = os.path.join(saveDirPath, f"{package_name}.apk")
            # print(f'adb pull "{filePath}" "{saveFilePath}"\n')
            os.system(f'adb pull "{filePath}" "{saveFilePath}"')



# __all__ = [
#     name
#     for name, obj in globals().items()
#     if not name.startswith("_")
#     and not isinstance(obj, types.ModuleType)
#     and name not in {"wantobjects"}
# ]
if __name__ == "__main__":
    print(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(os.getcwd(), "apks"))
    print(dir())
    print(__all__)
