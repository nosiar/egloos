#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from egloos import Egloos
import json
import re

with open('auth', 'r') as f:
    line = f.readline().strip()

x = json.loads(line)

e = Egloos(x['user'], x['password'], x['nick'])
print(e.get_content(3459794))
print(e.view_article(3459794))
print(e.write_article("Diary", "하하", "호호"))
e.get_article_list("Diary", "헤헤", 1, re.I, True)
