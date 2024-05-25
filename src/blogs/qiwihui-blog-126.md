---
title: "09. 异常和错误 — Python 进阶"
description: "09. 异常和错误 — Python 进阶"
tags: 
- 技术
- Python
top: 126
date: 25/03/2021, 18:19:49
author: qiwihui
update: 29/03/2021, 15:16:21
categories: 技术
---

Python程序在遇到错误后立即终止。在Python中，错误可以是语法错误或异常。 在本文中，我们将关注以下内容：

- 语法错误与异常
- 如何抛出异常
- 如何处理异常
- 常见的内置异常
- 如何定义自己的异常

<!--more-->

### 语法错误

当解析器检测到语法不正确的语句时发生语法错误。 语法错误可以是例如拼写错误，缺少括号，没有新行（请参见下面的代码）或错误的标识（这实际上会引发它自己的IndentationError，但它是SyntaxError的子类）。

```python
a = 5 print(a)
```

```python
    File "<ipython-input-5-fed4b61d14cd>", line 1
    a = 5 print(a)
                  ^
    SyntaxError: invalid syntax
```

### 异常

即使一条语句在语法上是正确的，执行该语句也可能导致错误，这称为 **异常错误**。 有几种不同的错误类别，例如，尝试对数字和字符串求和将引发 `TypeError`。

```python
a = 5 + '10'
```

```python
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-6-893398416ed7> in <module>
    ----> 1 a = 5 + '10'

    TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

### 抛出异常

如果要在满足特定条件时强制发生异常，则可以使用 `raise` 关键字。

```python
x = -5
if x < 0:
    raise Exception('x should not be negative.')
```

```python
    ---------------------------------------------------------------------------
    Exception                                 Traceback (most recent call last)
    <ipython-input-4-2a9e7e673803> in <module>
          1 x = -5
          2 if x < 0:
    ----> 3     raise Exception('x should not be negative.')

    Exception: x should not be negative.
```

你还可以使用 `assert` 语句，如果你的断言**不是** `True`，则将引发 `AssertionError`。 这样，你可以主动测试必须满足的某些条件，而不必等待程序中途崩溃。 断言还用于**单元测试**。

```python
x = -5
assert (x >= 0), 'x is not positive.'
# --> 如果 x >= 0，代码将正常运行
```

```python
    ---------------------------------------------------------------------------
    AssertionError                            Traceback (most recent call last)
    <ipython-input-7-f9b059c51e45> in <module>
          1 x = -5
    ----> 2 assert (x >= 0), 'x is not positive.'
          3 # --> Your code will be fine if x >= 0
    AssertionError: x is not positive.
```

### 处理异常

你可以使用 `try` 和 `except` 块来捕获和处理异常。 如果你可以捕获异常，则你的程序将不会终止，并且可以继续。

```python
# 这将捕获所有可能的异常
try:
    a = 5 / 0
except:
    print('some error occured.')
    
# 可以捕获异常类型
try:
    a = 5 / 0
except Exception as e:
    print(e)
    
# 最好指定要捕获的异常类型
# 因此，你必须知道可能的错误
try:
    a = 5 / 0
except ZeroDivisionError:
    print('Only a ZeroDivisionError is handled here')
    
# 你可以在try块中运行多个语句，并捕获不同的可能的异常
try:
    a = 5 / 1 # 注意：这里没有 ZeroDivisionError
    b = a + '10'
except ZeroDivisionError as e:
    print('A ZeroDivisionError occured:', e)
except TypeError as e:
    print('A TypeError occured:', e)
```

```python
    Some error occured.
    Division by zero
    Only a ZeroDivisionError is handled here
    A TypeError occured: unsupported operand type(s) for +: 'float' and 'str'
```

### `else` 语句

如果没有发生异常，则可以使用else语句运行。

```python
try:
    a = 5 / 1
except ZeroDivisionError as e:
    print('A ZeroDivisionError occured:', e)
else:
    print('Everything is ok')
```

```python
    Everything is ok
```

### `finally` 语句

你可以使用始终运行的 `finally` 语句，无论是否存在异常。 例如，这可用于进行一些清理操作。

```python
try:
    a = 5 / 1 # 注意：这里没有 ZeroDivisionError
    b = a + '10'
except ZeroDivisionError as e:
    print('A ZeroDivisionError occured:', e)
except TypeError as e:
    print('A TypeError occured:', e)
else:
    print('Everything is ok')
finally:
    print('Cleaning up some stuff...')
```

```python
    A TypeError occured: unsupported operand type(s) for +: 'float' and 'str'
    Cleaning up some stuff...
```

### 常见的内置异常

你可以在此处找到所有内置的异常：[https://docs.python.org/3/library/exceptions.html](https://docs.python.org/3/library/exceptions.html)

- `ImportError`：如果无法导入模块
- `NameError`：如果你尝试使用未定义的变量
- `FileNotFoundError`：如果你尝试打开一个不存在的文件或指定了错误的路径
- `ValueError`：当某个操作或函数收到类型正确但值不正确的参数时，例如尝试从不存在的列表中删除值
- `TypeError`：将操作或函数应用于不适当类型的对象时引发。
- `IndexError`：如果你尝试访问序列的无效索引，例如列表或元组。
- `KeyError`：如果你尝试访问字典中不存在的键。

```python
# ImportError
import nonexistingmodule

# NameError
a = someundefinedvariable

# FileNotFoundError
with open('nonexistingfile.txt') as f:
    read_data = f.read()

# ValueError
a = [0, 1, 2]
a.remove(3)

# TypeError
a = 5 + "10"

# IndexError
a = [0, 1, 2]
value = a[5]

# KeyError
my_dict = {"name": "Max", "city": "Boston"}
age = my_dict["age"]
```

### 如何定义自己的异常

你可以定义自己的异常类，该异常类应从内置的 `Exception` 类派生。 与标准异常的命名类似，大多数异常都以“错误”结尾的名称定义。 可以像定义其他任何类一样定义异常类，但是它们通常保持简单，通常仅提供一定数量的属性，这些属性允许处理程序提取有关错误的信息。

```python
# 自定义异常类的最小示例
class ValueTooHighError(Exception):
    pass

# 或者为处理者添加一些信息
class ValueTooLowError(Exception):
    def __init__(self, message, value):
        self.message = message
        self.value = value

def test_value(a):
    if a > 1000:
        raise ValueTooHighError('Value is too high.')
    if a < 5:
        raise ValueTooLowError('Value is too low.', a) # 注意，构造器接受两个参数
    return a

try:
    test_value(1)
except ValueTooHighError as e:
    print(e)
except ValueTooLowError as e:
    print(e.message, 'The value is:', e.value)
```

```python
    Value is too low. The value is: 1
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

