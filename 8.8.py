#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 16:20
# @Author  : linranran
# @Site    : 
# @File    : 8.8.py
# @Software: PyCharm



import os
import argparse
from tools import *
from get_data import *
from similars import *

def draw_one_video(name):
    frames = get_img(name, args.frame_num,img_type='gray',filter=None)
    if  '1' in args.method:
        hist = histogram(frames)
        similars1 = similar(hist)
        # draw_one(similars, name)
    if '2' in args.method:
        divide_frames=divide_imges(frames,args.block,args.block)
        hist=divide_histogram(divide_frames)
        similars2 = divide_difference(hist,args.block,args.block)
        # draw_one(similars, name)
    if '3' in args.method :
        img_hists1 = sample_hist(frames, args.sample_num)
        similars3 = similar(img_hists1,type='feng_difference')
        # draw_one(similars1, name)
    if '4' in args.method:
        img_hists1 ,similars4= sample_refresh_hist(frames, args.sample_num)
        # draw_one(similars1, name)
    draw_four(similars1,similars2,similars3,similars4,name)

    # similars=ssim(frames)
    # img_hists2,similars2 = sample_refresh_hist(frames, args.sample_num)
    # img_hists1 = sample_hist(frames, args.sample_num)
    # # img_hists = pixel_hist(frames)
    # similars1=similar(img_hists1)
    # img_hists2[0]=0
    # similars2 = similar(img_hists2)
    # similars2[0]=0
    # draw_one(similars2,name)
    # patterns1=pattern(similars1)
    # draw(patterns, name)
    # detect_patterns=detect_pattern(similars,args.FR)
    # print(detect_patterns)
    # draw(similars, name)
    # draw_two(similars1, similars2, name)
    # draw(patterns, name)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='frame detect')
    parser.add_argument('-frame_num', '--frame_num', type=int, default='120')
    parser.add_argument('--block', default=4, type=int, help="number of data loading workers (default: 4)")
    parser.add_argument('-frame_rate', '--FR', type=int, default='60')
    parser.add_argument('--sample_num', default=100, type=int)   #'C:/Users/ranran/Desktop/dataset'
    parser.add_argument('--method', default='1,2,3,4', type=str,help="which methods you want choose,they are 1:histogram 2:histogram+divide 3:sample_partical 4:resample_particla")
    parser.add_argument('--data_path', default='E:/MEMC_CODE/data/962a', type=str)#E:\MEMC_CODE\收集的视频     C:/Users/ranran/Videos/RECentral/     E:\BaiduYunDownload\MEMC片源(1)  E:\MEMC_CODE\dataset
    args = parser.parse_args()
    data=os.listdir(args.data_path)
    print(data)
    # draw_one_video('save.avi')
    # draw_one_video('E:/MEMC_CODE/data/848c/coco_2.mp4')C:\Users\ranran\Desktop\24FPS
    for i in range(len(data)):
        draw_one_video(os.path.join(args.data_path,data[i]))
        # draw_hotmap(os.path.join(args.data_path, data[i]), args.frame_num)
        # draw_abs_imgdiff(os.path.join(args.data_path, data[i]), args.frame_num)