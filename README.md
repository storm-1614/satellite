# satellite

这个项目目前是有两个不同的程序:  
* downloadDigitalTyphoon 内是批量下载数字台风网的程序  
* Wallpaper 内是将风云四号或向日葵九号卫星的西太平洋云图用作壁纸  

### Wallpaper
这是一个用来下载卫星云图并设置为壁纸的 python 程序  
仅限用于 Linux 系统，如有需要，欢迎通过 Issues 为我提供其他操作系统的设置壁纸方法  
依赖 :  
```
sudo pacman -S feh python3
```

FY4B.py 比较完整，可以直接运行。会在`~/.cache/fy4b/`创建文件用作数据存储，而且不需要代理大陆内就可以使用  
