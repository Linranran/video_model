#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/24 10:26
# @Author  : linranran
# @Site    : 
# @File    : cancate_video.py
# @Software: PyCharm


#保存视频文件

import cv2
cap = cv2.VideoCapture('../data/962a/封神榜01_3.mp4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')#视频编码格式
fps =cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('save.avi',fourcc,fps,size)#第三个参数为帧率，第四个参数为每帧大小

for i in range(200):
    ret,frame = cap.read()
    if(ret):
        cv2.imshow('input',frame)
        out.write(frame)
    else:
        break
    if(cv2.waitKey(1)==27):
        break
cap = cv2.VideoCapture('../data/962a/喜剧之王_20190103_新版_656_352_3.mp4')
for i in range(400):
    ret,frame = cap.read()
    if(ret):
        cv2.imshow('input',frame)
        out.write(frame)
    else:
        break
    if(cv2.waitKey(1)==27):
        break
cap.release()
out.release()
cv2.destroyAllWindows()


# vc = cv2.VideoCapture('/data/962a/封神榜01_3.mp4')  # 读入视频文件，命名cv
# n = 1  # 计数
#
# if vc.isOpened():  # 判断是否正常打开
#     rval, frame = vc.read()
# else:
#     rval = False
#
#
# i = 0
# for i in range(100):  # 循环读取视频帧
#     rval, frame = vc.read()
#     cv2.imwrite('framesplit/{}.jpg'.format(i), frame)  # 存储为图像
#     cv2.waitKey(1)
# vc.release()