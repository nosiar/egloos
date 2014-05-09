#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from egloos import Egloos
import json

with open('auth', 'r') as f:
    line = f.readline().strip()

x = json.loads(line)

e = Egloos(x['user'], x['password'], x['nick'])
print(e.view_article(3459794))
