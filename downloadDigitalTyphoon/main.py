#! /bin/python

import time
import requests
import os

### 开始下载的时间 
## **年**月**日**时间
t = '22010420'

 ## 检查目录是否创建，如果没有则创建  
def checkDir(downloadPath):
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdir(downloadPath)

## 时间字符串转换成时间戳
def timeToStamp (t):  
    t1 = time.strptime(t, '%y%m%d%H')
    t2 = time.mktime(t1)
    return t2

## 时间戳转换成时间字符串
def stampToTime (t):
    t1 = time.localtime(t)
    t2 = time.strftime('%y%m%d%H', t1)
    return t2

## 下载图片 参数：链接，文件时间
def downloadImg(download_url,time):
    res = requests.get(download_url)
    download_file = ('./img/'+time+'.jpg')
    with open(download_file, 'wb') as f:
        f.write(res.content)


checkDir('./img')

Running = True
while Running:
    ## 一个 try 语句房子网络问题导致报错中断
    try:
        url = "http://agora.ex.nii.ac.jp/digital-typhoon/globe/color/2022/2048x2048/HMW8"+t+".globe.1.jpg"
        downloadImg(url,t)
        print(t," OK")
        t = timeToStamp(t)
        t = t + 3600
        t = stampToTime(t)
    except:    
        continue
        
    if t == '23010101':  ## 停止时间
        Running = False

