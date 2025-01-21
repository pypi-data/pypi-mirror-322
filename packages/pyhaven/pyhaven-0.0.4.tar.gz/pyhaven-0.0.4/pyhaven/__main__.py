# 使用相对方式导入子包，只会导入当前包中的子包,不会导入当前包本身。
from . import (
    expADB,
    expAI,
    expAlgorithm,
    expAutomation,
    expDatetime,
    expGraph,
    expMath,
    expMC,
    expPackage,
    expString,
    expTools,
    expWebcrawler,
)

# 使用绝对方式导入子包，Python interpreter会首先找到pyexplore包,然后再从其中导入expADB包等其他子包。
# 这个过程会将pyexplore包导入到当前命名空间。
# import pyhaven.expADB
# import pyhaven.expAI
# import pyhaven.expAlgorithm
# import pyhaven.expAutomation
# import pyhaven.expDatetime
# import pyhaven.expGraph
# import pyhaven.expMath
# import pyhaven.expPackage
# import pyhaven.expString
# import pyhaven.expTools
# import pyhaven.expWebcrawler


identifier_rules = r"""
根据PEP 8对Python标识符命名的规范,主要有以下规则:
According to the PEP 8 specification for naming Python identifiers, the main rules are as follows:

1. 只使用英文ascii字母(a-z, A-Z)、数字(0-9)和下划线(_)。不使用特殊字符。
Only use English ascii letters (a-z, A-Z), numbers (0-9) and underscores (_). Do not use special characters.

2. 类名使用驼峰命名法,首字母大写,如 MyClass。
Class names use CamelCase, with the first letter capitalized, e.g. MyClass.

3. 函数、方法、变量名全部小写,单词以下划线连接,如 my_function()。
Function, method and variable names are all lowercase, with words connected by underscores, e.g. my_function().

4. 常量全部大写,单词以下划线连接,如 MAX_VALUE。
Constants are all uppercase, with words connected by underscores, e.g. MAX_VALUE.

5. 模块名简短小写,可使用下划线连接,如 my_module.py。
Module names are short and lowercase, can use underscores, e.g. my_module.py.

6. 包名简短小写,不用下划线连接,如 mypackage。
Package names are short and lowercase, without underscores, e.g. mypackage.

7. 避免使用单字符名称,除了计数器和迭代器。
Avoid single letter names, except for counters and iterators.

8. 私有属性和方法以一个下划线开头,如 _private_method()。
Private attributes and methods start with a single underscore, e.g. _private_method().

9. 保护实例属性以两个下划线开头,如__protected_field。
Protected instance attributes start with double underscores, e.g. __protected_field.

10. 不要使用双下划线开头的方法名(如__init__),以避免与Python特殊方法冲突。
Do not use double-underscore prefixed method names like __init__ to avoid conflicts with Python special methods.

综上,PEP 8推荐使用有意义并且能明确表示变量用途的标识符命名,使代码更具可读性。
In summary, PEP 8 recommends using meaningful identifiers that can explicitly indicate the purpose of variables for more readable code.
"""


if __name__ == "__main__":
    # 创建一个字典，用于存储全局变量的名称和值
    # 使用字典推导式，遍历globals()函数返回的字典，将其键值对复制到新的字典中
    globals_dict = {k: v for k, v in globals().items()}

    # 也可以使用copy()方法，直接复制globals()函数返回的字典
    globals_dict = globals().copy()

    # 遍历新的字典，打印每个全局变量的名称和值，使用f字符串格式化输出
    for k, v in globals_dict.items():
        print(f"{k}:{v}")

    # 打印dir()函数返回的列表，它包含了当前作用域中的所有变量的名称
    print(f"\ndir(): {dir()}")

    print(f"\nlocals(): {locals()}")
