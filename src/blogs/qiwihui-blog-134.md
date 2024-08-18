# 16. 多线程 — Python 进阶


在本文中，我们讨论了如何在Python中使用 `threading` 模块。

- 如何创建和启动多个线程
- 如何等待线程完成
- 如何在线程之间共享数据
- 如何使用锁（ `lock` ）来防止竞态情况
- 什么是守护线程
- 如何使用 `Queue` 进行线程安全的数据/任务处理。

<!--more-->

### 创建和运行线程

你可以使用 `threading.Thread()` 创建一个线程。 它包含两个重要的参数：

- `target`：线程启动时要调用的该线程的可调用对象（函数）
- `args`：目标函数的（函数）参数。 这必须是一个元组

使用 `thread.start()` 启动线程

调用 `thread.join()` 告诉程序在继续执行其余代码之前，应等待该线程完成。

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

### 在线程之间共享数据

由于线程位于相同的内存空间中，因此它们可以访问相同的（公共）数据。 因此，例如，你可以简单地使用所有线程都具有读取和写入访问权限的全局变量。

任务：创建两个线程，每个线程应访问当前数据库值，对其进行修改（在这种情况下，仅将其增加1），然后将新值写回到数据库值中。 每个线程应执行10次此操作。

```python
from threading import Thread
import time

# 所有线程可以访问全局变量
database_value = 0

def increase():
    global database_value # 需要可以修改全局变量
    
    # 获取本地副本（模拟数据获取）
    local_copy = database_value

    # 模拟一些修改操作
    local_copy += 1
    time.sleep(0.1)

    # 将计算的性质写入全局变量
    database_value = local_copy

if __name__ == "__main__":

    print('Start value: ', database_value)

    t1 = Thread(target=increase)
    t2 = Thread(target=increase)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('End value:', database_value)

    print('end main')
```

```python
    Start value:  0
    End value: 1
    end main
```

### 如何使用锁

请注意，在上面的示例中，2个线程将值递增1，因此将执行2个递增操作。但是，为什么最终值是1而不是2？

### 竞态条件

这里发生了竞态情况。当两个或多个线程可以访问共享数据并且它们试图同时更改它们时，就会发生竞态情况。因为线程调度算法可以随时在线程之间交换，所以你不知道线程尝试访问共享数据的顺序。在我们的例子中，第一个线程访问 `database_value`（0）并将其存储在本地副本中。然后将其递增（ `local_copy` 现在为1）。利用我们的 `time.sleep()` 函数，该函数仅模拟一些耗时的操作，在此期间，程序将交换到第二个线程。这还将检索当前的 `database_value`（仍为0），并将 `local_copy` 递增为1。现在，两个线程都有一个值为1的本地副本，因此两个线程都将1写入全局 `database_value`。这就是为什么最终值是1而不是2的原因。

### 使用锁避免竞态条件

锁（也称为互斥锁）是一种同步机制，用于在存在许多执行线程的环境中强制限制对资源的访问。锁具有两种状态：**锁定**和**解锁**。如果状态是锁定的，则在状态再次被解锁之前，不允许其他并发线程进入此代码段。

两个函数很重要：

- `lock.acquire()`：这将锁定状态并阻塞
- `lock.release()`：这将再次解锁状态。

重要提示：块获得后，你应始终再次释放它！

在我们的示例中，检索和修改数据库值的关键代码部分现已锁定。这样可以防止第二个线程同时修改全局数据。我们的代码没有太大变化。所有新更改都在下面的代码中进行了注释。

```python
# import Lock
from threading import Thread, Lock
import time

database_value = 0

def increase(lock):
    global database_value 
    
    # 锁定状态
    lock.acquire()
    
    local_copy = database_value
    local_copy += 1
    time.sleep(0.1)
    database_value = local_copy
    
    # 解锁状态
    lock.release()

if __name__ == "__main__":

    # 创建锁
    lock = Lock()
    
    print('Start value: ', database_value)

    # 将锁传递给目标函数
    t1 = Thread(target=increase, args=(lock,)) # 注意锁后的逗号，因为args必须是一个元组
    t2 = Thread(target=increase, args=(lock,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('End value:', database_value)

    print('end main')
```

```python
    Start value:  0
    End value: 2
    end main
```

### 使用锁作为上下文管理器

