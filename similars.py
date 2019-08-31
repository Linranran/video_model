#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/30 14:46
# @Author  : linranran
# @Site    : 
# @File    : difference.py
# @Software: PyCharm

import cv2
from matplotlib import pyplot
from PIL import Image
import numpy as np
import copy
import os
import argparse
import random
from skimage.measure import compare_ssim
import scipy.spatial.distance
def Cosine_distance_2(vector1, vector2):
    # 点与点的夹角余弦距离
    return scipy.spatial.distance.pdist(np.vstack((vector1, vector2)), 'cosine')
def euclidean_distance_2(vector1, vector2):
    # 点与点的夹角余弦距离
    return scipy.spatial.distance.pdist(np.vstack((vector1, vector2)), 'euclidean')



def sigmoid_similar(img_hist):
    similars=[]
    for i in range(len(img_hist) - 1):
        sim=sum(1 - (0 if l == r else float(abs(int(l) - int(r))) / max(l, r)) for l, r in zip(img_hist[i], img_hist[i+1])) / len(img_hist[i])
        similars.append(sim)
    return similars



def Cosine_similar(img_hist):
    similars=[]
    for i in range(len(img_hist) - 1):
        sim=Cosine_distance_2(img_hist[i],img_hist[i+1])
        similars.append(sim)
    return similars



def euclidean_similar(img_hist):
    similars=[]
    for i in range(len(img_hist) - 1):
        sim=euclidean_distance_2(img_hist[i],img_hist[i+1])
        similars.append(sim)
    return similars

def ssim(images):
    ssims=[]
    for i in range(len(images)-1):
        ssims.append(compare_ssim(images[i],images[i+1]))
    return ssims

# (score, diff) = compare_ssim(grayA, grayB, full=True)


def feng_difference(img1,img2):
    sum1 = 0
    pixels=[]
    for i in range(len(img1)):
            pixel=abs(int(img1[i])-int(img2[i]))
            pixels.append(pixel)
    dict={ }
    for key in pixels:
        dict[key] = dict.get(key, 0) + 1
    # print(dict)
    for  i in dict.keys():
        if i in [0,1,2] :
            pass
        elif i in [3,4,5,6,7]:
            sum1 = sum1 + dict[i]
        elif i in [8,9,10,11,12,13,14,15]:
            sum1 = sum1 + i*dict[i]
        else:
            sum1 = sum1 + 16* dict[i]

    # for i in dict.keys():
    #     sum1 = sum1 + i * dict[i]

    return sum1

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


def histogram(frames):
    return [cv2.calcHist([frames[i]], [0], None, [50], [0, 255], False) for i in range(len(frames))]

# def difference(histogram,type='nomal_difference'):
#     return [diff(histogram[i],histogram[i+1]) for i in range(len(histogram)-1)]
#     # if type == 'feng_difference':
#     #     return [feng_diff(histogram[i], histogram[i + 1]) for i in range(len(histogram) - 1)]



def similar(img_hist,type='similar'):
    similars = []
    if type=='similar':
        for i in range(len(img_hist)-1):
            similar=sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(img_hist[i], img_hist[i+1]))/len(img_hist[i])
            similars.append(similar)
    if type=='difference':
        for i in range(len(img_hist) - 1):
            similar = difference(img_hist[i],img_hist[i+1])
            similars.append(similar)
    if type == 'feng_difference':
        for i in range(len(img_hist) - 1):
            similar = feng_difference(img_hist[i], img_hist[i + 1])
            similars.append(similar)
    return similars



def divide_histogram(divide_frames):
    hists=[]
    for i in range(len(divide_frames)):
        hist = [cv2.calcHist([divide_frames[i][j]], [0], None, [20], [0, 255], False) for j in range(len(divide_frames[i]))]
        hists.append(copy.copy(hist))
    return hists



def divide_difference(img_hist,a,b):
    similars=[]
    for i in range(len(img_hist)-1):
        s = 0
        for j in range(len(img_hist[i])):
            similar = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(img_hist[i][j], img_hist[i+1][j])) / len(img_hist[i][j])
            s=s+similar
        similars.append(s/(a*b))
    return similars




def pattern(similars):
    patterns=[]
    for i in range(len(similars)-1):
        a=similars[i]-similars[i+1]
        if a >50:
            patterns.append(1)
        else:
            patterns.append(0)
    return patterns
