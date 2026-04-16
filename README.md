# satellite

这个项目目前是有两个不同的程序:  
* downloadDigitalTyphoon 内是批量下载数字台风网的程序  
* Wallpaper 内是将风云四号或向日葵九号卫星的西太平洋云图用作壁纸  

### Wallpaper
这是一个用来下载卫星云图并设置为壁纸的 python 程序  
仅限用于 Linux 系统，如有需要，欢迎通过 Issues 为我提供其他操作系统的设置壁纸方法  
依赖 :  
```
sudo pacman -S feh python3 python-apscheduler
```

FY4B.py 比较完整，可以直接运行。会在`~/.cache/fy4b/`创建文件用作数据存储，而且不需要代理大陆内就可以使用  

### 日志
又过去了好几年，我也从高一那个迷茫的高中生到现在已经是一名计算机科学与技术专业的大一学生。这个项目算是我第一个“有用处”的程序，又翻过了三年的篇章，那时我还只是使用 dwm 窗口管理器而到现在使用 hyprland 变化了好多好多。目前 FY4B 还可以正常使用，但 rammb 的向日葵可见光的链接已经不在了。到现在，从最初用 `time.sleep()` 来简易的定时，到今天改版使用 `apscheduler.schedulers.background` 定时任务库，更加完善了。  
*——2026-04-15 21:51*  
