# coding: utf-8
r"""
explore Artificial Intelligence
探索 AI 模块
"""
import types
import pyttsx3
__version__ = "0.1"
__author__ = "mingwe <shannonhacker@outlook.com>"
# __all__ = [
#     name
#     for name, obj in globals().items()
#     if not name.startswith("_")
#     and not isinstance(obj, types.ModuleType)
#     and name not in {"wantobjects"}
# ]


def TTS_gtts(text):
    """
    gTTS:这个库使用Google的文本到语音服务,可以将文本转化为语音文件,支持多种语言和语音,比较简单易用。
    """
    from gtts import gTTS

    tts = gTTS(text="Hello World", lang="en", slow=False)
    tts.save("hello.mp3")


def TTS_pyttsx3(text):
    """
    Pyttsx3:这是一个文本到语音转换库,支持多种语音引擎,比如SAPI5,NSSpeechSynthesizer,espeak等。用法简单,可以快速将文本转为语音。
    """
    # import pyttsx3

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



if __name__ == "__main__":
    print(dir())
    print(__all__)
