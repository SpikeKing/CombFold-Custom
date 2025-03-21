#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/7/9

常用方法
"""


import collections
import io
import os
import random
import shutil
import sys
import time
from datetime import timedelta, datetime
from io import open
from itertools import chain

import numpy as np
import pandas as pd

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if p not in sys.path:
    sys.path.append(p)

import glob
import json
import os
import re
import operator

FORMAT_DATE = '%Y%m%d'
FORMAT_DATE_2 = '%Y-%m-%d'
FORMAT_DATE_3 = '%Y%m%d%H%M%S'


def traverse_dir_files(root_dir, ext="", is_sorted=True):
    """
    列出文件夹中的文件, 深度遍历
    :param root_dir: 根目录
    :param ext: 后缀名
    :param is_sorted: 是否排序，耗时较长
    :return: 文件路径列表
    """
    paths_list = []
    for parent, _, fileNames in os.walk(root_dir):
        for name in fileNames:
            if name.startswith('.'):  # 去除隐藏文件
                continue
            if ext:  # 根据后缀名搜索
                if name.endswith(ext):
                    paths_list.append(os.path.join(parent, name))
            else:
                paths_list.append(os.path.join(parent, name))
    if is_sorted and paths_list:
        paths_list = sorted(paths_list)
    return paths_list


def traverse_dir_folders(root_dir, is_sorted=True):
    """
    列出文件夹中的文件, 深度遍历
    :param root_dir: 根目录
    :param is_sorted: 是否排序，耗时较长
    :return: 文件路径列表
    """
    paths_list = []
    for parent, _, fileNames in os.walk(root_dir):
        # 判断文件夹是否相同
        if os.path.samefile(parent, root_dir):
            continue
        paths_list.append(parent)
    if is_sorted and paths_list:
        paths_list = sorted(paths_list)
    return paths_list


def traverse_dir_files_for_large(root_dir, ext="", count=-1):
    """
    列出文件夹中的文件, 深度遍历
    :param root_dir: 根目录
    :param ext: 后缀名
    :param count: 终止遍历数量
    :return: 文件路径列表
    """
    paths_list = []
    dir_list = list()
    dir_list.append(root_dir)
    print_count = 0
    while len(dir_list) != 0:
        dir_path = dir_list.pop(0)
        dir_name = os.path.basename(dir_path)
        for i in os.scandir(dir_path):
            print_count += 1
            if print_count % 10000 == 0:
                print(f"[Info] traverse_dir: {dir_name}, num {print_count}")
            path = i.path
            if path.startswith('.'):  # 去除隐藏文件
                continue
            if os.path.isdir(path):
                dir_list.append(path)
            else:
                if ext:  # 根据后缀名搜索
                    if path.endswith(ext):
                        paths_list.append(path)
                else:
                    paths_list.append(path)
        if 0 < count < print_count:
            break
    return paths_list

def check_np_empty(data_np):
    """
    检测Numpy是空或者None
    """
    none_type = type(None)
    if isinstance(data_np, np.ndarray):
        if data_np.size == 0:
            return True
    elif isinstance(data_np, none_type):
        return True
    elif isinstance(data_np, list):
        if not data_np:
            return True
    else:
        return False


def sort_two_list(list1, list2, reverse=False):
    """
    排序两个列表
    :param list1: 列表1
    :param list2: 列表2
    :param reverse: 逆序
    :return: 排序后的两个列表
    """
    try:
        list1, list2 = (list(t) for t in zip(*sorted(zip(list1, list2), reverse=reverse)))
    except Exception as e:
        sorted_id = sorted(range(len(list1)), key=lambda k: list1[k], reverse=True)
        list1 = [list1[i] for i in sorted_id]
        list2 = [list2[i] for i in sorted_id]

    return list1, list2


def sort_three_list(list1, list2, list3, reverse=False):
    """
    排序两个列表
    :param list1: 列表1
    :param list2: 列表2
    :param list3: 列表3
    :param reverse: 逆序
    :return: 排序后的两个列表
    """
    list1, list2, list3 = (list(t) for t in zip(*sorted(zip(list1, list2, list3), reverse=reverse)))
    return list1, list2, list3


def mkdir_if_not_exist(dir_name, is_delete=False):
    """
    创建文件夹
    :param dir_name: 文件夹
    :param is_delete: 是否删除
    :return: 是否成功
    """
    try:
        if is_delete:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return True
    except Exception as e:
        return False


def datetime_to_str(date, date_format=FORMAT_DATE):
    return date.strftime(date_format)


def str_to_datetime(date_str, date_format=FORMAT_DATE):
    date = time.strptime(date_str, date_format)
    return datetime(*date[:6])


def get_next_half_year():
    """
    当前时间的半年前
    :return: 半年时间
    """
    n_days = datetime.now() - timedelta(days=178)
    return n_days.strftime('%Y-%m-%d')


def timestr_2_timestamp(time_str):
    """
    时间字符串转换为毫秒
    :param time_str: 时间字符串, 2017-10-11
    :return: 毫秒, 如1443715200000
    """
    return int(time.mktime(datetime.strptime(time_str, "%Y-%m-%d").timetuple()) * 1000)


def create_folder(atp_out_dir):
    """
    创建文件夹
    :param atp_out_dir: 文件夹
    :return:
    """
    if os.path.exists(atp_out_dir):
        shutil.rmtree(atp_out_dir)
        print('文件夹 "%s" 存在，删除文件夹。' % atp_out_dir)

    if not os.path.exists(atp_out_dir):
        os.makedirs(atp_out_dir)
        print('文件夹 "%s" 不存在，创建文件夹。' % atp_out_dir)


def create_empty_file(file_name, is_delete=True):
    """
    创建文件
    :param file_name: 文件名
    :param is_delete: 是否删除
    :return: None
    """
    if os.path.exists(file_name) and is_delete:
        # print(f"[Warning] 文件存在，删除文件! {file_name}")
        os.remove(file_name)  # 删除已有文件
    if not os.path.exists(file_name):
        # print("文件不存在，创建文件：%s" % file_name)
        open(file_name, 'a').close()


def remove_punctuation(line):
    """
    去除所有半角全角符号，只留字母、数字、中文
    :param line:
    :return:
    """
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


def check_punctuation(word):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    if pattern.search(word):
        return True
    else:
        return False


def clean_text(text):
    """
    text = "hello      world  nice ok    done \n\n\n hhade\t\rjdla"
    result = hello world nice ok done hhade jdla
    将多个空格换成一个
    :param text:
    :return:
    """
    if not text:
        return ''
    return re.sub(r"\s+", " ", text)


def merge_files(folder, merge_file):
    """
    将多个文件合并为一个文件
    :param folder: 文件夹
    :param merge_file: 合并后的文件
    :return:
    """
    paths, _, _ = listdir_files(folder)
    with open(merge_file, 'w') as outfile:
        for file_path in paths:
            with open(file_path) as infile:
                for line in infile:
                    outfile.write(line)


def random_pick(some_list, probabilities=None):
    """
    根据概率随机获取元素
    :param some_list: 元素列表
    :param probabilities: 概率列表
    :return: 当前元素
    """
    if not probabilities:
        probabilities = [float(1) / float(len(some_list))] * len(some_list)

    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    item = some_list[0]
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


def intersection_of_lists(l1, l2):
    """
    两个list的交集
    :param l1:
    :param l2:
    :return:
    """
    return list(set(l1).intersection(set(l2)))


def safe_div(x, y):
    """
    安全除法
    :param x: 分子
    :param y: 分母
    :return: 除法
    """
    x = float(x)
    y = float(y)
    if y == 0.0:
        return 0.0
    r = x / y
    return r


def calculate_percent(x, y):
    """
    计算百分比
    :param x: 分子
    :param y: 分母
    :return: 百分比
    """
    x = float(x)
    y = float(y)
    return safe_div(x, y) * 100


def invert_dict(d):
    """
    当字典的元素不重复时, 反转字典
    :param d: 字典
    :return: 反转后的字典
    """
    return dict((v, k) for k, v in d.items())


def init_num_dict():
    """
    初始化值是int的字典
    :return:
    """
    return collections.defaultdict(int)


def sort_dict_by_value(dict_, reverse=True):
    """
    按照values排序字典
    :param dict_: 待排序字典
    :param reverse: 默认从大到小
    :return: 排序后的字典
    """
    return sorted(dict_.items(), key=operator.itemgetter(1), reverse=reverse)


def sort_dict_by_key(dict_, reverse=False):
    """
    按照values排序字典
    :param dict_: 待排序字典
    :param reverse: 默认从大到小
    :return: 排序后的字典
    """
    return sorted(dict_.items(), key=operator.itemgetter(0), reverse=reverse)


def get_current_time_str():
    """
    输入当天的日期格式, 20170718_1137
    :return: 20170718_1137
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_current_time_for_show():
    """
    输入当天的日期格式, 20170718_1137
    :return: 20170718_1137
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_current_day_str():
    """
    输入当天的日期格式, 20170718
    :return: 20170718
    """
    return datetime.now().strftime('%Y%m%d')


def remove_line_of_file(ex_line, file_name):
    ex_line = ex_line.replace('\n', '')
    lines = read_file(file_name)

    out_file = open(file_name, "w")
    for line in lines:
        line = line.replace('\n', '')  # 确认编码格式
        if line != ex_line:
            out_file.write(line + '\n')
    out_file.close()


def map_to_ordered_list(data_dict, reverse=True):
    """
    将字段根据Key的值转换为有序列表
    :param data_dict: 字典
    :param reverse: 默认从大到小
    :return: 有序列表
    """
    return sorted(data_dict.items(), key=operator.itemgetter(1), reverse=reverse)


def map_to_index(data_list, all_list):
    """
    转换为one-hot形式
    :param data_list:
    :param all_list:
    :return:
    """
    index_dict = {l.strip(): i for i, l in enumerate(all_list)}  # 字典
    index = index_dict[data_list.strip()]
    return index


def n_lines_of_file(file_name):
    """
    获取文件行数
    :param file_name: 文件名
    :return: 数量
    """
    return sum(1 for line in open(file_name))


def remove_file(file_name):
    """
    删除文件
    :param file_name: 文件名
    :return: 删除文件
    """
    if os.path.exists(file_name):
        os.remove(file_name)


def find_sub_in_str(string, sub_str):
    """
    子字符串的起始位置
    :param string: 字符串
    :param sub_str: 子字符串
    :return: 当前字符串
    """
    return [m.start() for m in re.finditer(sub_str, string)]


def list_has_sub_str(string_list, sub_str):
    """
    字符串是否在子字符串中
    :param string_list: 字符串列表
    :param sub_str: 子字符串列表
    :return: 是否在其中
    """
    for string in string_list:
        if sub_str in string:
            return True
    return False


def remove_last_char(str_value, num):
    """
    删除最后的字符串
    :param str_value: 字符串
    :param num: 删除位置
    :return: 新的字符串
    """
    str_list = list(str_value)
    return "".join(str_list[:(-1 * num)])


def read_file(data_file, mode='more'):
    """
    读文件, 原文件和数据文件
    :return: 单行或数组
    """
    try:
        with open(data_file, 'r', errors='ignore') as f:
            if mode == 'one':
                output = f.read()
                return output
            elif mode == 'more':
                output = f.readlines()
                output = [o.strip() for o in output]
                return output
            else:
                return list()
    except IOError:
        return list()


def is_file_nonempty(data_file):
    """
    判断文件是否非空
    """
    data_lines = read_file(data_file)
    if len(data_lines) > 0:
        return True
    else:
        return False


def read_csv_file(data_file, num=-1):
    """
    读取CSV文件
    """
    import pandas
    df = pandas.read_csv(data_file)
    row_list = []
    column_names = list(df.columns)
    for idx, row in df.iterrows():
        if idx == num:
            break
        row_list.append(dict(row))
        if idx != 0 and idx % 20000 == 0:
            print('[Info] idx: {}'.format(idx))
    return column_names, row_list


def read_file_utf8(data_file, mode='more', encoding='utf8'):
    """
    读文件, 原文件和数据文件
    :return: 单行或数组
    """
    try:
        with open(data_file, 'r', encoding=encoding) as f:
            if mode == 'one':
                output = f.read()
                return output
            elif mode == 'more':
                output = f.readlines()
                output = [o.strip() for o in output]
                return output
            else:
                return list()
    except IOError:
        return list()


def read_file_gb2312(data_file, mode='more'):
    """
    读文件, 原文件和数据文件
    :return: 单行或数组
    """
    try:
        with open(data_file, 'r', encoding='gb2312') as f:
            if mode == 'one':
                output = f.read()
                return output
            elif mode == 'more':
                output = f.readlines()
                output = [o.strip() for o in output]
                return output
            else:
                return list()
    except IOError:
        return list()


def read_excel_to_df(file_path):
    """
    读取excel文件
    pip install openpyxl
    """
    df = pd.read_excel(file_path, engine='openpyxl')
    return df


def find_word_position(original, word):
    """
    查询字符串的位置
    :param original: 原始字符串
    :param word: 单词
    :return: [起始位置, 终止位置]
    """
    u_original = original.decode('utf-8')
    u_word = word.decode('utf-8')
    start_indexes = find_sub_in_str(u_original, u_word)
    end_indexes = [x + len(u_word) - 1 for x in start_indexes]
    return zip(start_indexes, end_indexes)


def write_list_to_file(file_name, data_list, log=False):
    """
    将列表写入文件
    :param file_name: 文件名
    :param data_list: 数据列表
    :param log: 日志
    :return: None
    """
    if file_name == "":
        return
    with io.open(file_name, "a+", encoding='utf8') as fs:
        count = 0
        for data in data_list:
            fs.write("%s\n" % data)
            count += 1
            if count % 100 == 0 and log:
                print('[Info] write: {} lines'.format(count))
    if log:
        print('[Info] final write: {} lines'.format(count))


def write_line(file_name, line):
    """
    将行数据写入文件
    :param file_name: 文件名
    :param line: 行数据
    :return: None
    """
    if file_name == "":
        return
    with io.open(file_name, "a", encoding='utf8') as fs:
        if type(line) is (tuple or list):
            fs.write("%s\n" % ", ".join(line))
        else:
            fs.write("%s\n" % line)


def show_set(data_set):
    """
    显示集合数据
    :param data_set: 数据集
    :return: None
    """
    data_list = list(data_set)
    show_string(data_list)


def show_string(obj):
    """
    用于显示UTF-8字符串, 尤其是含有中文的.
    :param obj: 输入对象, 可以是列表或字典
    :return: None
    """
    print(list_2_utf8(obj))


def list_2_utf8(obj):
    """
    用于显示list汉字
    :param obj:
    :return:
    """
    return json.dumps(obj, encoding="UTF-8", ensure_ascii=False)


def listdir_no_hidden(root_dir):
    """
    显示顶层文件夹
    :param root_dir: 根目录
    :return: 文件夹列表
    """
    return glob.glob(os.path.join(root_dir, '*'))


def listdir_files(root_dir, ext=None):
    """
    列出文件夹中的文件
    :param root_dir: 根目录
    :param ext: 类型
    :return: [文件路径(相对路径), 文件夹名称, 文件名称]
    """
    names_list = []
    paths_list = []
    for parent, _, fileNames in os.walk(root_dir):
        for name in fileNames:
            if name.startswith('.'):
                continue
            if ext:
                if name.endswith(tuple(ext)):
                    names_list.append(name)
                    paths_list.append(os.path.join(parent, name))
            else:
                names_list.append(name)
                paths_list.append(os.path.join(parent, name))
    return paths_list, names_list


def time_elapsed(start, end):
    """
    输出时间
    :param start: 开始
    :param end: 结束
    :return:
    """
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.6f}".format(int(hours), int(minutes), seconds)


def batch(iterable, n=1):
    """
    批次迭代器
    :param iterable: 迭代器
    :param n: 次数
    :return:
    """
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def unicode_str(s):
    """
    将字符串转换为unicode
    :param s: 字符串
    :return: unicode字符串
    """
    try:
        s = str(s, 'utf-8')
    except Exception as e:
        try:
            s = s.decode('utf8')
        except Exception as e:
            pass
        s = s
    return s


def unfold_nested_list(data_list):
    """
    展开嵌套的list
    :param data_list: 数据list
    :return: 展开list
    """
    return list(chain.from_iterable(data_list))


def unicode_list(data_list):
    """
    将list转换为unicode list
    :param data_list: 数量列表
    :return: unicode列表
    """
    return [unicode_str(s) for s in data_list]


def pairwise_list(a_list):
    """
    list转换为成对list
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."

    :param a_list: list
    :return: 成对list
    """
    if len(a_list) % 2 != 0:
        raise Exception("pairwise_list error!")
    r_list = []
    for i in range(0, len(a_list) - 1, 2):
        r_list.append([a_list[i], a_list[i + 1]])
    return r_list


def list_2_numdict(a_list):
    """
    list转换为num字典
    """
    num_dict = collections.defaultdict(int)
    for item in a_list:
        num_dict[item] += 1
    return num_dict


def shuffle_two_list(a, b):
    """
    shuffle两个列表
    """
    c = list(zip(a, b))
    random.shuffle(c)
    a, b = zip(*c)
    return a, b


def shuffle_three_list(a, b, c):
    """
    shuffle三个列表
    """
    d = list(zip(a, b, c))
    random.shuffle(d)
    a, b, c = zip(*d)
    return a, b, c


def sorted_index(myList, reverse=True):
    """
    从大到小排序，输出index
    myList = [1, 2, 3, 100, 5]
    output = [3, 4, 2, 1, 0]
    :return:
    """

    idx_list = sorted(range(len(myList)), key=myList.__getitem__, reverse=reverse)
    return idx_list


def download_url_img(url):
    """
    下载url图像
    """
    import cv2
    import requests
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.get(url, verify=False)
    except Exception as e:
        print(str(e))
        return False, []
    if response is not None and response.status_code == 200:
        input_image_data = response.content
        np_arr = np.asarray(bytearray(input_image_data), np.uint8).reshape(1, -1)
        parsed_image = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
        return True, parsed_image


def download_url_txt(url, is_split=False):
    """
    下载txt文本
    """
    import requests

    try:
        response = requests.get(url, timeout=3)
    except Exception as e:
        print(str(e))
        return False, []
    # with open(file_name, "wb") as code:
    #     code.write(down_res.content)
    if response is not None and response.status_code == 200:
        text_data = response.content
        if not is_split:
            return True, text_data.decode()
        else:
            text_list = text_data.decode().splitlines()
            return True, text_list
    else:
        return False, []



def save_dict_to_json(json_path, save_dict):
    """
    将字典保存成JSON文件
    """
    json_str = json.dumps(save_dict, indent=2, ensure_ascii=False)
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


def read_json(json_path):
    """
    读取JSON
    """
    import json
    json_path = json_path
    try:
        with open(json_path, 'r', encoding='utf-8') as load_f:
            res = json.load(load_f)
    except Exception as e:
        print(e)
        res = {}
    return res


def save_obj(file_path, obj):
    """
    存储obj
    """
    import pickle
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)


def load_obj(file_path):
    """
    加载obj
    """
    import pickle
    with open(file_path, 'rb') as f:
        x = pickle.load(f)
    return x


def write_list_to_excel(file_name, titles, res_list):
    """
    存储excel

    :param file_name: 文件名
    :param titles: title
    :param res_list: 数据
    :return: None
    """
    import xlsxwriter

    wk = xlsxwriter.Workbook(file_name)
    ws = wk.add_worksheet()

    for i, t in enumerate(titles):
        ws.write(0, i, t)

    for n_rows, res in enumerate(res_list):
        n_rows += 1
        try:
            for idx in range(len(titles)):
                ws.write(n_rows, idx, res[idx])
        except Exception as e:
            print(e)
            continue

    wk.close()
    print('[Info] 文件保存完成: {}'.format(file_name))


def random_prob(prob):
    """
    随机生成真值
    """
    x = random.choices([True, False], [prob, 1-prob])
    return x[0]


def filter_list_by_idxes(data_list, idx_list):
    """
    通过索引过滤list, 兼容1~2层list
    """
    res_list = []
    for idx in idx_list:
        if not isinstance(idx, list):
            res_list.append(data_list[idx])
        else:
            sub_list = []
            for i in idx:
                sub_list.append(data_list[i])
            res_list.append(sub_list)
    return res_list


def check_english_str(string):
    """
    检测英文字符串
    """
    pattern = re.compile('^[A-Za-z0-9.,:;!?()_*"\'，。 ]+$')
    if pattern.fullmatch(string):
        return True
    else:
        return False


def get_fixed_samples(a_list, num=20000):
    """
    固定数量的样本
    """
    if num <= 0:
        return a_list
    a_n = len(a_list)
    n_piece = num // a_n + 1
    x_list = a_list * n_piece
    random.seed(47)
    random.shuffle(x_list)
    x_list = x_list[:num]
    return x_list


def split_train_and_val(data_lines, gap=20):
    """
    分离数据集为训练和验证
    """
    print('[Info] 样本总数: {}'.format(len(data_lines)))
    random.seed(47)
    random.shuffle(data_lines)
    train_num = len(data_lines) // gap * (gap - 1)
    train_data = data_lines[:train_num]
    val_data = data_lines[train_num:]
    print('[Info] train: {}, val: {}'.format(len(train_data), len(val_data)))
    return train_data, val_data
