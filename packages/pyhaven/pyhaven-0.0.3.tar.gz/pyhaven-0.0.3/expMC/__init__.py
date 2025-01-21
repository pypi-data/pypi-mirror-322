# coding: utf-8
# 🌐 设置文件编码为UTF-8

# 📚 模块的文档字符串，简要说明模块的用途
r"""
有关于Minecraft mcpipy的工具
"""

# 🧩 导入types模块，用于类型检查
import types
import re
import os
import sys

# 📌 定义模块的版本号
__version__ = "0.1.0"
# 👨‍💻 定义模块的作者信息
__author__ = "mingwe <shannonhacker@outlook.com>"


def get_block_dict(path=None):
    MyNutstore_dir = os.environ["MyNutstore_dir"]
    file_path = r"0_Shannon2024\0_workspace\1_工作资料\1_体验课\Python\用Python玩我的世界\1_启动器\HMCL\.minecraft\versions\1.12.2\mcpipy\mcpi\block.py"
    if path is None:
        path = os.path.join(MyNutstore_dir, file_path)

    # 存储方块ID的临时字典,用于解析引用
    block_ids = {}
    # 最终的方块字典
    block_dict = {}

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

        # 第一遍扫描:收集所有直接定义的方块ID
        for line in lines:
            # 匹配形如 "BLOCK = Block(id)" 的模式
            match = re.match(r"^([A-Z_]+)\s*=\s*Block\((\d+)", line)
            if match:
                name, block_id = match.groups()
                block_ids[name] = int(block_id)

        # 第二遍扫描:处理所有方块定义
        for line in lines:
            # 匹配直接用数字定义的方块
            match1 = re.match(r"^([A-Z_]+)\s*=\s*Block\((\d+)(?:\s*,\s*(\d+))?\)", line)
            if match1:
                name = match1.group(1)
                block_id = int(match1.group(2))
                data = int(match1.group(3)) if match1.group(3) else 0
                block_dict[(block_id, data)] = name
                continue

            # 匹配引用其他方块ID的定义
            match2 = re.match(
                r"^([A-Z_]+)\s*=\s*Block\(([A-Z_]+)\.id\s*,\s*(\d+)\)", line
            )
            if match2:
                name = match2.group(1)
                ref_block = match2.group(2)
                data = int(match2.group(3))
                if ref_block in block_ids:
                    block_id = block_ids[ref_block]
                    block_dict[(block_id, data)] = name

    return block_dict


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
    # print(f"{__name__=}")
    path = r"C:\BaiduSyncdisk\MyNutstore\0_Shannon2024\0_workspace\1_工作资料\1_体验课\Python\用Python玩我的世界\1_启动器\HMCL\.minecraft\versions\1.12.2\mcpipy\mcpi\block.py"
    blocks = get_block_dict()
    print(blocks[(35, 1)])  # 输出: "WOOL_ORANGE"
    print(blocks[(1, 0)])  # 输出: "STONE"
