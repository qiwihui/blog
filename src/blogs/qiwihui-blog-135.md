# 17. 多进程 — Python 进阶

在本文中，我们讨论了如何在Python中使用 `multiprocessing` 模块。

- 如何创建和启动多个进程
- 如何等待进程完成
- 如何在进程之间共享数据
- 如何使用 `lock` 来防止竞态情
- 如何使用 `Queue` 进行进程安全的数据/任务处理
- 如何使用 `Pool` 来管理多个工作进程。

<!--more-->

### 创建和运行进程

你可以使用 `multiprocessing.Process()` 创建一个进程。 它包含两个重要的参数：

- `target`：进程启动时要调用的可调用对象（函数）
- `args`：目标函数的（函数）参数。 这必须是一个元组。

使用 `process.start()` 启动一个进程

调用 `process.join()` 告诉程序在继续执行其余代码之前，应等待该进程完成。

```python
from multiprocessing import Process
import os

def square_numbers():
    for i in range(1000):
        result = i * i

        
if __name__ == "__main__":        
    processes = []
    num_processes = os.cpu_count()
    # 机器CPU的数量，通常是确定进程数量的一个好选择

    # 创建进程并分配每个进程一个函数
    for i in range(num_processes):
        process = Process(target=square_numbers)
        processes.append(process)

    # 启动所有进程
    for process in processes:
        process.start()

    # 等待所有进程结束
    # 阻塞主程序直到所有进程结束
    for process in processes:
        process.join()
```

### 在进程之间共享数据

由于进程不在同一个内存空间中，因此它们无法访问相同（公共）数据。 因此，它们需要特殊的共享内存对象来共享数据。

可以使用 `Value` 或者 `Array` 将数据存储在共享内存变量中。

- `Value(type, value)`：创建类型为 `type` 的 `ctypes` 对象。 使用 `.target` 访问该值。
- `Array(type, value)`：使用类型为 `type` 的元素创建一个 `ctypes` 数组。 用 `[]` 访问值。

任务：创建两个进程，每个进程都应该有权访问一个共享变量并对其进行修改（在这种情况下，只是将其重复增加1达100次）。 创建另外两个共享一个数组的进程，然后修改（增加）该数组中的所有元素。

```python
from multiprocessing import Process, Value, Array
import time

def add_100(number):
    for _ in range(100):
        time.sleep(0.01)
        number.value += 1

def add_100_array(numbers):
    for _ in range(100):
        time.sleep(0.01)
        for i in range(len(numbers)):
            numbers[i] += 1

if __name__ == "__main__":

    shared_number = Value('i', 0) 
    print('Value at beginning:', shared_number.value)

    shared_array = Array('d', [0.0, 100.0, 200.0])
    print('Array at beginning:', shared_array[:])

    process1 = Process(target=add_100, args=(shared_number,))
    process2 = Process(target=add_100, args=(shared_number,))

    process3 = Process(target=add_100_array, args=(shared_array,))
    process4 = Process(target=add_100_array, args=(shared_array,))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    print('Value at end:', shared_number.value)
    print('Array at end:', shared_array[:])

    print('end main')
```

```python
    Value at beginning: 0
    Array at beginning: [0.0, 100.0, 200.0]
    Value at end: 144
    Array at end: [134.0, 237.0, 339.0]
    end main
```

### 如何使用锁

请注意，在上面的示例中，两个进程应将共享值增加1达100次。 这样一来，总共进行了200次操作。 但是为什么终值不是200？

### 竞态条件

