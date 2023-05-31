#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:Check.py
@Date       :2022/08/16 18:34:27
@Author     :JohnserfSeed
@version    :1.0
@License    :(C)Copyright 2019-2022, Liugroup-NLPR-CASIA
@Github     :https://github.com/johnserf-seed
@Mail       :johnserfseed@gmail.com
-------------------------------------------------
Change Log  :
2022/08/16 18:34:27 : Init
-------------------------------------------------
'''

import Util


class CheckInfo():

    def __init__(self):
        pass

    # 检测视频是否已经下载过
    def test(self, path, creat_time, file_name, file_type, profileData):
        if '|' in profileData.interval:
            in_time = profileData.interval.split('|')
            date_format = "%Y-%m-%d %H.%M.%S"
            start_data = Util.time.strptime(in_time[0], date_format)
            end_data = Util.time.strptime(in_time[1], date_format)
            creat_date = Util.time.strptime(creat_time, date_format)
            if creat_date < start_data:
                print("[  提示  ]:", "目标视频时间：{0}，小于设置初始时间：{1} 结束下载。".format(creat_time, in_time[0]))
                return True, 'finish'
            elif creat_date > end_data:
                print("[  提示  ]:", "目标视频时间：{0}，大于设置初始时间：{1} 跳过下载。".format(creat_time, in_time[1]))
                return True, 'continue'
        return Util.os.path.exists(path + creat_time + file_name + file_type), ''


if __name__ == '__main__':
    CheckInfo()
