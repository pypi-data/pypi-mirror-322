# coding: utf-8
r"""
算法和数据结构:
binarySearchSensitivity - 二分搜索灵敏度
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
def binarySearchSensitivity(minn=0.05, maxx=8):
    """
    parameter:
    二分搜索灵敏度
    (minn=0.05, maxx=8)
    """
    preSelectList = []

    def sensitivity(minn=0.05, maxx=8):
        average = (minn + maxx) / 2
        print(
            "Sensitivity:{:0.2f}".format(average)
            + " (input None is exit,P is previous)"
        )
        print("A.faster    B.slower")
        print("Please pick A or B:")
        userSelect = input().upper()
        preSelectList.append(userSelect)
        if userSelect == "":
            return average
        elif userSelect == "A":
            sensitivity(minn, average)
        elif userSelect == "B":
            sensitivity(average, maxx)
        elif userSelect == "P":
            # search previous select's index
            i = preSelectList.index(userSelect) - 1
            if i < 0:
                return average
            if preSelectList[i] == "A":
                preSelectList[i] = "P"
                sensitivity(minn, maxx * 2 - minn)
            elif preSelectList[i] == "B":
                preSelectList[i] = "P"
                sensitivity(minn * 2 - maxx, maxx)

    sensitivity(minn, maxx)


if __name__ == "__main__":
    print(binarySearchSensitivity())



