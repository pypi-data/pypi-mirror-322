# coding: utf-8
r"""
Python发布包:
getPyFunctionName - 得到py文件函数名
"""
__version__ = "0.1"
__author__ = "mingwe <shannonhacker@outlook.com>"


import types
import re
import os
import pyhaven


def getPyFunctionName(path=""):
    """
    ::path py文件路径
    获取python源代码中的所有函数名(key)和函数文档(value)
    """
    with open(path, "r", encoding="utf-8") as f:
        text = ""
        for line in f.readlines():
            text += line
    __all__ = [
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and not isinstance(obj, types.ModuleType)
        and name not in {"wantobjects"}
    ]
    FunctionNameList = re.findall(r"(?<=\ndef ).{1,30}(?=\()", text)
    # print(f"{FunctionNameList=}")
    return FunctionNameList


def getSubpackageName(package):
    """
    得到所有子包的名字(主包名字)
    """
    dir_path = package.__path__[0]
    dir_names = os.listdir(dir_path)  # 获取目录下的所有文件及文件夹名字
    # print(dir_names)
    sub_dirs = []
    for name in dir_names:
        path = os.path.join(dir_path, name)  # 将目录和名字合成路径
        # 如果是文件夹 并 不以'_'，不以'.'开头
        if (
            os.path.isdir(path)
            and not name.startswith("_")
            and not name.startswith(".")
        ):
            sub_dirs.append(name)  # 添加到列表中

    return sub_dirs  # 返回子文件夹名字


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
    print(
        getPyFunctionName(
            r"P:\JupyterNotebookCodes\0_exercise\pyhaven\expPackage\__init__.py"
        )
    )

    print(",\n".join(getSubpackageName(pyhaven)))
