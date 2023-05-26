# -*- coding: utf-8 -*-
"""
@Author  : Xhunmon 
@Time    : 2023/4/18 15:39
@FileName: __init__.py.py
@desc: 同级目录import pyCharm不识别，对module右击-->mark  Directory as-->Sources Root
"""
import os, sys

sys.path.append(os.path.dirname(__file__))