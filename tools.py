#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 16:21
# @Author  : linranran
# @Site    : 
# @File    : tools.py
# @Software: PyCharm
import cv2
from matplotlib import pyplot
from PIL import Image
import numpy as np
import copy
import os
import argparse
import random

from scipy.stats import pearsonr
import seaborn
from similars import *
from get_data import get_img




pyplot.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
pyplot.rcParams['axes.unicode_minus']=False

def draw_one(similars,name):
    x = range(0,len(similars),1)
    y = similars
    pyplot.plot(x, y)
    loc = 'left'
    font_dict = {'fontsize': 14, 'fontweight': 8.2, 'verticalalignment': 'baseline',  'horizontalalignment': loc}
    pyplot.title(name, fontdict=font_dict, loc=loc)
    pyplot.show()


def sample_hist(img,number):
    hists=[]
    result = random.sample(range(1, img[1].shape[0]*img[1].shape[1]), number)
    for i in range(len(img)):
        sample_img=list((img[i].flat[j]) for j in result)
        hists.append(sample_img)
    return  hists
# def sample_refresh_hist(img,number):
#     hists = []
#     mask = random.sample(range(1, img[1].shape[0]*img[1].shape[1]), number)
#     for i in range(len(img)-1):
#         sample_img=list((img[i].flat[j]) for j in mask)
#         similar=pix_difference(list((img[i].flat[j]) for j in mask),list((img[i+1].flat[j]) for j in mask))
#         # a=i % 2
#         if i%5==0:
#             mask = gen_hashmask(img[1].shape[0], img[1].shape[1], similar, mask)
#         hists.append(sample_img)
#     hists.append(list((img[i + 1].flat[j]) for j in mask))
#     return  hists


def sample_refresh_hist(img,number):
    hists = []
    simi=[]
    mask = random.sample(range(1, img[1].shape[0]*img[1].shape[1]), number)
    for i in range(len(img)-1):
        # mask = random.sample(range(1, img[1].shape[0] * img[1].shape[1]), number)
        sample_img=list((img[i].flat[j]) for j in mask)
        similar=pix_difference(list((img[i].flat[j]) for j in mask),list((img[i+1].flat[j]) for j in mask))
        simis=difference(list((img[i].flat[j]) for j in mask),list((img[i+1].flat[j]) for j in mask))
        if i%3==0:
            mask = gen_hashmask(img[1].shape[0], img[1].shape[1], similar, mask)
        hists.append(sample_img)
        simi.append(simis)
        # cv2.imshow('input', img[i])
        # cv2.waitKey(1)
        # cv2.circle(img[i], (center_x, center_y), 20, red, -1)
        # show_img = list((img[i].flat[j]) for j in mask)
    hists.append(list((img[i + 1].flat[j]) for j in mask))
    return  hists,simi


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

# def gen_hashmask(w, h, similar, mask):
#     number=len(mask)
#     mask_new=[]
#     a=w*h
#     out=np.argsort(-np.array(similar))
#     #
#     # a=out[0:len(out*1/4)]
#     # b=out[0:int(len(out)/4)]
#     for i in out[0:int(len(out)/4)] :
#         mask_new.append(mask[i])
#     while len(mask_new)<=number:
#             mask_new.append(random.randint(0,h*w-1))
#     return mask_new


def pixel_hist(img):
    hists=[]
    for i in range(len(img)):
        hists.append(img[i].flat)
    return  hists






# def pattern(similars):
#     patterns=[]
#     aver = sum(similars[i] for i in range(len(similars))) / len(similars)
#     for i in range(len(similars)):
#         # a=sum(similars[a] for a in range(i,i+10))/10
#         # a=similars[i]-similars[i+1]
#         if similars[i] >aver:
#             patterns.append(1)
#         else:
#             patterns.append(0)
#     return patterns

def scene_change(similars):
    ma= max(np.array(similars))
    # aver = sum(similars[i] for i in range(10))/10
    aver = sum(similars[i] for i in range(len(similars))) / len(similars)
    if ma>5*aver:
        return  similars.index(ma)

    return False

