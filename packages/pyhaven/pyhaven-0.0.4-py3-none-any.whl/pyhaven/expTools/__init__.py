# coding: utf-8
# 🌐 设置文件编码为UTF-8

# 📚 模块的文档字符串，简要说明模块的用途
r"""
This module contains some tools for explore python.
这个模块包含了一些用于探索Python的工具。
"""

# 🧩 导入types模块，用于类型检查
import types

# 📌 定义模块的版本号
__version__ = "0.1.0"
# 👨‍💻 定义模块的作者信息
__author__ = "mingwe <shannonhacker@outlook.com>"


# 🧰 定义一个函数，用来查看模块的所有方法和属性
def explore_module(module):
    """
    探索模块的内容并返回详细信息。

    :param module: 要探索的模块
    :type module: module
    :return: 包含模块信息的字符串
    :rtype: str
    """
    # 📝 创建一个空字符串来存储结果
    result = ""

    # 📌 添加模块名称到结果中
    result += f"正在检查模块 '{getattr(module, '__name__',None)}'\n"

    all_attribute = [
        # 🔍 遍历全局变量字典
        name
        for name in dir(module)
        # ✅ 只选择不以下划线开头的变量
        if not name.startswith("_")
        # ✅ 排除在集合里的变量
        and name not in {"wantobjects", "types"}
    ]

    # 🔍 遍历模块的所有属性
    for item_name in all_attribute:
        # 🎣 获取属性的值
        item_value = getattr(module, item_name, None)

        # 🧠 判断属性是否是可调用的（比如函数或方法）
        if callable(item_value):
            # 📘 如果是可调用的，添加方法信息
            result += f"方法 '{item_name}' 来自模块 '{item_value.__module__}'\n"
            result += f"方法 '{item_name}' 的说明文档是：\n'{item_value.__doc__}'\n"
        else:
            # 📊 如果不是可调用的，添加属性信息
            result += f"属性 '{item_name}' 的值是 '{item_value}'\n"

        # ➖ 添加分隔线
        result += "_" * 80 + "\n"

    # 📬 返回收集到的所有信息
    return result


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


# 🏁 如果这个文件是作为主程序运行的
if __name__ == "__main__":
    # 🖨️ 打印当前模块的名称
    print(f"{__name__=}")

    # ⏰ 导入时间模块
    import time

    # 🔍 使用我们的函数来探索时间模块，并打印结果
    # print(explore_module(time))
    print(__all__)
