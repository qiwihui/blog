---
title: "《编写高质量Python代码的59个有效方法》笔记"
description: "《编写高质量Python代码的59个有效方法》笔记"
tags: 
- Python
- tips
top: 79
date: 09/01/2020, 11:42:26
author: qiwihui
update: 09/01/2020, 12:33:54
categories: 
---

### 1. Python版本

- Python 3
- CPython, PyPy, Jython, IronPython

### 2. PEP8

代码风格一致

### 3. bytes，str，unicode（只讨论Python 3）

Python 3中：bytes实例包含原始的8位值，str实例包含Unicode字符。把Unicode字符表示为二进制数据，最常见的编码方式是UTF-8。

- Unicode 字符 => 二进制：`encode`
- 二进制 => Unicode 字符：`decode`

<!--more-->

Python程序中，一定要把编码和解码放在最外围来操作。程序的核心部分应该使用Unicode字符类型，而且不要对字符编码做任何假设。

定义 `to_str` 和 `to_bytes` 方法。

Python 3中，`open`默认以`utf-8`编码打开，而不是二进制。

### 4. 用辅助函数来取代复杂表达式

### 5. 序列切片

1. `list`，`str`，`bytes` 以及实现了 `__getitem__` 和 `__setitem__`  的类；
2. 切片时下表可以越界，但访问元素时不能；
3. 当start索引为0或者end索引为列序列长度时，应该将其省略；
4. 对list赋值时，使用切片会把原序列相关范围的值替换成新值，即使长度不一样；

```shell
>>> a = [1,2,3,4,5,6,7]
>>> a[1:6] = [9]
>>> a
[1,9,7]
```

### 6. 步进式切割

1. 避免在一个切片操作中同时使用 `start`，`end`和`stride`；
2. 避免使用负数做stride；

### 7. 用列表推导代替map和filter

1. list, 字典和集合支持列表推导；
2. 代码清晰；

### 8. 不要使用含有两个以上表达式的列表推导

会变得难理解

### 9. 用生成器表达式来改写数据量较大的列表推导式

1. 数据量较大时，列表推导式会占用大量内存

2. `()`

```py
a_long_list = [1,2,3,4,5]
value = [len(x) for x in a_long_list]
print(value)
```

=>

```py
value = (len(x) for x in a_long_list)
print(next(value))
```

3. 可以组合

```py
roots = ((v, v ** 0.5)for v in value)
print(next(roots))
```

### 10. `range` => `enumerate`

`enumerate` 可以把各种迭代器包装成生成器，以便稍后产生输出值。
`enumerate` 计数下表默认从 `0` 开始，可以修改。

### 11. 用 `zip` 同是遍历两个迭代器

1. 迭代器长度相同
2. 不同时使用 `itertools.zip_longest`

### 12. 不要在 `for` 和 `while` 循环后面写 `else`

与 `if/else`, `try/except/else` 的 `else` 不同，容易误解

### 13. `try/except/else/finally`

1. `finally`块：既要将异常向上传播，又要在异常发生时做清理工作
2. `ry/except/else`：except使异常传播变得清晰，else便于自己处理代码

### 14. 尽量用异常来表示特殊情况，而不要返回 `None`

比如除以0时，抛出异常

### 15. 在闭包中使用外围作用域中的变量

1. Python3 获取闭包中的变量：`nonlocal`，但是`nonlocal`不能延伸到模块级别；
2. Python2 中可以使用可变值来实现，比如包含单个元素的列表。
3. 除非函数简单，尽量不使用 `nonlocal`

### 16. 考虑用生成器改写直接返回列表的函数

`yield`

### *17. 在参数上迭代时需要多加小心*

1. 参数是迭代器时要多加注意；
2. 迭代器协议：容器和迭代器，`iter`，`next`
3. `__iter__`
4. 判断是否为迭代器：`iter(target) == iter(target)` 为True，则为迭代器

### 18. 用数量可变的位置参数减少视觉混乱

1. 星号参数（`*args`），`*`操作符
2. 变长参数在传给函数时，总是先转化成元组，如果是生成器，注意内存使用；
3. 添加新参数时，需要修改原来函数使用。可使用关键字形式指定的参数解决这个问题。

### 19. 用关键字参数表达可选行为

1. 位置参数必必须出现在关键字之前；每个参数只能指定一次；
2. 关键字参数；易读，可提供默认值，扩充参数方便；

### 20. 用`None`和文档字符串描述具有动态默认值的参数

1. 参数的默认值，只会在程序加载模块并读到本函数的定义时评估一次，对于`{}`，`[]`等动态值会出现奇怪行为。

### 21. 用只能以关键值形式指定的参数来确保代码明晰

Python 3 中：

