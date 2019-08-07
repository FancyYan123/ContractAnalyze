# -*- coding=utf-8 -*-
from PIL import Image
import base64
import re
import math

def get_image_base64():
    path = 'C:\\tmp\\test.jpg'
    im = Image.open(path)
    size = im.height, im.width
#    if im.height > 2000:
#        size = 2000, 2000 * (im.width / im.height)
    im.thumbnail(size)
    im.save(path)

    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
    return base64_data


def text_splitter(text: str, data_type):
    """
    :param text: 需要切分的文字片段
    :param data_type: 文字片段的来源，可能是纯文本，可能是从图片中提取出来的
    :return: 返回切分后的文本list
    """
    if data_type == 'image':
        text = re.split(r'。|；|;|\?', text)
    else:
        text = re.split(r'\n|。|；|;|\?', text)
    text = list(map(lambda s: s.replace('\n', '').replace(' ',  ''), text))
    text = list(filter(lambda x: x != '', text))
    return text


def find_closest_substr(whole_str:str, target:str, sub_strs:list):
    """
    在字符串中找到与target字符串距离最近的sub_strs元素
    :param whole_str: 字符串整体
    :param target: 目标
    :param sub_strs: 其他子串
    :return: 返回sub_strs中距离target最近的字符串
    """
    if len(sub_strs) == 1:
        return sub_strs[0]
    target_index = whole_str.find(target)
    distance = [math.fabs(target_index-whole_str.find(each)) for each in sub_strs]
    return sub_strs[distance.index(min(distance))]
