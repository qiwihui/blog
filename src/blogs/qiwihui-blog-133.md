---
title: "15. 多线程和多进程 — Python 进阶"
description: "15. 多线程和多进程 — Python 进阶"
tags: 
- 技术
- Python
top: 133
date: 29/03/2021, 22:33:53
author: qiwihui
update: 29/03/2021, 22:33:53
categories: 技术
---

我们有两种常用的方法来并行运行代码（实现多任务并加快程序速度）：通过线程或通过多进程。

<!--more-->

## 进程

进程是程序的一个实例，例如Python解释器。它们彼此独立，并且不共享相同的内存。

关键事实：

- 一个新进程独立于第一个进程启动
- 充分利用多个CPU和内核
- 单独的内存空间
- 进程之间不共享内存
- 每个进程一个GIL（全局解释器锁），即避免了GIL限制
- 非常适合CPU密集型处理
- 子进程可中断/可终止
- 启动进程慢于启动线程
- 更大的内存占用
- IPC（进程间通信）更加复杂

### 线程

线程是可以调度执行的进程（也称为“轻量级进程”）中的实体。一个进程可以产生多个线程。主要区别在于，进程中的所有线程共享同一内存。

关键事实：

- 可以在一个进程中产生多个线程
- 内存在所有线程之间共享
- 启动线程比启动进程要快
- 适用于 I/O 密集型任务
- 轻量
- 内存占用少
- 所有线程使用一个GIL，即线程受GIL限制
- 由于GIL，多线程处理对CPU密集的任务无效
- 不可中断/杀死->注意内存泄漏
- 出现竞态情况的可能性增加

### Python中的线程

使用 `threading` 模块。

注意：由于受CPU限制，以下示例通常不会从多个线程中受益。 它应显示如何使用线程的示例。

```python
from threading import Thread

def square_numbers():
    for i in range(1000):
        result = i * i

        
if __name__ == "__main__":        
    threads = []
    num_threads = 10

    # 创建线程，并给每一个线程分配函数
    for i in range(num_threads):
        thread = Thread(target=square_numbers)
        threads.append(thread)

    # 启动所有线程
    for thread in threads:
        thread.start()

    # 等待所有线程结束
    # 阻塞主线程直到所有线程结束
    for thread in threads:
        thread.join()
```

### 线程何时有用

尽管使用了GIL，但在程序必须与速度较慢的设备（例如硬盘驱动器或网络连接）进行通讯时，它仍可用于 I/O 密集型任务。 通过线程化，程序可以花费时间等待这些设备并同时智能地执行其他任务。

示例：从多个站点下载网站信息。 为每个站点使用一个线程。

### 多进程

使用 `multiprocessing` 模块。 语法与上面非常相似。

```python
from multiprocessing import Process
import os

def square_numbers():
    for i in range(1000):
        result = i * i

if __name__ == "__main__":
    processes = []
    num_processes = os.cpu_count()

    # 创建进程，并给每一个线程分配函数
    for i in range(num_processes):
        process = Process(target=square_numbers)
        processes.append(process)

    # 启动所有进程
    for process in processes:
        process.start()

    # 等待所有进程结束
    # 阻塞主线程直到所有进程结束
    for process in processes:
        process.join()
```

### 什么时候多进程有用

这对于必须对大量数据执行大量CPU操作且需要大量计算时间的CPU密集型任务很有用。通过多进程，你可以将数据分成相等的部分，然后在不同的CPU上进行并行计算。

示例：计算从1到1000000的所有数字的平方数。将数字分成相等大小的部分，并对每个子集使用一个过程。

### GIL-全局解释器锁

这是一个互斥锁（或锁），仅允许一个线程控制Python解释器。这意味着即使在多线程体系结构中，GIL一次也只允许一个线程执行。

### 为什么需要它？

之所以需要它，是因为CPython（Python的引用实现）的内存管理不是线程安全的。 Python使用引用计数进行内存管理。这意味着在Python中创建的对象具有引用计数变量，该变量跟踪指向该对象的引用数。当此计数达到零时，将释放对象占用的内存。问题在于该引用计数变量需要保护，以防止两个线程同时增大或减小其值的竞争条件。如果发生这种情况，则可能导致从未释放的内存泄漏，或者在仍然存在对该对象的引用的情况下错误地释放了内存。

### 如何避免GIL

GIL在Python社区中引起很大争议。避免GIL的主要方法是使用多线程而不是线程。另一个（但是很不舒服）的解决方案是避免CPython实现，而使用 `Jython` 或 `IronPython` 之类的自由线程Python实现。第三种选择是将应用程序的部分移到二进制扩展模块中，即使用Python作为第三方库的包装器（例如在C / C ++中）。这是 `numpy` 和 `scipy` 采取的路径。

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

