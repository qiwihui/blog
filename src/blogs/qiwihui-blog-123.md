---
title: "06. collections — Python 进阶"
description: "06. collections — Python 进阶"
tags: 
- 技术
- Python
top: 123
date: 25/03/2021, 14:07:26
author: qiwihui
update: 29/03/2021, 15:19:28
categories: 技术
---

Python 中的 `collections` 模块实现了专门的容器数据类型，提供了 Python 通用内置容器dict，list，set和tuple的替代方案。

包含以下工具：

- `namedtuple`：用于创建具有命名字段的元组子类的工厂函数
- `OrderedDict`：用于记住条目添加顺序的dict子类
- `Counter`：用于计算可哈希对象的dict子类
- `defaultdict`：调用工厂函数以提供缺失值的dict子类
- `deque`： 列表式容器，支持两端都有快速追加和弹出

在Python 3中，还存在其他一些模块（ChainMap，UserDict，UserList，UserString）。 有关更多参考，请参见 [https://docs.python.org/3/library/collections.html](https://docs.python.org/3/library/collections.html)。

<!--more-->

### Counter

计数器是一个将元素存储为字典键的容器，而它们的计数则存储为字典值。

```python
from collections import Counter
a = "aaaaabbbbcccdde"
my_counter = Counter(a)
print(my_counter)

print(my_counter.items())
print(my_counter.keys())
print(my_counter.values())

my_list = [0, 1, 0, 1, 2, 1, 1, 3, 2, 3, 2, 4]
my_counter = Counter(my_list)
print(my_counter)

# 出现最多的元素
print(my_counter.most_common(1))

# 返回元素的迭代器，每个元素重复其计数次数
# 元素返回顺序任意
print(list(my_counter.elements()))
```

```python
    Counter({'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1})
    dict_items([('a', 5), ('b', 4), ('c', 3), ('d', 2), ('e', 1)])
    dict_keys(['a', 'b', 'c', 'd', 'e'])
    dict_values([5, 4, 3, 2, 1])
    Counter({1: 4, 2: 3, 0: 2, 3: 2, 4: 1})
    [(1, 4)]
    [0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
```

### namedtuple

`namedtuple` 是容易创建，轻量级的对象类型。 它们为元组中的每个位置分配含义，并允许使用更具可读性的带文档代码。 它们可以在使用常规元组的任何地方使用，并且它们增加了按名称而不是位置索引访问字段的能力。

```python
from collections import namedtuple
# 创建一个namedtuple，其类名称为string，其字段为string
# 给定字符串中的字段必须用逗号或空格分隔
Point = namedtuple('Point','x, y')
pt = Point(1, -4)
print(pt)
print(pt._fields)
print(type(pt))
print(pt.x, pt.y)

Person = namedtuple('Person','name, age')
friend = Person(name='Tom', age=25)
print(friend.name, friend.age)
```

```python
    Point(x=1, y=-4)
    ('x', 'y')
    <class '__main__.Point'>
    1 -4
    Tom 25
```

### OrderedDict

OrderedDict 就像常规dict一样，但是它们记住条目插入的顺序。 在 OrderedDict 上进行迭代时，将按照条目的键首次添加的顺序返回项。 如果新条目覆盖了现有条目，则原始插入位置将保持不变。 既然内置dict类获得了记住插入顺序的能力（自python 3.7起），它们的重要性就变得不那么重要了。 但是仍然存在一些差异，例如 OrderedDict 被设计为擅长重新排序操作。

```python
from collections import OrderedDict
ordinary_dict = {}
ordinary_dict['a'] = 1
ordinary_dict['b'] = 2
ordinary_dict['c'] = 3
ordinary_dict['d'] = 4
ordinary_dict['e'] = 5
# 在Python 3.7之前，这个可能是任意顺序
print(ordinary_dict)

ordered_dict = OrderedDict()
ordered_dict['a'] = 1
ordered_dict['b'] = 2
ordered_dict['c'] = 3
ordered_dict['d'] = 4
ordered_dict['e'] = 5
print(ordered_dict)
# 与普通dict具有相同的功能，但始终有序
for k, v in ordinary_dict.items():
    print(k, v)
```

```python
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])
    a 1
    b 2
    c 3
    d 4
    e 5
```

### defaultdict

defaultdict是一个与通常的dict容器相似的容器，但是唯一的区别是，如果尚未设置该键，则defaultdict将具有默认值。 如果不使用defaultdict，则你必须检查该键是否存在，如果不存在，则将其设置为所需的键。

```python
from collections import defaultdict

# 初始化一个默认int值，即 0
d = defaultdict(int)
d['yellow'] = 1
d['blue'] = 2
print(d.items())
print(d['green'])

# 初始化一个默认列表值，即空列表
d = defaultdict(list)
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 5)]
for k, v in s:
    d[k].append(v)

print(d.items())
print(d['green'])
```

```python
    dict_items([('yellow', 1), ('blue', 2)])
    0
    dict_items([('yellow', [1, 3]), ('blue', [2, 4]), ('red', [5])])
    []
```

### deque

deque是双端队列。 它可用于在两端添加或删除元素。 deque支持从队列的任一侧线程安全，内存高效地追加和弹出，在任一方向上大致相同的 `O(1)` 性能。 更常用的栈和队列是双端队列的退化形式，其中输入和输出限制为单端。

```python
from collections import deque
d = deque()

# append() : 添加元素到右端
d.append('a')
d.append('b')
print(d)

# appendleft() : 添加元素到左端
d.appendleft('c')
print(d)

# pop() : 返回并删除右端元素
print(d.pop())
print(d)

# popleft() : 返回并删除左端元素
print(d.popleft())
print(d)

# clear() : 删除所有元素
d.clear()
print(d)

d = deque(['a', 'b', 'c', 'd'])

# 在右端或者左端扩展
d.extend(['e', 'f', 'g'])
d.extendleft(['h', 'i', 'j']) # 主语 'j' 现在在最左侧 
print(d)

# count(x) : 返回找到的元素个数
print(d.count('h'))

# 向右旋转1个位置
d.rotate(1)
print(d)

向左旋转2个位置
d.rotate(-2)
print(d)
```

```python
    deque(['a', 'b'])
    deque(['c', 'a', 'b'])
    b
    deque(['c', 'a'])
    c
    deque(['a'])
    deque([])
    deque(['j', 'i', 'h', 'a', 'b', 'c', 'd', 'e', 'f', 'g'])
    1
    deque(['g', 'j', 'i', 'h', 'a', 'b', 'c', 'd', 'e', 'f'])
    deque(['i', 'h', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'j'])
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

