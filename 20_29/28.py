#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 28.py

import re
from mymodule import extract_from_json


def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str)
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    str = re.sub(r"\{{2}.+?\|.+?\|(.+?)\}{2}", r"\1 ", str)
    str = re.sub(r"<.*?>", r"", str)
    str = re.sub(r"\[.*?\]", r"", str)
    return str

temp_dict = {}
lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    temp_line = re.search("^\|(.*?)\s=\s(.*)", line)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

for k, v in sorted(temp_dict.items(), key=lambda x: x[0]):
    print(k, v)
