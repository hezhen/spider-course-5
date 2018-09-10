# spider-course-4
Spider course 4 sample, Python 3.6

## 环境搭建
1. 安装 python 3.6 
2. 安装 pip
    1. Linux 
    
        参考 https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers

    2. Windows
        
        \# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        
        \# python get-pip.py
3. 配置 pip 为清华源
    1. Linux、MacOS

        \# vim ~/.config/pip/pip.conf
        
        [global]<br>
        index-url = https://pypi.tuna.tsinghua.edu.cn/simple 
    
    2. Windows

        %APPDATA%\pip\pip.ini

        [global]<br>
        index-url = https://pypi.tuna.tsinghua.edu.cn/simple 
4. 统一安装全部需要的依赖库，执行下面的命令

    \#pip install -r requirements.txt 

## Ubuntu 18 虚拟机环境

    1. 下载安装 Virtubox 
    2. 下载 虚拟机，下载完成后解压后，双击启动虚拟机。下载链接: https://pan.baidu.com/s/1Rns_T6Pr3prMtXdQJOkgug 密码: kaq8
    3. 密码为 xxxy


## 目录结构
### weibo
> 利用微博的 API 来抓取微博的代码

### multithread
> 多线程抓取

### multi-process
> 多进程抓取，利用数据库来做任务队列

### mafengwo
> 利用分布式的方式抓取马蜂窝，包括了控制台、通信协议栈demo

### lxml
> lxml 的demo

### headless-chrome
> 用 Selenium + Chrome 的方式，抓取动态网页微博，安装方法在文件夹里有

### part_4_demo
> 第4节课作业的参考代码

### mfw_travel_notes
> 马蜂窝网站按照 城市名->游记 结构抓取的参考实现