这里发生了竞态情况。当两个或多个进程或线程可以访问共享数据并且它们试图同时更改它们时，就会发生竞态情况。在我们的示例中，两个进程必须读取共享值，将其增加1，然后将其写回到共享变量中。如果这同时发生，则两个进程将读取相同的值，将其增加并写回。因此，两个进程都将相同的增加的值写回到共享对象中，并且该值未增加2。有关竞态条件的详细说明，请参见 [16. 多线程 — Python 进阶](https://www.notion.so/16-Python-1d15878dedcd42f18eed31799af94980) 。

### 避免带锁的竞态条件

锁（也称为互斥锁）是一种同步机制，用于在存在许多执行进程/线程的环境中强制限制对资源的访问。锁具有两种状态：锁定和解锁。如果状态为锁定，则在状态再次被解锁之前，不允许其他并发进程/线程进入此代码段。

两个函数很重要：

- `lock.acquire()`：这将锁定状态并阻塞
- `lock.release()`：这将再次解锁状态。

重要提示：块获得后，你应始终再次释放它！

在我们的示例中，读取并增加了共享变量的关键代码部分现已锁定。这样可以防止第二个进程同时修改共享库。我们的代码没有太大变化。所有新更改都在下面的代码中进行了注释。

```python
# import Lock
from multiprocessing import Lock
from multiprocessing import Process, Value, Array
import time

def add_100(number, lock):
    for _ in range(100):
        time.sleep(0.01)
        # lock the state
        lock.acquire()
        
        number.value += 1
        
        # 解锁状态
        lock.release()

def add_100_array(numbers, lock):
    for _ in range(100):
        time.sleep(0.01)
        for i in range(len(numbers)):
            lock.acquire()
            numbers[i] += 1
            lock.release()

if __name__ == "__main__":

    # 创建锁
    lock = Lock()
    
    shared_number = Value('i', 0) 
    print('Value at beginning:', shared_number.value)

    shared_array = Array('d', [0.0, 100.0, 200.0])
    print('Array at beginning:', shared_array[:])

    # 将锁传入目标函数
    process1 = Process(target=add_100, args=(shared_number, lock))
    process2 = Process(target=add_100, args=(shared_number, lock))

    process3 = Process(target=add_100_array, args=(shared_array, lock))
    process4 = Process(target=add_100_array, args=(shared_array, lock))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    print('Value at end:', shared_number.value)
    print('Array at end:', shared_array[:])

    print('end main')
```

```python
    Value at beginning: 0
    Array at beginning: [0.0, 100.0, 200.0]
    Value at end: 200
    Array at end: [200.0, 300.0, 400.0]
    end main
```

### 使用锁作为上下文管理器

在 `lock.acquire()` 之后，你应该永远不要忘记调用 `lock.release()` 来解锁代码。 你还可以将锁用作上下文管理器，这将安全地锁定和解锁你的代码。 建议以这种方式使用锁：

```python
def add_100(number, lock):
    for _ in range(100):
        time.sleep(0.01)
        with lock:
            number.value += 1
```

### 在Python中使用队列

数据也可以通过队列在进程之间共享。 队列可用于多线程和多进程环境中的线程安全/进程安全数据交换和数据处理，这意味着你可以避免使用任何同步原语（例如锁）。

队列
队列是遵循先进先出（FIFO）原理的线性数据结构。 一个很好的例子是排队等候的客户队列，其中首先服务的是第一位的客户。

```python
from multiprocessing import Queue

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

### 在多进程中使用队列

带有队列的操作是进程安全的。 除了 `task_done()` 和 `join()` 之外，多进程队列实现了 `queue.Queue` 的所有方法。 重要方法是：

- `q.get()`：删除并返回第一项。 默认情况下，它会阻塞，直到该项可用为止。
- `q.put(item)`：将元素放在队列的末尾。 默认情况下，它会阻塞，直到有空闲插槽可用为止。
- `q.empty()`：如果队列为空，则返回True。
- `q.close()`：指示当前进程不会再将更多数据放入此队列。

```python
# 使用多进程队列在进程之间进行通信
# 队列是线程和进程安全的
from multiprocessing import Process, Queue

def square(numbers, queue):
    for i in numbers:
        queue.put(i*i)

def make_negative(numbers, queue):
    for i in numbers:
        queue.put(i*-1)

if __name__ == "__main__":
    
    numbers = range(1, 6)
    q = Queue()

    p1 = Process(target=square, args=(numbers,q))
    p2 = Process(target=make_negative, args=(numbers,q))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # 顺序可能不是按序列的
    while not q.empty():
        print(q.get())
        
    print('end main')
```

```python
    1
    4
    9
    16
    25
    -1
    -2
    -3
    -4
    -5
    end main
```

### 进程池

进程池对象控制可以向其提交作业的工作进程池。它支持带有超时和回调的异步结果，并具有并行映射实现。它可以自动管理可用的处理器，并将数据拆分为较小的块，然后由不同的进程并行处理。有关所有可能的方法，请参见 [https://docs.python.org/3.7/library/multiprocessing.html#multiprocessing.pool](https://docs.python.org/3.7/library/multiprocessing.html#multiprocessing.pool)。重要方法有

- `map(func, iterable[, chunksize])`：此方法将 Iterable 分成许多块，作为单独的任务提交给进程池。这些块的（大约）大小可以通过将 chunksize 设置为正整数来指定。它会阻塞，直到结果准备好为止。
- `close()`：阻止将更多任务提交到池中。一旦完成所有任务，工作进程将退出。
- `join()`：等待工作进程退出。使用 `join()` 之前，必须先调用 `close()` 或 `terminate()`。
- `apply(func, args)`：使用参数args调用func。它会阻塞，直到结果准备好为止。 func仅在池的一个工作程序中执行。

注意：也有不会阻塞的异步变体 `map_async()` 和 `apply_async()`。结果准备好后，他们可以执行回调。

```python
from multiprocessing import Pool 

def cube(number):
    return number * number * number

    
if __name__ == "__main__":
    numbers = range(10)
    
    p = Pool()

    # 默认情况下，这将分配此任务的最大可用处理器数 --> os.cpu_count()
    result = p.map(cube,  numbers)
    
    # or 
    # result = [p.apply(cube, args=(i,)) for i in numbers]
    
    p.close()
    p.join()
    
    print(result)
```

```python
    [0, 1, 8, 27, 64, 125, 216, 343, 512, 729]
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

