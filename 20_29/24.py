
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 24.py

import re
from mymodule import extract_from_json

lines = extract_from_json(u"イギリス").split("\n")

for line in lines:
    file_line = re.search(u"(File|ファイル):(.*?)\|", line)
    if file_line is not None:
        print(file_line.group(2))
