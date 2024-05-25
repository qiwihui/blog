---
title: "在VirtualBox安装Arch Liux初步指南"
description: "在VirtualBox安装Arch Liux初步指南"
tags: 
- 技术
top: 20
date: 10/09/2018, 13:36:09
author: qiwihui
update: 31/01/2019, 16:05:32
categories: 技术
---

简单地写一下在VirtualBox上安装Arch Linux的过程，以此为在PC上安装做准备。在PC上安装的过程和下面描述的基本一致。
<!--more-->

##0x00 准备

1. 下载iso文件：在Arch官网上[下载](https://www.archlinux.org/download/)最新的镜像，这里
  我选用了[163.com](http://mirrors.163.com/archlinux/iso/2015.01.01/)节点的资源，下载archlinux-2015.01.01-dual.iso；

2. 检查文件的完整性：在MAC中使用md5或者sha1检验文件的完整行，并和下载站点提供的值进行比较。

    ~~~sh
    $ openssl sha1 archlinux-2014.12.01-dual.iso 
    SHA1(archlinux-2014.12.01-dual.iso)= 86085153f97f0097fd0a02496e67cf85138c1ba5

    $ md5 archlinux-2014.12.01-dual.iso 
    MD5 (archlinux-2014.12.01-dual.iso) = 667ed3c5e935666edfd54a2271e05b72
    ~~~

##0x01 创建虚拟机

1. 给虚拟机一个名字
    <img src="/media/files/2015/Jan/0-NameAndOperatingSystem.png"><img>

2. 内存：最小为256MB
    <img src="/media/files/2015/Jan/1-MemorySize.png"><img>

3. 创建新的虚拟磁盘
    <img src="/media/files/2015/Jan/2-HardDrive.png"><img>

4. 文件类型
    <img src="/media/files/2015/Jan/3-HardDriveFileType.png"><img>

5. 动态分配
    <img src="/media/files/2015/Jan/4-StorageOnPhysicalHardDrive.png"><img>

6. 文件位置和大小，最小10GB
    <img src="/media/files/2015/Jan/5-FileLocationAndSize.png"><img>

7. 如果要安装桌面环境的话就勾选`Enable 3D Acceleration`
    <img src="/media/files/2015/Jan/6-Enable3DAcceleration.png"><img>

8. 第一次启动虚拟机时，选取之前下载的ISO文件
    <img src="/media/files/2015/Jan/7-SelectISOFile.png"><img>

##0x01 开始安装

1. 选择32位或者64位Arch
    <img src="/media/files/2015/Jan/8-BootArchLinux.png"><img>

    一旦看到如下提示，就可以开始进行配置了：
    <img src="/media/files/2015/Jan/9-Command.png"><img>

2. 更改键盘布局和设置语言：

    默认键盘布局为`us`，非us布局可以用如下命令修改：

    ```sh
    # loadkeys layout
    ```

    layout可以是`uk`, `dvorak`等。设置语言：

2. 磁盘分区

    先看一下磁盘状态：

    ```sh
    # ls /dev
    ```

    开始啦，一般创建四个分区：`/`, `/boot`, `/home`, `swap`

    ```
    # gdisk /dev/sda
    ```

    当出现下面命令时, 开始分区，一下以`/boot`分区为例：

    ```
    Command (? for help):
    ```

    a. 创建新分区：'n'
    b. 分区号码：回车默认从0开始递增
    c. "first sector": 回车默认从上一个分区结束处开始，初始为0
    d. "last sector": '+250MB'
    e. "hex code": 回车默认（8300 为"Linux File System"），`swap`分区输入8200, 见[这儿](http://www.basicconfig.com/hex_codes_system_id)

    依次给`swap`分配'+1G'（和分配的RAM一样大），`/boot`分配'+8G'，`/home`分配'+1G'，再次看一下磁盘的状态，可以看到已经分配好了，
    键入'w'并回车即可保存修改。

3. 格式化分区

    再次回到命令行：

    ```
    root@archiso ~ #
    ```

    格式化分区：

    ```
    # mkfs -t ext4 /dev/sda1
    # mkfs -t ext4 /dev/sda3
    # mkfs -t ext4 /dev/sda4

    # mkswap /dev/sda2
    ```

4. 挂载新分区

    ```
    # swapon /dev/sda2

    # mount /dev/sda3 /mnt
    # cd /mnt
    # mkdir boot home
    # mount /dev/sda1 boot
    # mount /dev/sda4 home
    ```

5. 安装Arch

    ```
    # cd /
    # pacstrap /mnt base base-devel
    ```

6. 生成`fstab`文件

    ```
    # genfstab -p /mnt >> /mnt/etc/fstab
    ```

    可以看看fstab里面的内容：

    ```
    # more /mnt/etc/fstab
    ```

7. 初始化安装Boot Loader

    ```
    # pacstrap /mnt syslinux
    ```

8. 配置安装

    运行以下命令：

    ```
    # arch-chroot /mnt
    ```

    得到：

    ```
    sh-4.2#
    ```
    这个shell很基础，用Bash也许更好些：

    ```
    # bash
    ```

    得到：

    ```
    [root@archiso /]#
    ```

    设置语言：

    ```sh
    # nano /etc/locale.conf
    ```

    添加：

    ```
    LANG="en_US.UTF-8"
    ```

    ```sh
    # nano /etc/locale.gen
    ```

    将下面两行前面`#`去除：

    ```
    en_US.UTF-8 UTF-8
    de_DE.UTF-8 UTF-8
    ```

    完成语言设置：

    ```
    # locale-gen
    ```

    设置时间：

    ```
    # ln -s /usr/share/zoneinfo/<your_state>/<your_city> /etc/localtime
    ```

    比如我设置的是：

    ```
    # ln -s /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
    ```

    改hostname：

    ```
    # nano /etc/hostname
    ```

9. 完成Bootloader安装

    ```
    # cd /boot/syslinux/
    ```

    打开syslinux.cfg文件，找到"comboot modules"一段：

    ```
    # more syslinux.cfg
    ```

    将其中列举的文件copy到本地，同时还要加上'libutil.c32':

    ```
    # cp /usr/lib/syslinux/bios/menu.c32 .
    # cp /usr/lib/syslinux/bios/vesamenu.c32 .
    # cp /usr/lib/syslinux/bios/chain.c32 .
    # cp /usr/lib/syslinux/bios/hdt.c32 .
    # cp /usr/lib/syslinux/bios/reboot.c32 .
    # cp /usr/lib/syslinux/bios/poweroff.c32 .
    # cp /usr/lib/syslinux/bios/libutil.c32 .
    ```

    一旦完成上述设置，

    ```
    # extlinux --install /boot/syslinux
    # dd conv=notrunc bs=440 count=1 if=/usr/lib/syslinux/bios/gptmbr.bin of=/dev/sda
    # mkinitcpio -p linux
    ```

10. 完成安装

    最后，更改root密码：

    ```
    # passwd
    ```

    输入两次`exit`退回到：

    ```
    [root@archiso /]#
    ```

    umount所有的分区：

    ```
    # umount /mnt/boot
    # umount /mnt/home
    # swapoff /dev/sda2
    # umount /mnt
    ```

    在重启之前最后一步，设置`/boot`分区的[BIOS](http://en.wikipedia.org/wiki/BIOS)标识为'bootable'：

    ```
    # sgdisk /dev/sda --attributes=1:set:2
    ```

11. 重启Arch

    ```
    # reboot
    ```

    重启之后会再次进入CD启动，这时，去除安装CD，再次重启：

    ```
    Devices > CD/DVD Devices > Remove disk from virtual drive
    ```

    等待一小会：

    <img src="/media/files/2015/Jan/10-ArchLinux.png"><img>

    Congradulations!

12. 后续工作

    链接网络：

    ```
    dhcpcd
    ```

    安装'sudo'：

    ```
    # pacman -S sudo
    ```

    添加'sudoer':

    ```
    # nano /etc/sudoers
    ```

    ```
    ##
    ## User privilege specification
    ##
    root ALL=(ALL) ALL
    qiwihui ALL=(ALL) ALL
    ```

    保存，并log out：

    ```
    # exit
    ```

    以新的ID和密码重新登录。

    最后，每次登录的时候自动获取ip：

    ```
    # sudo systemctl enable dhcpcd@eth0.service
    ```

这样最基本的Arch Linux就好了，Desktop Environment就不装了。


## 0x02 参考文档

- [Arch Linux Beginners' guide](https://wiki.archlinux.org/index.php/Beginners%27_guide)
- [Arch Linux Installation Guide](https://wiki.archlinux.org/index.php/Installation_guide)
- [A Guide to Installing Arch in VirtualBox](http://wideaperture.net/blog/?p=3851)


### Comments

