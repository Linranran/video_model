#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 9:38
# @Author  : linranran
# @Site    : 
# @File    : histogram_two_frame.py
# @Software: PyCharm

import os
import argparse
from matplotlib import pyplot
import seaborn
from tools import draw,get_img,hisogram_two_frame,abs_diff

def draw_abs_diff1(name):
    frames=get_img(name,args.frame_num)
    for i in range(len(frames)-1):
        difference_1 = []
        difference=hisogram_two_frame(frames[i],frames[i+1])
        for i in difference.keys():
            difference_1.append(difference[i])
        draw(difference_1,name)

def draw_abs_diff2(name):
    frames=get_img(name,args.frame_num)
    for i in range(len(frames)-1):
        diff = abs_diff(frames[i],frames[i+1])
        seaborn.heatmap(diff)
        pyplot.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='frame detect')
    parser.add_argument('-frame_num', '--frame_num', type=int, default='50')
    parser.add_argument('--sample_num', default=100, type=int)
    parser.add_argument('--data_path', default='E:\MEMC_CODE\hard_examples', type=str)#E:\MEMC_CODE\收集的视频     C:/Users/ranran/Videos/RECentral/     E:\BaiduYunDownload\MEMC片源(1)  E:\MEMC_CODE\dataset
    args = parser.parse_args()
    data=os.listdir(args.data_path)
    print(data)
    for i in range(len(data)):
        # draw_abs_diff1(os.path.join(args.data_path, data[i]))
        draw_abs_diff2(os.path.join(args.data_path, data[i]))