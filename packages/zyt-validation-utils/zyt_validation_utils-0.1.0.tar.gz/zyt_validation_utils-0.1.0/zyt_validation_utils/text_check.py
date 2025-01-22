# -*- coding: utf-8 -*-
"""
Project Name: zyt_validation_utils
File Created: 2025.01.17
Author: ZhangYuetao
File Name: text_check.py
Update: 2025.01.22
"""


def is_have_chinese(text):
    """
    判断字符串是否含有中文字符。

    :param text: 输入的文本。
    :return: 如果含有中文返回 True，否则返回 False。
    """
    result = any('\u4e00' <= char <= '\u9fff' for char in text)
    return result


def is_all_chinese(text):
    """
    判断字符串是否全部由中文字符组成。

    :param text: 输入的文本。
    :return: 如果全部是中文返回 True，否则返回 False。
    """
    result = all('\u4e00' <= char <= '\u9fff' for char in text)
    return result


def is_have_english(text):
    """
    判断字符串是否含有英文字符。

    :param text: 输入的文本。
    :return: 如果含有英文字符返回 True，否则返回 False。
    """
    result = any('a' <= char.lower() <= 'z' for char in text)
    return result


def is_all_english(text):
    """
    判断字符串是否全部由英文字符组成。

    :param text: 输入的文本。
    :return: 如果全部是英文字符返回 True，否则返回 False。
    """
    result = all('a' <= char.lower() <= 'z' for char in text)
    return result


def is_have_digit(text):
    """
    判断字符串是否含有数字。

    :param text: 输入的文本。
    :return: 如果含有数字返回 True，否则返回 False。
    """
    result = any(char.isdigit() for char in text)
    return result


def is_all_digit(text):
    """
    判断字符串是否全部由数字组成。

    :param text: 输入的文本。
    :return: 如果全部是数字返回 True，否则返回 False。
    """
    result = all(char.isdigit() for char in text)
    return result


def is_have_special_char(text):
    """
    判断字符串是否含有特殊字符（非字母、非数字、非中文）。

    :param text: 输入的文本。
    :return: 如果含有特殊字符返回 True，否则返回 False。
    """
    result = any(not ('a' <= char.lower() <= 'z' or char.isdigit() or '\u4e00' <= char <= '\u9fff') for char in text)
    return result


def is_all_special_char(text):
    """
    判断字符串是否全部由特殊字符组成（非字母、非数字、非中文）。

    :param text: 输入的文本。
    :return: 如果全部是特殊字符返回 True，否则返回 False。
    """
    result = all(not ('a' <= char.lower() <= 'z' or char.isdigit() or '\u4e00' <= char <= '\u9fff') for char in text)
    return result


def is_have(text, check):
    """
    判断字符串中是否包含给定的字符或子字符串。

    :param text: 输入的文本。
    :param check: 需要检查的字符、子字符串或判断函数。
                 可以是单个字符、字符串、列表、集合或自定义函数。
    :return: 如果包含给定的字符或子字符串返回 True，否则返回 False。
    """
    if callable(check):
        # 如果 check 是一个函数，调用该函数进行判断
        result = any(check(char) for char in text)
        return result
    elif isinstance(check, (list, set)):
        # 如果 check 是列表或集合，检查是否包含其中任意一个字符
        result = any(char in check for char in text)
        return result
    else:
        # 如果 check 是单个字符或子字符串，直接检查是否包含
        result = str(check) in text
        return result
