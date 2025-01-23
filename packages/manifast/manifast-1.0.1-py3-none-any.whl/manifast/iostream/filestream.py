#!/usr/bin/env python
# coding=utf-8
'''
brief        :  
Author       : knightdby knightdby@163.com
Date         : 2023-02-24 16:57:43
FilePath     : /manifast/manifast/iostream/filestream.py
Description  : 
LastEditTime : 2023-08-15 15:16:19
LastEditors  : knightdby
Copyright (c) 2023 by Inc, All Rights Reserved.
'''

import os
import time
import json


def get_files(file_dir='', extention=['.jpg'], in_line=None, out_line=None):
    """
     description: 获取指定文件夹下的所有指定文件类型的文件，到List
     param       {*} file_dir  指定的迭代检索的文件夹
     param       {*} tail_name 迭代检测的文件类型
     return      {*} 包含所有文件绝对路径的list
    """
    if not isinstance(extention, list):
        extention = [extention]
    path_list = []
    if in_line:
        if out_line:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention) and (in_line in os.path.join(dirpath, filename)) and (out_line not in os.path.join(dirpath, filename)):
                        path_list.append(os.path.join(dirpath, filename))
        else:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention) and (in_line in os.path.join(dirpath, filename)):
                        path_list.append(os.path.join(dirpath, filename))
    else:
        if out_line:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention) and (out_line not in os.path.join(dirpath, filename)):
                        path_list.append(os.path.join(dirpath, filename))
        else:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention):
                        path_list.append(os.path.join(dirpath, filename))
    path_list = list(set(path_list))
    path_list = sorted(path_list)
    return path_list


def get_dirs(file_dir='', extention=['.jpg'], in_line=None, out_line=None):
    """
     description: 获取指定文件夹下的所有指定文件类型的文件，到List
     param       {*} file_dir  指定的迭代检索的文件夹
     param       {*} tail_name 迭代检测的文件类型
     return      {*} 包含所有文件绝对路径的list
    """
    if not isinstance(extention, list):
        extention = [extention]
    path_list = []
    if in_line:
        if out_line:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention) and (in_line in os.path.join(dirpath, filename)) and (out_line not in os.path.join(dirpath, filename)):
                        path_list.append(dirpath)
        else:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention) and (in_line in os.path.join(dirpath, filename)):
                        path_list.append(dirpath)
    else:
        if out_line:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention) and (out_line not in os.path.join(dirpath, filename)):
                        path_list.append(dirpath)
        else:
            for (dirpath, dirnames, filenames) in os.walk(file_dir):
                for filename in filenames:
                    if (os.path.splitext(filename)[1] in extention):
                        path_list.append(dirpath)
    path_list = list(set(path_list))
    path_list = sorted(path_list)
    return path_list


def make_path_dirs(path):
    if '.' in os.path.basename(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)


def write_dict2json(data={}, save_path='./results.json'):
    """
     description: 将data保存到指定的json文件下
     param       {*} data 
     param       {*} save_path
     return      {*}
    """
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def read_json_data(readPath):
    with open(readPath, "r", encoding='utf-8') as f:
        dict = json.load(f)
    return dict


def read_txt_data(txt_path):
    constants = []
    with open(txt_path, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            # p_tmp = [i for i in lines.split(' ')]
            constants.append(lines.strip('\n'))  # 添加新读取的数据
            # Efield.append(E_tmp)
            pass
    return constants


def write_list2txt(datas=[], save_path='./results.txt'):
    """
     description: 将data保存到指定的json文件下
     param       {*} data 
     param       {*} save_path
     return      {*}
    """
    with open(save_path, 'w') as f:
        pass
    for data in datas:
        if isinstance(data, int):
            with open(save_path, 'a') as f:
                f.write(str(data)+'\n')
        elif isinstance(data, str):
            with open(save_path, 'a') as f:
                f.write(str(data)+'\n')
        elif isinstance(data, list):
            for dt in data:
                with open(save_path, 'a') as f:
                    f.write(str(dt)+',')
            with open(save_path, 'a') as f:
                f.write('\n')
        elif isinstance(data, set):
            for dt in data:
                with open(save_path, 'a') as f:
                    f.write(str(dt)+',')
            with open(save_path, 'a') as f:
                f.write('\n')
        else:
            for dt in data:
                with open(save_path, 'a') as f:
                    f.write(str(dt)+',')
            with open(save_path, 'a') as f:
                f.write('\n')


def get_time():
    return time.strftime('%Y%m%d', time.localtime(time.time()))+time.strftime('_%H%M%S', time.localtime(time.time()))


def get_time_day():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_time_clock():
    return time.strftime('%H%M%S', time.localtime(time.time()))
