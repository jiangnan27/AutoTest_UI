#! /usr/bin/python
# -*- coding:utf-8 -*-
import inspect
import os
import sys
import shutil

from config.PATH import BASE_PATH
from utils.my_logger import log


def get_module_name():
    """
    获取 模块名
    """
    # last=inspect.stack()[1]
    module_path = inspect.stack()[1][1]
    module_file = os.path.basename(module_path)
    # moduleName = moduleFile.split(".")[0]
    # print("last is:",last)
    # print("modulePath:",modulePath)
    # print("moduleFile:", moduleFile)
    return module_file


def get_method_name():
    """
    获取 函数名
    """
    return inspect.stack()[1][3]


def remove_dir(dir_path):
    """
    清空目录树
    """
    if not os.path.isdir(dir_path):
        return
    files = os.listdir(dir_path)
    try:
        for file in files:
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                remove_dir(file_path)
        os.rmdir(dir_path)
    except Exception as e:
        raise e


def rmdir_next_mkdir(dir_path):
    """
    清空旧目录树并新建空目录
    """
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)  # 可以删除一个目录树
            os.makedirs(dir_path)
        else:
            os.makedirs(dir_path)
    except Exception as e:
        raise e


def copy_to_dir(source_dir, target_dir):
    """
    复制一个文件夹（包括文件夹本身和旗下内容）到另一个文件夹下
    """
    try:
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        shutil.copytree(source_dir, os.path.join(target_dir, os.path.split(source_dir)[-1]))
    except Exception as e:
        raise e


def get_loop_filenames(dirname: str, loop_level: int = None) -> list:
    """递归获取某路径下所有文件名称
    :param dirname: 真实存在的路径
    :param loop_level: 递归多少层
    :return:
    """

    filenames = list()
    # 绝对路径
    if not os.path.isabs(dirname):
        dirname = os.path.abspath(dirname)

    for (pathname, dirs, files) in os.walk(dirname):
        if files:  # 文件,则添加进列表
            for f in files:
                filenames.append(f)
        if dirs:  # 目录,递归获取
            for dir_ in dirs:
                loop_level -= 1
                if loop_level is not None and loop_level >= 0:
                    get_loop_filenames(path_join(pathname, dir_), loop_level - 1)
                elif loop_level is not None and loop_level < 0:
                    return filenames
                else:
                    get_loop_filenames(path_join(pathname, dir_))
    return filenames


def get_filenames(dirname: str) -> list:
    """获取某路径下所有文件名称
    :param dirname: 真实存在的路径
    :return:
    """
    filenames = list()
    # 绝对路径
    if not os.path.isabs(dirname):
        dirname = os.path.abspath(dirname)

    for (pathname, dirs, files) in os.walk(dirname):
        if files:  # 文件,则添加进列表
            for f in files:
                filenames.append(f)
    return filenames


def get_loop_filepaths(dirname: str, loop_level: int = None) -> list:
    """获取某路径下所有文件
    :param dirname: 真实存在的路径
    :param loop_level: 要递归的层数
    :return:
    """
    filepaths = list()
    # 绝对路径
    if not os.path.isabs(dirname):
        dirname = os.path.abspath(dirname)

    for (pathname, dirs, files) in os.walk(dirname):
        if files:  # 文件,则添加进列表
            for f in files:
                filepaths.append(path_join(pathname, f))
        for dir_ in dirs:  # 目录,递归获取
            loop_level -= 1
            if loop_level is not None and loop_level >= 0:
                get_loop_filepaths(path_join(pathname, dir_), loop_level - 1)
            elif loop_level is not None and loop_level < 0:
                return filepaths
            else:
                get_loop_filepaths(path_join(pathname, dir_))
    return filepaths


def loop_search_dir(dirname: str, search_keyword: str, loop_level: int = None) -> list:
    """递归搜索文件夹
    :param dirname: 真实存在的路径
    :param loop_level: 要递归的层数
    :param search_keyword: 搜索关键字
    :return:
    """

    dir_list = list()

    # 绝对路径
    if not os.path.isabs(dirname):
        dirname = os.path.abspath(dirname)

    for (pathname, dirs, files) in os.walk(dirname):
        # 限定层级
        if loop_level is not None:
            loop_level -= 1
            if dirs and loop_level >= 0:  # 没到最后一层
                if search_keyword in dirs:
                    dir_list.append(path_join(pathname, search_keyword))
                else:
                    for dir_ in dirs:
                        loop_search_dir(path_join(pathname, dir_), search_keyword, loop_level)
            else:  # 到了最后一层
                return dir_list

        # 没限定层级
        else:
            for dir_ in dirs:
                if search_keyword in dir_:
                    dir_list.append(path_join(pathname, search_keyword))
                loop_search_dir(path_join(pathname, dir_), search_keyword, loop_level)

    return dir_list


def makedirs(dirname: str):
    """
    创建多级目录
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def path_join(base_path, *paths):
    """
    目录拼接
    :param base_path: 基础路径
    :param paths: 需要拼接的路径
    """
    if 'win' in sys.platform:
        return os.path.join(base_path, *paths).replace('/', '\\')
    else:
        return os.path.join(base_path, *paths).replace('\\', '/')


def touch_file(filepath, content=None, model='w', encoding='utf-8'):
    """
    新建文件
    """
    if not os.path.exists(filepath):
        makedirs(dir_name(filepath))
        with open(filepath, model, encoding=encoding) as f:
            if content:
                f.write(content)
    return filepath


def is_path_exits(path):
    """
    检测路径是否存在
    """
    if os.path.exists(path):
        return True
    else:
        return False


def is_path(path):
    """
    检测是不是目录
    """
    if is_path_exits(path):
        if os.path.isdir(path):
            return True
        else:
            return False


def is_file(path):
    """
    检测是不是文件
    """
    if is_path_exits(path):
        if os.path.isfile(path):
            return True
        else:
            return False


def is_abs(path):
    """
    检测是否是 绝对路径
    """
    return os.path.isabs(path)


def dir_name(path):
    """
    返回上级路径
    """
    return os.path.dirname(path)


def get_relpath(base_path, start=BASE_PATH):
    """
    获取相对路径
    """
    return os.path.relpath(base_path, start)


def get_abspath(base_path):
    """
    获取绝对路径
    """
    return os.path.abspath(base_path)


def set_os_environ(variables_mapping):
    """ set variables mapping to os.environ
    """
    for variable in variables_mapping:
        os.environ[variable] = variables_mapping[variable]
        log.debug("Set OS environment variable: {}".format(variable))
