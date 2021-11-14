#! /usr/bin/python
# -*- coding:utf-8 -*-
import json
from config.PATH import os


class JsonHandle:
    def __init__(self, json_file):
        if os.path.exists(json_file):
            self.json_file = json_file
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    def read_data(self):
        # 如果是第一次调用data，读取json文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self._data = json.load(f)  # load后是个generator，用list组织成列表
        return self._data

    def write_data(self, content):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    pass
