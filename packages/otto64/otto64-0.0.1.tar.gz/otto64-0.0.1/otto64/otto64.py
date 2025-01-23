import base64

__all__ = ['text_to_otto64', 'otto64_to_text']

ottowords = [
    '三人', '上不去', '上路', '下不来',
    '不值得', '不配', '东厂', '中单',
    '为什么', '优越狗', '但是呢', '低分狗',
    '你告诉我', '健全', '创死', '卡在这里了',
    '卡比兽', '发育', '啥币', '回忆',
    '垃圾', '夺冠', '打比赛', '如果',
    '实力', '对', '尊尼获加', '小号',
    '尴尬', '怎么', '急眼', '总管',
    '患者', '想操作', '意义', '打野',
    '掉下去', '时光', '晚期', '最后',
    '最猛', '有什么', '杠精', '段位',
    '独轮车', '电棍', '癌症', '白银',
    '盲僧', '看不惯', '瞅几把', '知道',
    '祭拜', '穷抬杠', '膨胀', '自己',
    '虚空', '西厂', '起劲', '越塔',
    '道理', '青铜', '顺从', '飞舞',
    '黄金'
]
ottowords.sort()

base64charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def base64_to_otto64(raw: str) -> str:
    ret = []
    for c in raw:
        if c in base64charset:
            ret.append(ottowords[base64charset.index(c)])
        else:
            raise ValueError(f"Unexpected token: {c}")
    return ''.join(ret)


def otto64_to_base64(raw: str) -> str:
    ret = []
    while raw:
        flag = False
        for i, word in enumerate(ottowords):
            if raw.startswith(word):
                raw = raw[len(word):]
                ret.append(base64charset[i])
                flag = True
                break
        if not flag:
            raise ValueError(f"Unexpected token: {str[:10]}...")
    return ''.join(ret)


def text_to_otto64(text: str) -> str:
    """
    将文本转为OTTO64
    :param text: 原始文本
    :return: OTTO64
    """
    return base64_to_otto64(base64.b64encode(text.encode()).decode())


def otto64_to_text(text: str) -> str:
    """
    将OTTO64转为原始文本
    :param text: OTTO64
    :return: 文本
    """
    return base64.b64decode(otto64_to_base64(text)).decode()
