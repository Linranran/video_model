#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 17:48
# @Author  : linranran
# @Site    : 
# @File    : 8.22.py
# @Software: PyCharm
import os
import subprocess
import argparse
import cv2
import numpy as np
from tools import draw_one,get_img,feng_difference,pattern,sample_hist,pixel_hist,sample_refresh_hist,ssim,detect_pattern,scene_change,re_detect_pattern

def similar(img_hist):
    results=[]
    for i in range(len(img_hist) - 1):
        result=feng_difference(img_hist[i], img_hist[i + 1])
        results.append(result)
    return results

def draw_one_video(name):
    cap = cv2.VideoCapture(name)
    print('get the video ',name)
    video_len=cap.get(7)
    frame_mum=0
    lock_patterns = False
    ret=True
    while (ret):
        frames = []
        for i in range(args.frame_num):
            ret, frame = cap.read()
            if ret:
                frame_mum+=1
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            else:
                break
        if  not ret:
            break
        img_hists = sample_hist(frames, args.sample_num)
        similars = similar(img_hists)
        scene = scene_change(similars)
        if scene:
            print('detect scene change')
            draw_one(similars,'test')
            # subprocess.call("pause", shell=True)
            # os.system("pause")
            # cap = cv2.VideoCapture(name)
            frame_mum = frame_mum - args.frame_num + scene
            print('important frame',frame_mum)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_mum)
            while (ret):
                frames = []
                for i in range(args.frame_num):
                    ret, frame = cap.read()
                    if ret:
                        frame_mum+=1
                        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

                img_hists = sample_hist(frames, args.sample_num)
                similars = similar(img_hists)
                draw_one(similars,name)
                # patterns = pattern(similars)
                if lock_patterns:
                    # i=2
                    # important_frames = sum(np.array(patterns[(i - 1) * len(lock_patterns):i * len(lock_patterns)]) ^ np.array(patterns[i * len(lock_patterns):(i + 1) * len(lock_patterns)]))  ##检测关键帧比例
                    detect_patterns = detect_pattern(similars, args.FR)
                    if detect_patterns:
                        if sum(np.array(detect_patterns))== sum(np.array(lock_patterns)):
                            print('scene change but the frequent contain the same')
                            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_mum)
                            break
                # draw(similars, name)
                lock_patterns = detect_pattern(similars, args.FR)
                print('scene changed and the relocked video frequent is',lock_patterns)
                # draw(similars, name)

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_mum)

                break
        else:
            if lock_patterns:
                print('lock_patterns', lock_patterns)
            else:
            # patterns = pattern(similars)
                lock_patterns = detect_pattern(similars, args.FR)
                draw_one(similars, name)
        # draw(lock_patterns, name)

    cap.release()
    print('the video',name,' is end')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='frame detect')
    parser.add_argument('-frame_num', '--frame_num', type=int, default='60')
    parser.add_argument('-frame_rate', '--FR', type=int, default='60')
    parser.add_argument('--sample_num', default=1000, type=int)   #'C:/Users/ranran/Desktop/dataset'
    parser.add_argument('--data_path', default='E:/MEMC_CODE/data/962a', type=str)#E:\MEMC_CODE\收集的视频     C:/Users/ranran/Videos/RECentral/     E:\BaiduYunDownload\MEMC片源(1)  E:\MEMC_CODE\dataset
    args = parser.parse_args()
    data=os.listdir(args.data_path)
    print(data)
    # draw_one_video('save.avi')
    for i in range(len(data)):
        draw_one_video(os.path.join(args.data_path,data[i]))
    #     draw_one_video('../data/962a/coco_3.mp4')
    #     # draw_one_video('E:/MEMC_CODE/data/962a/2K-NXP-TRIDENT-MEMC-Clips_29fps_3.mp4')