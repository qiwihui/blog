# 21. 上下文管理器 — Python 进阶


上下文管理器是资源管理的绝佳工具。 它们使你可以在需要时精确地分配和释放资源。 一个著名的例子是 `with open()` 语句：

```python
with open('notes.txt', 'w') as f:
    f.write('some todo...')
```

这将打开一个文件，并确保在程序执行离开with语句的上下文之后自动将其关闭。 它还处理异常，并确保即使在发生异常的情况下也能正确关闭文件。 在内部，上面的代码翻译成这样的东西：

```python
f = open('notes.txt', 'w')
try:
    f.write('some todo...')
finally:
    f.close()
```

我们可以看到，使用上下文管理器和 `with` 语句更短，更简洁。

<!--more-->

### 上下文管理器示例

- 打开和关闭文件
- 打开和关闭数据库连接
- 获取和释放锁：

```python
from threading import Lock
lock = Lock()

# 容易出错:
lock.acquire()
# 做一些操作
# 锁应始终释放！
lock.release()

# 更好：
with lock:
    # 做一些操作
```

### 将上下文管理器实现为类

为了支持我们自己的类的 `with` 语句，我们必须实现 `__enter__` 和 `__exit__` 方法。 当执行进入 `with` 语句的上下文时，Python调用 `__enter__`。 在这里，应该获取资源并将其返回。 当执行再次离开上下文时，将调用 `__exit__` 并释放资源。

```python
class ManagedFile:
    def __init__(self, filename):
        print('init', filename)
        self.filename = filename

    def __enter__(self):
        print('enter')
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file:
            self.file.close()
        print('exit')

with ManagedFile('notes.txt') as f:
    print('doing stuff...')
    f.write('some todo...')
```

```python
    init notes.txt
    enter
    doing stuff...
    exit
```

### 处理异常

如果发生异常，Python将类型，值和回溯传递给 `__exit__` 方法。 它可以在这里处理异常。 如果 `__exit__` 方法返回的不是 `True`，则 `with` 语句将引发异常。

```python
class ManagedFile:
    def __init__(self, filename):
        print('init', filename)
        self.filename = filename

    def __enter__(self):
        print('enter')
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file:
            self.file.close()
        print('exc:', exc_type, exc_value)
        print('exit')

# 没有异常
with ManagedFile('notes.txt') as f:
    print('doing stuff...')
    f.write('some todo...')
print('continuing...')

print()

# 异常触发，但是文件仍然能被关闭
with ManagedFile('notes2.txt') as f:
    print('doing stuff...')
    f.write('some todo...')
    f.do_something()
print('continuing...')
```

```python
    init notes.txt
    enter
    doing stuff...
    exc: None None
    exit
    continuing...

    init notes2.txt
    enter
    doing stuff...
    exc: <class 'AttributeError'> '_io.TextIOWrapper' object has no attribute 'do_something'
    exit

    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-24-ed1604efb530> in <module>
         27     print('doing stuff...')
         28     f.write('some todo...')
    ---> 29     f.do_something()
         30 print('continuing...')
    AttributeError: '_io.TextIOWrapper' object has no attribute 'do_something'
```

我们可以在 `__exit__` 方法中处理异常并返回 `True`。

```python
class ManagedFile:
    def __init__(self, filename):
        print('init', filename)
        self.filename = filename

    def __enter__(self):
        print('enter')
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file:
            self.file.close()
        if exc_type is not None:
            print('Exception has been handled')
        print('exit')
        return True

with ManagedFile('notes2.txt') as f:
    print('doing stuff...')
    f.write('some todo...')
    f.do_something()
print('continuing...')
```

```python
    init notes2.txt
    enter
    doing stuff...
    Exception has been handled
    exit
    continuing...
```

### 将上下文管理器实现为生成器

除了编写类，我们还可以编写一个生成器函数，并使用 `contextlib.contextmanager` 装饰器对其进行装饰。 然后，我们也可以使用 `with` 语句调用该函数。 对于这种方法，函数必须在 `try` 语句中 `yield` 资源，并且释放资源的 `__exit__` 方法的所有内容现在都在相应的 `finally` 语句内。

```python
from contextlib import contextmanager

@contextmanager
def open_managed_file(filename):
    f = open(filename, 'w')
    try:
        yield f
    finally:
        f.close()

with open_managed_file('notes.txt') as f:
    f.write('some todo...')
```

生成器首先获取资源。 然后，它暂时挂起其自己的执行并 *产生* 资源，以便调用者可以使用它。 当调用者离开 `with` 上下文时，生成器继续执行并释放 `finally` 语句中的资源。

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/132)


