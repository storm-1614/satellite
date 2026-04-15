#! /bin/python

import requests
import os
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image

downloadPath = os.path.join(os.environ["HOME"] + "/.cache/fy4b/")
Image.MAX_IMAGE_PIXELS = 300000000  # 设置最大图片尺寸


## 检查目录是否创建，如果没有则创建
def checkDir(downloadPath):
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdir(downloadPath)


# 下载壁纸
def downloadWallpaper():
    checkDir(downloadPath)  ## 检查目录创建
    picture_url = "http://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_DISK_GCLR.JPG"  ## 下载 FY4B 链接
    res = requests.get(picture_url)  ### 创建一个 res 对象内容：下载图片
    global downloadFile
    downloadFile = os.path.join(downloadPath+time.strftime('%Y-%m-%d_%H:%M')+"-img.jpg")
    #downloadFile = os.path.join(downloadPath + "img.jpg")
    ## 写入
    with open(downloadFile, "wb") as f:
        f.write(res.content)


## 剪裁图片使之与屏幕相符
def cropWallpaper():
    img = Image.open(downloadFile)
    width, height = img.size
    x = 2400
    y = 1200
    box = (x, y, x + 1920 * 4.5, y + 1080 * 4.5)  ## 剪裁宽高
    region = img.crop(box)  # 用 img 类创建 region 对象
    region.save(os.path.join(downloadPath + "end.jpg"))  ## 调用 save 方法保存最终图片


## 设置壁纸
def setWallpaper():
    os.system(
        "awww img -a --transition-type=center " + downloadPath + "end.jpg"
    )  # hyprland with hyprpaper


def update():
    """
    壁纸更新函数
    """
    time.sleep(1);
    print("=================")
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行")
    print("下载中")
    downloadWallpaper()
    print("下载成功")
    cropWallpaper()
    print("剪裁成功")
    setWallpaper()
    print("壁纸设置成功")

if __name__ == "__main__":
    scheduler = BackgroundScheduler() # 创建一个后台调度器
    scheduler.add_job(update, 'interval', minutes = 15, id='update_wallpaper', next_run_time=datetime.datetime.now()) # 添加任务
    scheduler.start() # 开启调度器
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 调度器已启动")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("\n调度器已关闭")
