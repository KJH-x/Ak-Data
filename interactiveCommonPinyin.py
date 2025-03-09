from copy import deepcopy
from typing import List

import pyperclip
from pypinyin import Style, load_phrases_dict, pinyin
from pypinyin_dict.pinyin_data import cc_cedict, kxhc1983

# kxhc1983.load()
cc_cedict.load()
custom_dict: dict[str, List[List[str]]] = {
    # 浊心斯卡蒂、涤火杰西卡、芙兰卡、卡缇、卡夫卡、杰西卡、斯卡蒂、泡普卡、卡达、布洛卡、阿斯卡纶、卡涅利安
    u'卡': [[u'kǎ']],
    # 阿米娅、阿米娅(近卫)、阿米娅(医疗)、阿、阿消、阿斯卡纶、阿罗玛
    u'阿': [[u'ā']],
    # 纯烬艾雅法拉、艾丝黛尔、艾雅法拉、艾丽妮、苦艾、艾拉
    u'艾': [[u'ài']],
    # 维娜·维多利亚、安洁莉娜、贝娜、薇薇安娜、娜仁图亚
    u'娜': [[u'nà']],
    # 火龙S黑角、角峰、号角、黑角
    u'角': [[u'jiǎo']],
    # 早露、露托、玛露西尔
    u'露': [[u'lù']],
    # 暴行、见行者、行箸
    u'行': [[u'xíng']],
    # 深海色、九色鹿
    u'色': [[u'sè']],
    # 提丰、莫斯提马
    u'提': [[u'tí']],
    # 雷蛇、蛇屠箱
    u'蛇': [[u'shé']],
    # 铅踝、钼铅
    u'铅': [[u'qiān']],

    u'百': [[u'bǎi']],
    u'吽': [[u'hōng']],
    u'红': [[u'hóng']],
    u'亚叶': [[u'yà'], [u'yè']],
    u'薄绿': [[u'bó'], [u'lù']],
    u'谜图': [[u'mí'], [u'tú']],
    u'波卜': [[u'bō'], [u'bo']],
    u'嵯峨': [[u'cuó'], [u'é']],
    u'焰尾': [[u'yàn'], [u'wěi']],
    u'伺夜': [[u'sì'], [u'yè']],
    u'摩根': [[u'mó'], [u'gēn']],
    u'暮落': [[u'mù'], [u'luò']],
    u'末药': [[u'mò'], [u'yào']],
    u'左乐': [[u'zuǒ'], [u'lè']],
    u'贾维': [[u'jiǎ'], [u'wéi']],
    u'地灵': [[u'dì'], [u'líng']],
    u'柏喙': [[u'bǎi'], [u'huì']],
    u'仇白': [[u'qiú'], [u'bái']],
    u'空爆': [[u'kōng'], [u'bào']],
    u'澄闪': [[u'chéng'], [u'shǎn']],
    u'刻俄柏': [[u'kè'], [u'é'], [u'bó']],
    u'车尔尼': [[u'chē'], [u'ěr'], [u'nǐ']],
    u'塞雷娅': [[u'sài'], [u'léi'], [u'yà']],
    u'玫兰莎': [[u'méi'], [u'lán'], [u'shā']],
    u'龙舌兰': [[u'lóng'], [u'shé'], [u'lán']],
    u'见行者': [[u'jiàn'], [u'xíng'], [u'zhě']],
    u'史都华德': [[u'shǐ'], [u'dū'], [u'huá'], [u'dé']],
    u'齐尔查克': [[u'qí'], [u'ěr'], [u'chá'], [u'kè']],
    u'维什戴尔': [[u'wéi'], [u'shí'], [u'dài'], [u'ěr']],
}
# {u"阿爸": [[u"ā"], [u"bà"]]}

load_phrases_dict(custom_dict, style='default')
input("准备好读取剪贴板，回车以继续")
clipboard_content = pyperclip.paste().splitlines()
# clipboard_pinyin: List[str] = []
# clipboard_py: List[str] = []
clipboard_output: List[str] = []


def pinyin_combination(line, heteronym: bool, strict: bool, style: Style) -> List[str]:
    pys: List[str] = [""]
    parse = pinyin(line, strict=strict, heteronym=heteronym, style=style)
    for py in parse:
        next_py: List[str] = []
        for base in pys:
            next_py = [f"{base}{heteronym}" for heteronym in py]
        pys = deepcopy(next_py)
    return pys


for line in clipboard_content:
    # First_letter
    pinyins = pinyin_combination(line, heteronym=True, strict=False, style=Style.NORMAL)
    # clipboard_py.append("/".join(pys))

    pys = pinyin_combination(line, heteronym=True, strict=False, style=Style.FIRST_LETTER)
    # clipboard_pinyin.append("".join(pys))
    clipboard_output.append(f"{line},{"/".join(pinyins)},{"/".join(pys)}")

pyperclip.copy("\n".join(clipboard_output))
