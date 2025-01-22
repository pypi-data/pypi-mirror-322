# -*- coding: utf-8 -*-
"""
Project Name: zyt_validation_utils
File Created: 2025.01.17
Author: ZhangYuetao
File Name: data_check.py
Update: 2025.01.22
"""


def is_all_of_type(target_type, *args):
    """
    检测所有数据是否都属于指定类型

    :param target_type: 目标类型（如 str, int, list 等）
    :param args: 不定数量的待检测数据
    :return: 如果所有数据都属于目标类型，返回 True；否则返回 False
    """
    result = all(isinstance(arg, target_type) for arg in args)
    return result


def is_all_unique(data):
    """
    判断列表或元组中是否有重复元素

    :param data: 列表或元组
    :return: 如果有重复元素，返回 True；否则返回 False
    """
    # 检查输入是否为列表或元组
    if not isinstance(data, (list, tuple)):
        raise TypeError("输入必须是列表或元组")

    seen = set()  # 用于存储已经见过的元素
    for item in data:
        if item in seen:  # 如果元素已经存在于集合中，说明有重复
            return False
        seen.add(item)  # 将当前元素添加到集合中
    return True  # 遍历完成后没有发现重复
