#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:Download.py
@Date       :2022/08/11 22:02:49
@Author     :JohnserfSeed
@version    :1.0
@License    :(C)Copyright 2019-2022, Liugroup-NLPR-CASIA
@Github     :https://github.com/johnserf-seed
@Mail       :johnserfseed@gmail.com
-------------------------------------------------
Change Log  :
2022/08/11 22:02:49 : Init
2022/08/30 00:30:09 : Add ImageDownload()
-------------------------------------------------
'''

import Util


class Download():

    def __init__(self):
        self.urls = Util.Urls()

    def VideoDownload(self, profileData):
        self.headers = profileData.headers
        # 检查已经下载的作品
        self.check = Util.CheckInfo()
        self.like_counts = 0
        self.new_video_list = []
        # 生成1080p分辨率的视频链接
        self.uri_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&radio=1080p&line=0'
        # 视频原声
        self.music = profileData.music
        # 下载模式
        self.mode = profileData.mode
        # 下载路径
        self.path = profileData.path
        # 名称列表
        self.author_list = profileData.author_list
        # self.video_list = profileData.video_list
        # 作品uri列表
        # self.uri_list = profileData.uri_list
        # 作品播放地址列表
        self.url_list = profileData.url_list
        # 作品id列表
        self.aweme_id = profileData.aweme_id
        # 作者
        self.nickname = profileData.nickname
        # 页码
        self.max_cursor = profileData.max_cursor
        # 系统分隔符
        self.sprit = profileData.sprit
        # cxh230527:已下载列表
        self.nickname = profileData.nickname
        self.downloads = profileData.downloads

        # self.v_info = profileData.v_info
        # self.profile = Profile()
        with Util.progress:
            with Util.ThreadPoolExecutor(max_workers=5) as pool:
                for i in range(len(self.author_list)):
                    if i >= len(self.aweme_id):
                        print('[  🚩🚩  ]:数据异常：index=%d,data=%d' % (i, len(self.aweme_id)))
                        break
                    # 获取单部视频接口信息
                    try:
                        # 官方接口
                        # 旧接口22/12/23失效
                        # jx_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={self.aweme_id[i]}'
                        # 23/01/11
                        # 此ies domian暂时不需要xg参数
                        # 单作品接口 'aweme_detail'
                        # 主页作品 'aweme_list'
                        # 23/02/09 更新xg参数
                        jx_url = Util.Urls().POST_DETAIL + Util.XBogus(
                            f'aweme_id={self.aweme_id[i]}&aid=6383&cookie_enabled=true&platform=PC&downlink=10').params
                        js = Util.requests.get(
                            url=jx_url, headers=self.headers).text
                        # 防止接口多次返回空
                        while js == '':
                            js = Util.requests.get(
                                url=jx_url, headers=self.headers).text
                        js = Util.json.loads(js)
                        creat_time = Util.time.strftime(
                            "%Y-%m-%d %H.%M.%S", Util.time.localtime(js['aweme_detail']['create_time']))
                    except Exception as videoNotFound:
                        Util.log.warning(videoNotFound)
                        print('[  🚩🚩  ]:由于官方接口cdn缓存暂没过期，id:%s的视频已经不存在！\r' %
                              self.aweme_id[i])
                        Util.log.warning(
                            f'[  🚩🚩  ]: {self.nickname} 的视频 {self.aweme_id[i]} 下载失败')
                        continue

                    # Code From RobotJohns https://github.com/RobotJohns
                    # 移除文件名称  /r/n
                    self.author_list[i] = ''.join(
                        self.author_list[i].splitlines())
                    if len(self.author_list[i]) > 182:
                        print("[  提示  ]:", "文件名称太长 进行截取")
                        self.author_list[i] = self.author_list[i][0:180]
                        print("[  提示  ]:", "截取后的文案：{0}，长度：{1}".format(
                            self.author_list[i], len(self.author_list[i])))

                    # 检查视频下载情况
                    file_state, finish = self.check.test(
                        self.path, creat_time, self.author_list[i], ".mp4", profileData)
                    if file_state == True:
                        if 'finish' == finish:  # 当前的视频日期已经小于设定的开始时间，跳出
                            print('已经完成下载 1 ！')
                            return True
                        v_url = self.path + creat_time + '.mp4'
                        tag_names = [tag['tag_name'] for tag in js['aweme_detail']['video_tag']]
                        tag_name = ','.join(tag_names)
                        info = {
                            'author_user_id': js['aweme_detail']['author_user_id'],
                            'aweme_id': js['aweme_detail']['aweme_id'],
                            'desc': js['aweme_detail']['desc'],
                            'duration': js['aweme_detail']['duration'],
                            'create_time': js['aweme_detail']['create_time'],
                            'video_tag': tag_name,
                            'create_time2': creat_time,
                            'nickname': self.nickname,
                            'file': v_url,
                        }
                        self.downloads.append(info)
                        continue
                    else:
                        pass

                    # 尝试下载音频
                    try:
                        if self.music == "yes":
                            music_url = str(
                                js['aweme_detail']['music']['play_url']['url_list'][0])
                            music_title = str(
                                js['aweme_detail']['music']['author']) + '创作的视频原声'
                            m_url = self.path + self.sprit + creat_time + Util.re.sub(
                                r'[\\/:*?"<>|\r\n]+', "_", music_title) + '_' + self.author_list[i] + '.mp3'
                            if len(self.author_list[i]) > 20:
                                filename = creat_time[:10] + self.author_list[i][:20] + "..."
                            else:
                                filename = creat_time[:10] + self.author_list[i]
                            task_id = Util.progress.add_task(
                                "[  原声  ]:", filename=filename, start=False)
                            pool.submit(Util.copy_url, task_id,
                                        music_url, self.author_list[i], m_url)
                            Util.log.info(m_url)
                    except Exception as e:
                        Util.log.error(e)
                        print('[  ❌  ]:%s\r' % e)
                        print('\r[  警告  ]:下载音频出错!\r')
                        Util.log.error('[  ❌  ]:下载音频出错!')

                    # 尝试下载视频
                    try:
                        # 生成1080p视频链接
                        # self.new_video_list.append(
                        #     self.uri_url % self.uri_list[i])
                        # 2023/04/20 1080p不再通过拼接uri获取，url_list为1080p
                        self.new_video_list.append(self.url_list[i])
                        try:
                            v_url = self.path + creat_time + '.mp4'
                            if len(self.author_list[i]) > 20:
                                filename = creat_time[:10] + self.author_list[i][:20] + "..."
                            else:
                                filename = creat_time[:10] + self.author_list[i]
                            task_id = Util.progress.add_task(
                                "[  视频  ]:", filename=filename, start=False)
                            pool.submit(
                                Util.copy_url, task_id, self.new_video_list[0], self.author_list[i], v_url)

                            tag_names = [tag['tag_name'] for tag in js['aweme_detail']['video_tag']]
                            tag_name = ','.join(tag_names)
                            info = {
                                'author_user_id': js['aweme_detail']['author_user_id'],
                                'aweme_id': js['aweme_detail']['aweme_id'],
                                'desc': js['aweme_detail']['desc'],
                                'duration': js['aweme_detail']['duration'],
                                'create_time': js['aweme_detail']['create_time'],
                                'video_tag': tag_name,
                                'create_time2': creat_time,
                                'nickname': self.nickname,
                                'file': v_url,
                            }
                            self.downloads.append(info)
                            Util.log.info(v_url)
                            # 清除每个旧的视频列表
                            self.new_video_list = []
                        except Exception as videoError:
                            Util.log.error(videoError)
                            print('[  ❌  ]:%s\r' % videoError)
                            Util.log.error('[  警告  ]:下载视频出错!')
                            print('[  警告  ]:下载视频出错!')

                    except Exception as PageNoFull:
                        Util.log.error(PageNoFull)
                        print('[  ❌  ]:%s\r' % PageNoFull)
                        Util.log.error('[  提示  ]:该页视频资源没有35个,为你跳过该页！')
                        print('[  提示  ]:该页视频资源没有35个,为你跳过该页！\r')
                        break
        return False

    def ImageDownload(self, datas):
        with Util.progress:
            with Util.ThreadPoolExecutor(max_workers=5) as pool:
                for i in range(len(datas)):
                    self.nickname = datas[i][0]
                    self.desc = Util.replaceT(datas[i][1])
                    self.create_time = Util.time.strftime(
                        '%Y-%m-%d %H.%M.%S', Util.time.localtime(datas[i][2]))
                    self.position = datas[i][3]
                    self.number = datas[i][4]
                    self.images = datas[i][5]
                    self.sprit = Util.sprit

                    path = "Download" + self.sprit + "pic" + self.sprit + \
                           self.nickname + self.sprit + self.create_time + self.desc
                    # 检测下载目录是否存在
                    if not Util.os.path.exists(path):
                        Util.os.makedirs(path)

                    for i in range(self.number):
                        # 图片目录
                        p_url = 'Download' + self.sprit + 'pic' + self.sprit + self.nickname + self.sprit + \
                                self.create_time + self.desc + self.sprit + \
                                self.create_time + self.desc + \
                                '_' + str(i) + '.jpeg'
                        # 检查图片下载情况
                        if Util.os.path.exists(p_url):
                            continue
                        else:
                            pass
                        # 尝试下载图片
                        try:
                            if len(self.desc) > 25:
                                filename = self.create_time[:10] + self.desc[:25] + "..."
                            else:
                                filename = self.create_time[:10] + self.desc
                            task_id = Util.progress.add_task(
                                "[  原声  ]:", filename=filename, start=False)
                            pool.submit(Util.copy_url, task_id,
                                        self.images[i], self.desc, p_url)
                        except Exception as error:
                            print('[  错误  ]:%s\r' % error)
                            print('[  提示  ]:发生了点意外!\r')


if __name__ == '__main__':
    Download()
