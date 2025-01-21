"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="pyhaven",  # Required 项目名称
    version="0.0.4",  # Required 发布版本号
    description="This is the package used to explore Python.",  # Optional 项目简单描述
    long_description=long_description,  # Optional 详细描述
    long_description_content_type="text/markdown",  # 内容类型
    url="",  # Optional github项目地址
    author="mingwei",  # Optional 作者
    author_email="mingwe.me@qq.com",  # Optional 作者邮箱
    classifiers=[  # Optional 分类器通过对项目进行分类来帮助用户找到项目, 以下除了python版本其他的 不需要改动
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="explore, python , development",  # Optional 搜索关键字
    package_dir={
        "": "."
    },  # Optional 手动指定包目录
    packages=find_packages(
        where=".",
        include=[
            "pyhaven",
            "pyhaven.expADB",
            "pyhaven.expAI",
            "pyhaven.expAlgorithm",
            "pyhaven.expAutomation",
            "pyhaven.expDatetime",
            "pyhaven.expGraph",
            "pyhaven.expMath",
            "pyhaven.expMC",
            "pyhaven.expPackage",
            "pyhaven.expString",
            "pyhaven.expTools",
            "pyhaven.expWebcrawler",
        ],
    ),  # Required
    python_requires=">=3.12, <4",  # python 版本要求
    install_requires=[
        "pyperclip",
        "requests",
        "pyautogui",
        "bs4",
        "pyttsx3",
        "pypinyin",
    ],  # Optional 第三方依赖库
    # extras_require={  # Optional
    #     "dev": ["check-manifest"],
    #     "test": ["coverage"],
    # },
    # package_data={  # Optional       包数据
    #     "sample": ["package_data.dat"],
    # },
    # data_files=[("my_data", ["data/data_file"])],
    # entry_points={  # Optional
    #     "console_scripts": [
    #         "sample=sample:main",
    #     ],
    # },
    # project_urls={  # Optional 和项目相关的 其他网页连接资源
    #     "Bug Reports": "",
    #     "Funding": "",
    #     "Say Thanks!": "",
    #     "Source": "",
    # },
)