在 `lock.acquire()` 之后，你应该永远不要忘记调用 `lock.release()` 来解锁代码。 你还可以将锁用作上下文管理器，这将安全地锁定和解锁你的代码。 建议以这种方式使用锁：

```python
def increase(lock):
    global database_value 
    
    with lock: 
        local_copy = database_value
        local_copy += 1
        time.sleep(0.1)
        database_value = local_copy
```

### 在Python中使用队列

队列可用于多线程和多进程环境中的线程安全/进程安全的数据交换和数据处理。

### 队列

队列是遵循先进先出（FIFO）原理的线性数据结构。 一个很好的例子是排队等候的客户队列，其中首先服务的是第一位的客户。

```python
from queue import Queue

# 创建队列
q = Queue()

# 添加元素
q.put(1) # 1
q.put(2) # 2 1
q.put(3) # 3 2 1 

# 现在 q 看起来是这样的:
# back --> 3 2 1 --> front

# 获取和移除第一个元素
first = q.get() # --> 1
print(first) 

# q 现在看起来是这样的:
# back --> 3 2 --> front
```

```python
    1
```

### 在多线程中使用队列

带有队列的操作是线程安全的。重要方法是：

- `q.get()`：删除并返回第一项。默认情况下，它会阻塞，直到该项可用为止。
- `q.put(item)`：将元素放在队列的末尾。默认情况下，它会阻塞，直到有空闲插槽可用为止。
- `q.task_done()`：指示先前入队的任务已完成。对于每个 `get()`，在完成此项任务后，都应调用此函数。
- `q.join()`：阻塞直到队列中的所有项目都已获取并处理（已为每个项目调用 `task_done()`）。
- `q.empty()`：如果队列为空，则返回True。

以下示例使用队列来交换0至19之间的数字。每个线程都调用worker方法。在无限循环内，线程等待直到由于阻塞 `q.get()` 调用而使项可用为止。项可用时，将对其进行处理（即，仅在此处打印），然后 `q.task_done()` 告知队列处理已完成。在主线程中，创建10个**守护**线程。这意味着它们在主线程死亡时自动死亡，因此不再调用worker方法和无限循环。然后，队列中填充了项，并且worker方法可以继续使用可用项。最后，需要 `q.join()` 来阻塞主线程，直到获得并处理所有项为止。

```python
from threading import Thread, Lock, current_thread
from queue import Queue

def worker(q, lock):
    while True:
        value = q.get()  # 阻塞知道有可用项

        # 做一些处理...
        with lock:
            # 使用锁阻止其他打印
            print(f"in {current_thread().name} got {value}")
        # ...

        # 对弈每一个 get()，随后对 task_done() 的调用告诉队列该项的处理已完成。
        # 如果完成所有任务，则 q.join() 可以取消阻塞
        q.task_done()

if __name__ == '__main__':
    q = Queue()
    num_threads = 10
    lock = Lock()

    for i in range(num_threads):
        t = Thread(name=f"Thread{i+1}", target=worker, args=(q, lock))
        t.daemon = True  # 当主线程死亡时死亡
        t.start()
    
    # 使用项填充队列
    for x in range(20):
        q.put(x)

    q.join()  # 阻塞直到队列中的所有项被获取并处理

    print('main done')
```

```python
    in Thread1 got 0
    in Thread2 got 1
    in Thread2 got 11
    in Thread2 got 12
    in Thread2 got 13
    in Thread2 got 14
    in Thread2 got 15
    in Thread2 got 16
    in Thread2 got 17
    in Thread2 got 18
    in Thread2 got 19
    in Thread8 got 5
    in Thread4 got 9
    in Thread1 got 10
    in Thread5 got 2
    in Thread6 got 3
    in Thread9 got 6
    in Thread7 got 4
    in Thread10 got 7
    in Thread3 got 8
    main done
```

### 守护线程

在以上示例中，使用了守护线程。 守护线程是后台线程，它们在主程序结束时自动消失。 这就是为什么可以退出 worker 方法内的无限循环的原因。 没有守护进程，我们将不得不使用诸如 `threading.Event` 之类的信号机制来停止 worker。 但请注意守护进程：它们会突然停止，并且它们的资源（例如打开的文件或数据库事务）可能无法正确释放/完成。

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/134)


