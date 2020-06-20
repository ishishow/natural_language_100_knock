#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 26.py

import re
from mymodule import extract_from_json

temp_dict = {}
lines = re.split(r"\n[\|}]", extract_from_json(u"イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = re.sub(r"'{2,5}", r"", temp_line.group(2))

# 25.py と同様 Python3 参照
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)
