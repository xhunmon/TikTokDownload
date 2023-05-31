#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/27 09:02
@Author  : xhunmon
@Email   : xhunmon@126.com
@File    : Douyin.py
@Desc    : 
"""
import Util


def download_user(args):
    headers = Util.Cookies(args).dyheaders
    # 获取主页内容
    profile = Util.Profile(headers)
    # 使用参数并下载

    profile.getProfile(args)
    return profile.downloads
