#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/29 20:07
# @Author  : linranran
# @Site    : 
# @File    : show_samples.py
# @Software: PyCharm


import os
import argparse
import cv2
import random
import numpy as np



def difference(hist1,hist2):
    sum=0
    for i in range(len(hist1)):
        sum+=abs(int(hist1[i]) -int(hist2[i]))
    return sum

def pix_difference(hist1,hist2):
    a=[]
    for i in range(len(hist1)):
        a.append(abs(int(hist1[i]) -int(hist2[i])))
    return a

def similar(img_hist):
    results=[]
    for i in range(len(img_hist) - 1):
        result=difference(img_hist[i], img_hist[i + 1])
        results.append(result)
    return results

def sample_refresh_hist(img,number):
    hists = []
    simi=[]
    mask = random.sample(range(1, img[1].shape[0]*img[1].shape[1]), number)
    for i in range(len(img)-1):
        sample_img=list((img[i].flat[j]) for j in mask)
        similar=pix_difference(list((img[i].flat[j]) for j in mask),list((img[i+1].flat[j]) for j in mask))
        simis=difference(list((img[i].flat[j]) for j in mask),list((img[i+1].flat[j]) for j in mask))
        if i%3==0:
            mask = gen_hashmask(img[1].shape[0], img[1].shape[1], similar, mask)
        hists.append(sample_img)
        simi.append(simis)
        imgs = np.zeros([img[1].shape[0], img[1].shape[1]], np.uint8)
        for j in mask:
            imgs.flat[j]=255

        cv2.imshow('input', imgs)
        cv2.imshow('2', img[i])
        cv2.waitKey(10)
    hists.append(list((img[i + 1].flat[j]) for j in mask))
    return  hists,simi
def random_2d_sample(w,h,m,n):
    mask=[]
    for i in range(m):
        for j in range(n):
            mask.append([random.randint(1, w),random.randint(1,h)])
    return mask


def gen_hashmask(w, h, similar, mask):
    number=len(mask)
    mask_new=[]
    a=w*h
    out=np.argsort(-np.array(similar))
    for i in out:
        mask_new.append(mask[i])
        while 1:
            x_new=random.randint(mask[i]-5,mask[i]+5)
            if x_new >=w*h or x_new<0:
                pass
            else:
                break
        mask_new.append(x_new)
        x_new1 = random.randint(0, w*h-1)
        mask_new.append(x_new1)
        if len(mask_new)>=number:
            break
    return mask_new
random.randint(1,100)


def get_img(file_path, num_frame):
    cap = cv2.VideoCapture(file_path)
    frames=[]
    for i in range(num_frame):
        ret, frame = cap.read()
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))



    cap.release()
    return frames

def draw_one_video(name):
    frames = get_img(name, args.frame_num)
    img_hists2,similars2 = sample_refresh_hist(frames, args.sample_num)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='frame detect')
    parser.add_argument('-frame_num', '--frame_num', type=int, default='120')
    parser.add_argument('-frame_rate', '--FR', type=int, default='60')
    parser.add_argument('--sample_num', default=10000, type=int)   #'C:/Users/ranran/Desktop/dataset'
    parser.add_argument('--data_path', default='E:/MEMC_CODE/data/838c', type=str)#E:\MEMC_CODE\收集的视频     C:/Users/ranran/Videos/RECentral/     E:\BaiduYunDownload\MEMC片源(1)  E:\MEMC_CODE\dataset
    args = parser.parse_args()
    data=os.listdir(args.data_path)
    print(data)

    for i in range(len(data)):
        draw_one_video(os.path.join(args.data_path,data[i]))
