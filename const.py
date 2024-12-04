from enum import Enum
import json

class SubjectType(Enum):
    漫画 = 1
    动画 = 2
    音乐 = 3
    游戏 = 4
    三次元 = 6

# with json.open()