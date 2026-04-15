#! /bin/python

import requests
import os
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image

downloadPath = os.path.join(os.environ["HOME"] + "/.cache/fy4b/")
Image.MAX_IMAGE_PIXELS = 300000000  # 设置最大图片尺寸


def checkDir(downloadPath):
    """
    检查目录是否创建，如果没有则创建
    """
    mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdir(downloadPath)


def downloadWallpaper():
    """
    下载壁纸
    调用 requests 库，下载 nsmc 的 fy4b 真彩云图
    """
    checkDir(downloadPath)  
    picture_url = "http://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_DISK_GCLR.JPG"  ## 下载 FY4B 链接
    retry_count = 0
    max_retry = 5
    while retry_count < max_retry:
        try:
            print("下载中")
            res = requests.get(picture_url)  ### 创建一个 res 对象内容：下载图片
            print("下载成功")
            global downloadFile
            downloadFile = os.path.join(
                downloadPath + time.strftime("%Y-%m-%d_%H:%M") + "-img.jpg"
            )  ## 写入
            with open(downloadFile, "wb") as f:
                f.write(res.content)
            break
        except requests.exceptions.ConnectTimeout:
            retry_count += 1
            print(f"下载超时，正在进行第 {retry_count} 次重试...")
            if retry_count >= max_retry:
                print("错误次数超过 {max_retry} 次，下载失败")
        except requests.exceptions.ConnectionError:
            retry_count += 1
            print(f"连接错误，正在进行第 {retry_count} 次重试...")
            if retry_count >= max_retry:
                print("错误次数超过 {max_retry} 次，下载失败")


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
    time.sleep(1)
    print("=================")
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行")
    downloadWallpaper()
    print("下载成功")
    cropWallpaper()
    print("剪裁成功")
    setWallpaper()
    print("壁纸设置成功")


if __name__ == "__main__":
    scheduler = BackgroundScheduler()  # 创建一个后台调度器
    scheduler.add_job(
        update,
        "interval",
        minutes=15,
        id="update_wallpaper",
        next_run_time=datetime.datetime.now(),
    )  # 添加任务
    scheduler.start()  # 开启调度器
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 调度器已启动")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("\n调度器已关闭")
