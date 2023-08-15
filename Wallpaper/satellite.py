#! /bin/python

import requests
import os
import time
from PIL import Image

downloadPath='/data/TyphoonWeather_Archive/satellite/pic/'

 ## 检查目录是否创建，如果没有则创建  
def checkDir(downloadPath):
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdir(downloadPath)

# 下载壁纸
def downloadWallpaper():
    checkDir(downloadPath)   ## 检查目录创建
    picture_url = 'https://rammb.cira.colostate.edu/ramsdis/online/images/latest_hi_res/himawari-8/full_disk_ahi_true_color.jpg'   ## 下载向日葵9号链接
    res = requests.get(picture_url)    ### 创建一个 res 对象内容：下载图片
    global downloadFile
    downloadFile = os.path.join(downloadPath+time.strftime('%Y-%m-%d %H:%M')+"-img.jpg")
    ## 写入
    with open(downloadFile, 'wb') as f:
        f.write(res.content)

## 剪裁图片使之与屏幕相符
def cropWallpaper():
    img = Image.open(downloadFile)
    width, height = img.size
    x = 616
    y = 600
    box = (x, y, x+1920*2, y+1080*2)  ## 剪裁宽高
    region = img.crop(box)  # 用 img 类创建 region 对象
    region.save(os.path.join(downloadPath+'end.jpg')) ## 调用 save 方法保存最终图片
        
## 设置壁纸
def setWallpaper():
    os.system("feh --bg-fill "+downloadPath+"/end.jpg")


if __name__ == "__main__":
    ## 循环以便自动更新壁纸
    while True:
        setWallpaper()
        print("-"*20)
        print(time.strftime('%Y-%m-%d %H:%M'))
        print("下载中")
        try:
            downloadWallpaper()
            print("下载成功")
        except:
            print("下载失败")
            continue
        cropWallpaper()    
        print("剪裁成功")
        setWallpaper()      
        print("壁纸设置成功")
        time.sleep(600)  ## 十分钟一换

 