```py
def safe_division_before(number, divisor, ignore_overflow=False, ignore_zero_divisor=False):
    ...
```

==>

```py
def safe_division_after(number, divisor, *, ignore_overflow=False, ignore_zero_divisor=False):
    ...
```

`*` 标识着位置参数结束，之后的参数只能以关键字形式指定。

### 22. 尽量用辅助类来维护程序状态，而不用字典和元组

1. 不使用包含字典的字典或者过长的元组；
2. 具名元组：`collections.namedtuple`；

### 23. 简单的接口应该接受函数，而不是类的实例

1. Python中的函数是一级对象，函数和方法可以像语言中的其他值那样传递和引用；
2. 举例：
    - `list`类型的`sort`方法
    - `defaultdict`
3. `__call__` 使类的实例像普通函数那样调用；
4. 如果要用函数保存状态，就应该定义新的类，并令其实现 `__call__` 方法，而不要定义带状态的闭包。

### 24. 以 `@classmedtod` 形式的多态去通用地构建对象

1. 每个类只能有一个构造器，即 `__init__`；
2. `@@classmedtod` 机制可以用一种与构造器相似的方式构造类对象；

### 25. 用 `super` 初始化父类

1. Python采用标准的方法解析解析顺序来解决 *超类初始化次序* 和 *菱形继承问题*；
2. `super` 在Python2和Python3不一致；

Python 3 中以下两种方式效果相同

```py
class Explicit(MyBaseClass):

    def __init__(self, value):
        super(__class__, self).__init__(value)

class Implicit(MyBaseClass):

    def __init__(self, value):
        super().__init__(value)
```

3. 总是应该使用内置的 `super` 函数来初始化父类；
4. 类的 `mro` 方法可以查看方法解析顺序：`MyClass.mro()`

### 26. 只在使用 Mix-in 组件制作工具类时进行多重继承

1. mix-in 是一种小型类，它只定义了其他类可能需要提供的一套附加方法，而不定义自己的实例属性，它也不要求使用者调用自己的 `__init__` 构造器；
2. 能用 mix-in 组件实现的效果，就不要用多重继承来做；
3. 将各个功能实现为可插拔的 mix-in 组件，然后让相关类继承自己需要的组件，即可定制该类实例所应具备的行为；
4. 简单行为封装到 mix-in 组件中，然后用多个组件组合出复杂功能。

### 27. 多用 public 属性，少用 private 属性

1. Python解释器无法严格保证 private 字段的私密性（Python中会将类的 private 属性名称变化为 `_{类名称}__{原private属性名称}`）；
2. 不要盲目将属性设置为 private，而是一开始就做好规划，并允许子类更多地访问超类内部API；
3. 多用 protected 属性，并在文档中将这些字段的合理用法告诉开发者，而不要试图用 private 属性来限制子类访问；
4. 只有当子类不受自己控制时，才可考虑使用 private 属性避免冲突。

### 28. 继承 `collections.abc` 以实现自定义容器类型

编写自定义容器类型时，从 `collections.abc` 模块的抽象基类中继承，那些基类可以确保子类具有适当的接口和行为。

### 49. 为每个函数、类和模块编写文档字符串

1. docstring

### 54. 模块级别代码配置不同的部署环境

1. 环境变量
2. `os`，`sys`

### 55. 用 `repr` 输出调试信息

1. `print` 易于阅读字符串
2. `repr` 可供打印字符串，`eval` 还原为初始值
3. 格式化字符串：`%s` => str; `%r` => repr
4. `__repr__` 自定义可供打印字符串；
5. `__dict__` 任意对象查询实例字典；

示例：

```shell
>>> print(5)
5
>>> print('5')
5
>>> print(repr(5))
5
>>> print(repr('5'))
'5'
>>> print('%s' % 5)
5
>>> print('%s' % '5')
5
>>> print('%r' % 5)
5
>>> print('%r' % '5')
'5'
```

### 56. unittest 测试

要确保 Python 程序能正常运行，唯一的方法就是编写测试。
Python 语言动态特性，一方面阻碍了静态类型检测，另一方面却有利于开发者进行测试。

1. 断言（assertion）：`assertEqual`，`assertTrue`，`assertRaises`
2. mock
3. `setUp`，`tearDown`
4. 单元测试，集成测试

### 57. `pdb` 交互调试

`import pdb; pdb.set_trace()`

1. `bt`，`up`，`down`
2. `step`，`next`，`return`，`continue`

### 58. 性能分析

1. Python 性能分析工具 `profile`：`profile`，`cProfile`
2. `runcall`
3. `Stats`

### 59. `tracemalloc` 内存使用及泄漏

CPyhton：引用计数，gc

1. `gc.get_objects()`
2. `tracemalloc.take_snapshot()`


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

