---
title: "13. 装饰器 — Python 进阶"
description: "13. 装饰器 — Python 进阶"
tags: 
- 技术
- Python
top: 127
date: 26/03/2021, 14:39:08
author: qiwihui
update: 30/03/2021, 10:21:32
categories: 技术
---

装饰器是一个函数，它接受另一个函数并扩展该函数的行为而无需显式修改它。 这是一个非常强大的工具，可以将新功能添加到现有函数中。

装饰器有2种：

- 函数装饰器
- 类装饰器

函数用 `@` 符号修饰：

```python
@my_decorator
def my_function():
    pass
```

<!--more-->

### 函数装饰器

为了理解装饰器模式，我们必须了解Python中的函数是一级对象，这意味着像其他任何对象一样，它们可以在另一个函数内定义，作为参数传递给另一个函数或从其他函数返回 。 装饰器是一个将另一个函数作为参数的函数，将其行为包装在内部函数中，并返回包装的函数。 结果，修饰的函数便具有了扩展的功能！

```python
# 装饰器是一个将另一个函数作为参数的函数，将其行为包装在内部函数中，并返回包装的函数。
def start_end_decorator(func):
    
    def wrapper():
        print('Start')
        func()
        print('End')
    return wrapper

def print_name():
    print('Alex')
    
print_name()

print()

# 现在通过将其作为参数传递给装饰器函数并将其赋值给自身来包装该函数->我们的函数已扩展了行为！
print_name = start_end_decorator(print_name)
print_name()
```

```python
    Alex

    Start
    Alex
    End
```

### 装饰器语法

除了包装函数并将其分配给自身之外，我们还可以通过用 `@` 装饰函数来实现相同的目的。

```python
@start_end_decorator
def print_name():
    print('Alex')
    
print_name()
```

```python
    Start
    Alex
    End
```

### 关于函数参数

如果我们的函数具有输入参数，并且我们尝试使用上面的装饰器将其包装，则它将引发 `TypeError`，因为我们在包装器内调用函数时也必须使用此参数。 但是，我们可以通过在内部函数中使用 `*args` 和 `**kwargs` 来解决此问题：

```python
def start_end_decorator_2(func):
    
    def wrapper(*args, **kwargs):
        print('Start')
        func(*args, **kwargs)
        print('End')
    return wrapper

@start_end_decorator_2
def add_5(x):
    return x + 5

result = add_5(10)
print(result)
```

```python
    Start
    End
    None
```

### 返回值

请注意，在上面的示例中，我们没有取回结果，因此，下一步，我们还必须从内部函数返回值：

```python
def start_end_decorator_3(func):
    
    def wrapper(*args, **kwargs):
        print('Start')
        result = func(*args, **kwargs)
        print('End')
        return result
    return wrapper

@start_end_decorator_3
def add_5(x):
    return x + 5

result = add_5(10)
print(result)
```

```python
    Start
    End
    15
```

### 函数标识又如何变化呢？

如果我们看一下装饰函数的名称，并使用内置的 `help` 函数对其进行检查，我们会注意到Python认为我们的函数现在是装饰器函数的包装内部函数。

```python
print(add_5.__name__)
help(add_5)
```

```python
    wrapper
    Help on function wrapper in module __main__:

    wrapper(*args, **kwargs)
```

要解决此问题，请使用 `functools.wraps` 装饰器，该装饰器将保留有关原始函数的信息。 这有助于进行自省，即对象在运行时了解其自身属性的能力：

```python
import functools
def start_end_decorator_4(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('Start')
        result = func(*args, **kwargs)
        print('End')
        return result
    return wrapper

@start_end_decorator_4
def add_5(x):
    return x + 5
result = add_5(10)
print(result)
print(add_5.__name__)
help(add_5)
```

```python
    Start
    End
    15
    add_5
    Help on function add_5 in module __main__:

    add_5(x)
```

### 装饰器的最终模板

现在，我们已经有了所有部分，用于任何装饰器的模板如下所示：

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper
```

### 装饰器函数参数

请注意， `functools.wraps` 是一个装饰器，它自己接受一个参数。 我们可以将其视为2个内部函数，即内部函数里的内部函数。 为了更清楚地说明这一点，我们来看另一个示例：以数字作为输入的 `repeat` 装饰器。 在此函数内，我们有实际的装饰函数，该函数包装函数并在另一个内部函数内扩展其行为。 在这种情况下，它将输入函数重复给定的次数。

```python
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")
    
greet('Alex')
```

```python
    Hello Alex
    Hello Alex
    Hello Alex
```

### 嵌套装饰器

我们可以通过将多个装饰器彼此堆叠来将其应用到一个函数。 装饰器将按照其列出的顺序执行。

```python
# 装饰器函数，它输出有关包装函数的调试信息
def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}")
        return result
    return wrapper

@debug
@start_end_decorator_4
def say_hello(name):
    greeting = f'Hello {name}'
    print(greeting)
    return greeting

# 现在 `debug` 先执行，然后调用 `@start_end_decorator_4`，后者优惠调用 `say_hello`
say_hello(name='Alex')
```

```python
    Calling say_hello(name='Alex')
    Start
    Hello Alex
    End
    'say_hello' returned 'Hello Alex'
```

### 类装饰器

我们也可以使用一个类作为装饰器。 因此，我们必须实现 `__call__()` 方法以使我们的对象可调用。 类装饰器通常用于维护状态，例如： 在这里，我们跟踪函数执行的次数。 `__call__`方法与我们之前看到的 `wrapper()` 方法本质上是相同的。 它添加了一些功能，执行了该函数，并返回其结果。 请注意，这里我们使用 `functools.update_wrapper()` 代替 `functools.wraps` 来保留有关函数的信息。

```python
import functools

class CountCalls:
    # 初始化需要以func作为参数并将其存储
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0
    
    # 扩展功能，执行函数并返回结果
    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello(num):
    print("Hello!")
    
say_hello(5)
say_hello(5)
```

```python
    Call 1 of 'say_hello'
    Hello!
    Call 2 of 'say_hello'
    Hello!
```

### 一些典型的用例

- 使用计时器装饰器来计算函数的执行时间
- 使用调试装饰器来打印出有关被调用函数及其参数的更多信息
- 使用检查修饰符检查参数是否满足某些要求并相应地调整行为
- 注册函数（插件）
- 使用 `time.sleep()` 降低代码速度以检查网络行为
- 缓存返回值以进行记忆化（[https://en.wikipedia.org/wiki/Memoization）](https://en.wikipedia.org/wiki/Memoization%EF%BC%89)
- 添加信息或更新状态

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