def re_detect_pattern(similars):
    patterns = pattern(similars)
    scene = scene_change(similars)
    have_pattern=0
    if scene:
        if have_pattern :
            important_frame= sum(np.array(patterns[(i - 1) * windows_len:i * windows_len]) ^ np.array(patterns[i * windows_len:(i + 1) * windows_len])) ##检测关键帧比例
            if important_frame==have_pattern:
                    pass
            else:
                detect_pattern(similars)
        else:
            detect_pattern(similars)

    else:
        detect_pattern(similars)




def detect_pattern(similars,FR):
    patterns = pattern(similars)
    for windows_len in range(2,FR):
        staturs = 0
        for i in range(1,int(len(patterns)/windows_len)):
            a=sum(np.array(patterns[(i-1)*windows_len:i*windows_len])^np.array(patterns[i*windows_len:(i+1)*windows_len]))
            if a ==0:
                staturs+=1
            else:
                staturs=0
            if staturs>2:
                if sum(patterns[(i - 1) * windows_len:i * windows_len])>0:
                    return (patterns[(i - 1) * windows_len:i * windows_len])
    return (patterns[(i-1)*windows_len:i*windows_len])

def hisogram_two_frame(frame1,frame2):
    h, w = frame1.shape[0], frame1.shape[1]
    hist = []
    for i in range(h):
        for j in range(w):
            hist.append(abs(int(frame1[i][j])-int(frame2[i][j])))
    dict={ }
    for key in hist:
        dict[key] = dict.get(key, 0) + 1
    return dict

def abs_diff(img1,img2):
    h, w = img1.shape[0], img1.shape[1]
    diff_img=np.ones( [h, w],dtype=int)
    for i in range(h):
        for j in range(w):
            diff_img[i][j]=int(img1[i][j])-int(img2[i][j])
    return diff_img


def draw_two(similar1,similar2,name):

    x = range(0, len(similar1), 1)

    pyplot.figure(name)
    pyplot.subplot(211)
    pyplot.plot(x, similar1)
    pyplot.title('Algorithm1')

    pyplot.subplot(212)
    pyplot.plot(x, similar2)
    pyplot.title('Algorithm2')
    pyplot.show()



def draw_four(similar1,similar2,similar3,similar4,name):

    x = range(0, len(similar1), 1)

    pyplot.figure(name)
    pyplot.subplot(221)
    pyplot.plot(x, similar1)
    pyplot.title('Algorithm1')

    pyplot.subplot(222)
    pyplot.plot(x, similar2)
    pyplot.title('Algorithm2')


    pyplot.subplot(223)
    # similar3.append(0)
    pyplot.plot(x, similar3)
    pyplot.title('Algorithm3')


    pyplot.subplot(224)
    # similar4.append(0)
    pyplot.plot(x, similar4)
    pyplot.title('Algorithm4')

    pyplot.show()


def abs_diff_images(img1,img2,type=None):
    """
    :param img1:
    :param img2:
    :param type:
    :return:
    """
    h, w = img1.shape[0], img1.shape[1]
    diff_img=np.ones( [h, w],dtype=int)
    sum=0
    for i in range(h):
        for j in range(w):
            diff_img[i][j]=abs(int(img1[i][j])-int(img2[i][j]))
            sum = sum + abs(int(img1[i][j]) - int(img2[i][j]))
    if type=='diff_img':
        return diff_img
    if type == 'diff_sum':
        return sum/h*w

def draw_hotmap(name,frame_num):
    frames=get_img(name,frame_num)
    for i in range(len(frames)-1):
        similars = abs_diff_images(frames[i],frames[i+1],type='diff_img')
        pyplot.plot()
        ax = seaborn.heatmap(similars, cmap="YlGnBu")
        ax.set_title('cubehelix map')
        pyplot.show()

def draw_abs_imgdiff(name,frame_num):
    frames=get_img(name,frame_num)
    similars = [abs_diff_images(frames[i],frames[i+1],type='diff_sum') for i in range(len(frames)-1)]
    pyplot.plot()
    x = range(0, len(similars), 1)
    pyplot.plot(x, similars)
    pyplot.show()