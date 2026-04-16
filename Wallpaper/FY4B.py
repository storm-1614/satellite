#! /bin/python

import requests
import os
import logging
import time
import datetime
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image

downloadPath = os.path.join(os.environ["HOME"] + "/.cache/fy4b/")
Image.MAX_IMAGE_PIXELS = 300000000  # 设置最大图片尺寸


def init_log():
    """
    初始化日志模块
    """
    # TODO: 参数配置
    global logger
    logger = logging.getLogger("Logging")
    logger.setLevel(logging.INFO)
    file_hander = logging.FileHandler(downloadPath + "fy4b.log")
    file_hander.setLevel(logging.INFO)

    console_hander = logging.StreamHandler()
    console_hander.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_hander.setFormatter(formatter)
    console_hander.setFormatter(formatter)

    logger.addHandler(file_hander)
    logger.addHandler(console_hander)


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
            logger.info("下载中")
            res = requests.get(picture_url)  ### 创建一个 res 对象内容：下载图片
            logger.info("下载成功")
            global downloadFile
            downloadFile = os.path.join(
                downloadPath + time.strftime("%Y-%m-%d_%H:%M") + ".jpg"
            )  ## 写入
            with open(downloadFile, "wb") as f:
                f.write(res.content)
            break
        except requests.exceptions.ConnectTimeout:
            retry_count += 1
            time.sleep(3)
            logger.error(f"下载超时，正在进行第 {retry_count} 次重试...")
            if retry_count >= max_retry:
                logger.error(f"错误次数超过 {max_retry} 次，下载失败")
        except requests.exceptions.ConnectionError:
            time.sleep(3)
            retry_count += 1
            logger.error(f"连接错误，正在进行第 {retry_count} 次重试...")
            if retry_count >= max_retry:
                logger.error(f"错误次数超过 {max_retry} 次，下载失败")
        except requests.exceptions.ChunkedEncodingError:
            retry_count += 1
            logger.error(f"分块编码错误，正在进行第 {retry_count} 次重试...")
            if retry_count >= max_retry:
                logger.error(f"错误次数超过 {max_retry} 次，下载失败")


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
    logger.info(f"执行")
    downloadWallpaper()
    cropWallpaper()
    logger.debug("剪裁成功")
    setWallpaper()
    logger.debug("壁纸设置成功")


init_log()

scheduler = BackgroundScheduler()  # 创建一个后台调度器
scheduler.add_job(
    update,
    "cron",
    minute="10,25,40,55",
    id="update_wallpaper",
)  # 添加任务
update()


def watch_wake():
    """
    睡眠唤醒自动恢复
    """
    last = datetime.datetime.now()
    while True:
        time.sleep(5)
        now = datetime.datetime.now()
        time_diff = now - last # 对比时间差
        if time_diff > datetime.timedelta(minutes=1):
            try:
                logger.info("挂起，执行时间复位")
                if not scheduler.running:
                    logger.warning("调度器未运行，重启调度器")
                    scheduler.start()
                job = scheduler.get_job("update_wallpaper") # 获取任务
                if job:
                    job.modify(next_run_time=datetime.datetime.now())
                else:
                    logger.error("找不到任务")
            except Exception as e:
                logger.error(f"唤醒处理失败: {e}", exc_info=True)

        if time_diff > datetime.timedelta(minutes=15):
            try:
                time.sleep(10)
                logger.info("长时间挂起，立刻执行一次")
                update()
            except:
                pass

        last = now


threading.Thread(target=watch_wake, daemon=True).start()  # 启动监听
scheduler.start()  # 开启调度器
logger.info(f"调度器已启动")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
    logger.info("调度器已关闭")
