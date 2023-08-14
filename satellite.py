#! /bin/python

import requests
import os
import time
from PIL import Image

download_path='/data/TyphoonWeather_Archive/satellite/pic/'
download_file = os.path.join(download_path+time.strftime('%Y-%m-%d %H:%M')+"-img.jpg")

 ## 检查目录是否创建，如果没有则创建  
def checkDir(download_path):
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdir(download_path)

# 下载壁纸
def Wallpaper():
    checkDir(download_path)   ## 检查目录创建
    picture_url = 'https://rammb.cira.colostate.edu/ramsdis/online/images/latest_hi_res/himawari-8/full_disk_ahi_true_color.jpg'   ## 下载向日葵9号链接
    res = requests.get(picture_url)    ### 创建一个 res 对象内容：下载图片
    ## 写入
    with open(download_file, 'wb') as f:
        f.write(res.content)

## 剪裁图片使之与屏幕相符
def cropWallpaper():
    img = Image.open(download_file)
    width, height = img.size
    x = 616
    y = 600
    box = (x, y, x+1920*2, y+1080*2)  ## 剪裁宽高
    region = img.crop(box)  # 用 img 类创建 region 对象
    region.save(os.path.join(download_path+'end.jpg')) ## 调用 save 方法保存最终图片
        
## 设置壁纸
def setWallpaper():
    os.system("feh --bg-fill ./pic/end.jpg")


if __name__ == "__main__":
    ## 循环以便自动更新壁纸
    while True:
        print("-"*20)
        print(time.strftime('%Y-%m-%d %H:%M'))
        print("下载中")
        Wallpaper()
        print("下载成功")
        cropWallpaper()    
        print("剪裁成功")
        setWallpaper()      
        print("壁纸设置成功")
        time.sleep(600)  ## 十分钟一换

   
