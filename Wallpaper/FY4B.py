#! /bin/python

import requests
import os
import time
from PIL import Image

downloadPath='./pic/'

 ## 检查目录是否创建，如果没有则创建  
def checkDir(downloadPath):
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdir(downloadPath)

# 下载壁纸
def downloadWallpaper():
    checkDir(downloadPath)   ## 检查目录创建
    picture_url = 'http://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_DISK_GCLR.JPG'   ## 下载 FY4B 链接
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
    x = 2000
    y = 1000
    box = (x, y, x+1920*3.8, y+1080*3.8)  ## 剪裁宽高
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
        time.sleep(900)  ## 十分钟一换


