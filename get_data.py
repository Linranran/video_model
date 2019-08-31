#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/30 15:06
# @Author  : linranran
# @Site    : 
# @File    : get_data.py
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
from scipy.stats import pearsonr
import seaborn

def get_img(file_path, num_frame,img_type='gray',filter=None):
    """

    :param file_path:
    :param num_frame:
    :param img_type:
    :param filter:
    :return:
    """
    cap = cv2.VideoCapture(file_path)
    frames=[]
    if img_type=='gray':
        if filter:
            for i in range(num_frame):
                ret, frame = cap.read()
                frames.append(cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),(5,5),0))
        else:
            for i in range(num_frame):
                ret, frame = cap.read()
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        cap.release()
    if img_type=='rgb':
        for i in range(num_frame):
            ret, frame = cap.read()
            frames.append(frame)
        cap.release()
    return frames

def divide_imges(img, m, n):  # 分割成m行n列
    h, w = img[0].shape[0], img[0].shape[1]
    grid_h = int(h * 1.0 / m  + 0.5)
    grid_w = int(w * 1.0 / n  + 0.5)
    h = grid_h * m
    w = grid_w * n
    divide_images=[]
    for i in range(len(img)):
        img_re = cv2.resize(img[i], (w, h),cv2.INTER_LINEAR)  # 也可以用img_re=skimage.transform.resize(img, (h,w)).astype(np.uint8)
        # img_re=img[i]
        gx, gy = np.meshgrid(np.linspace(0, w, n+1), np.linspace(0, h, m+1))
        gx = gx.astype(np.int)
        gy = gy.astype(np.int)

        divide_image = np.zeros([ grid_h, grid_w],np.uint8)
        image=[]
        for i in range(m ):
            for j in range(n ):
                divide_image[ ...] = img_re[gy[i][j]:gy[i + 1][j + 1], gx[i][j]:gx[i + 1][j + 1]]
                image.append(copy.copy(divide_image))
        divide_images.append(image)

    mask0 = np.random.randint(0, high=2, size=[grid_h, grid_w], dtype=np.uint8)
    mask1 = np.ones( [grid_h, grid_w], dtype=np.uint8)
    # return [divide_images,mask0,mask1]
    return divide_images