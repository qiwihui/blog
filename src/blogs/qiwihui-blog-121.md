---
title: "04. 集合 — Python 进阶"
description: "04. 集合 — Python 进阶"
tags: 
- 技术
- Python
top: 121
date: 22/03/2021, 10:48:28
author: qiwihui
update: 29/03/2021, 15:20:01
categories: 技术
---

集合是无序的容器数据类型，它是无索引的，可变的并且没有重复的元素。 集合用大括号创建。

```python
my_set = {"apple", "banana", "cherry"}
```

<!--more-->

### 创建集合

使用花括号或内置的 `set` 函数。

```python
my_set = {"apple", "banana", "cherry"}
print(my_set)

# 或者使用 set 函数从可迭代对象创建，比如列表，元组，字符串
my_set_2 = set(["one", "two", "three"])
my_set_2 = set(("one", "two", "three"))
print(my_set_2)

my_set_3 = set("aaabbbcccdddeeeeeffff")
print(my_set_3)

# 注意：一个空的元组不能使用 {} 创建，这个会识别为字典
# 使用 set() 进行创建
a = {}
print(type(a))
a = set()
print(type(a))
```

```python
    {'banana', 'apple', 'cherry'}
    {'three', 'one', 'two'}
    {'b', 'c', 'd', 'e', 'f', 'a'}
    <class 'dict'>
    <class 'set'>
```

### 添加元素

```python
my_set = set()

# 使用 add() 方法添加元素
my_set.add(42)
my_set.add(True)
my_set.add("Hello")

# 注意：顺序不重要，只会影响打印输出
print(my_set)

# 元素已经存在是没有影响
my_set.add(42)
print(my_set)
```

```python
    {True, 42, 'Hello'}
    {True, 42, 'Hello'}
```

### 移除元素

```python
# remove(x): 移除 x, 如果元素不存在则引发 KeyError 错误
my_set = {"apple", "banana", "cherry"}
my_set.remove("apple")
print(my_set)

# KeyError:
# my_set.remove("orange")

# discard(x): 移除 x, 如果元素不存在则什么也不做
my_set.discard("cherry")
my_set.discard("blueberry")
print(my_set)

# clear() : 移除所有元素
my_set.clear()
print(my_set)

# pop() : 移除并返回随机一个元素
a = {True, 2, False, "hi", "hello"}
print(a.pop())
print(a)
```

```python
    {'banana', 'cherry'}
    {'banana'}
    set()
    False
    {True, 2, 'hi', 'hello'}
```

### 检查元素是否存在

```python
my_set = {"apple", "banana", "cherry"}
if "apple" in my_set:
    print("yes")
```

```python
    yes
```

### 迭代

```python
# 使用 for 循环迭代集合
# 注意：顺序不重要
my_set = {"apple", "banana", "cherry"}
for i in my_set:
    print(i)
```

```python
    banana
    apple
    cherry
```

### 并集和交集

```python
odds = {1, 3, 5, 7, 9}
evens = {0, 2, 4, 6, 8}
primes = {2, 3, 5, 7}

# union() : 合并来自两个集合的元素，不重复
# 注意这不会改变两个集合
u = odds.union(evens)
print(u)

# intersection(): 选择在两个集合中都存在的元素
i = odds.intersection(evens)
print(i)

i = odds.intersection(primes)
print(i)

i = evens.intersection(primes)
print(i)
```

```python
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    set()
    {3, 5, 7}
    {2}
```

### 集合的差

```python
setA = {1, 2, 3, 4, 5, 6, 7, 8, 9}
setB = {1, 2, 3, 10, 11, 12}

# difference() : 返回集合 setA 中不在集合 setB 中的元素的集合
diff_set = setA.difference(setB)
print(diff_set)

# A.difference(B) 与 B.difference(A) 不一样
diff_set = setB.difference(setA)
print(diff_set)

# symmetric_difference() : 返回集合 setA 和 setB 中不同时在两个集合中的元素的集合
diff_set = setA.symmetric_difference(setB)
print(diff_set)

# A.symmetric_difference(B) = B.symmetric_difference(A)
diff_set = setB.symmetric_difference(setA)
print(diff_set)
```

```python
    {4, 5, 6, 7, 8, 9}
    {10, 11, 12}
    {4, 5, 6, 7, 8, 9, 10, 11, 12}
    {4, 5, 6, 7, 8, 9, 10, 11, 12}
```

### 更新集合

```python
setA = {1, 2, 3, 4, 5, 6, 7, 8, 9}
setB = {1, 2, 3, 10, 11, 12}

# update() : 通过添加其他集合的元素进行更新
setA.update(setB)
print(setA)

# intersection_update() : 通过保留共同的元素进行更新
setA = {1, 2, 3, 4, 5, 6, 7, 8, 9}
setA.intersection_update(setB)
print(setA)

# difference_update() : 通过移除与其他集合中相同的元素进行更新
setA = {1, 2, 3, 4, 5, 6, 7, 8, 9}
setA.difference_update(setB)
print(setA)

# symmetric_difference_update() : 通过保留只出现在一个集合而不出现在另一个集合中的元素进行更新
setA = {1, 2, 3, 4, 5, 6, 7, 8, 9}
setA.symmetric_difference_update(setB)
print(setA)

# 注意：所有的更新方法同时适用于其他可迭代对象作为参数，比如列表，元组
# setA.update([1, 2, 3, 4, 5, 6])
```

```python
    {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
    {1, 2, 3}
    {4, 5, 6, 7, 8, 9}
    {4, 5, 6, 7, 8, 9, 10, 11, 12}
```

### 复制

```python
set_org = {1, 2, 3, 4, 5}

# 只是引用的复制，需要注意
set_copy = set_org

# 修改复制集合也会影响原来的集合
set_copy.update([3, 4, 5, 6, 7])
print(set_copy)
print(set_org)

# 使用 copy() 真正复制集合
set_org = {1, 2, 3, 4, 5}
set_copy = set_org.copy()

# 现在修改复制集合不会影响原来的集合
set_copy.update([3, 4, 5, 6, 7])
print(set_copy)
print(set_org)
```

```python
    {1, 2, 3, 4, 5, 6, 7}
    {1, 2, 3, 4, 5, 6, 7}
    {1, 2, 3, 4, 5, 6, 7}
    {1, 2, 3, 4, 5}
```

### 子集，超集和不交集

```python
setA = {1, 2, 3, 4, 5, 6}
setB = {1, 2, 3}
# issubset(setX): 如果 setX 包含集合，返回 True
print(setA.issubset(setB))
print(setB.issubset(setA)) # True

# issuperset(setX): 如果集合包含 setX，返回 True
print(setA.issuperset(setB)) # True
print(setB.issuperset(setA))

# isdisjoint(setX) : 如果两个集合交集为空，比如没有相同的元素，返回 True
setC = {7, 8, 9}
print(setA.isdisjoint(setB))
print(setA.isdisjoint(setC))
```

```python
    False
    True
    True
    False
    False
    True
```

### Frozenset

Frozenset 只是普通集和的不变版本。 尽管可以随时修改集合的元素，但 Frozenset 的元素在创建后保持不变。 创建方式：

```python
my_frozenset = frozenset(iterable)
```

```python
a = frozenset([0, 1, 2, 3, 4])

# 以下操作不允许：
# a.add(5)
# a.remove(1)
# a.discard(1)
# a.clear()

# 同时，更新方法也不允许：
# a.update([1,2,3])

# 其他集合操作可行
odds = frozenset({1, 3, 5, 7, 9})
evens = frozenset({0, 2, 4, 6, 8})
print(odds.union(evens))
print(odds.intersection(evens))
print(odds.difference(evens))
```

```python
    frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})
    frozenset()
    frozenset({1, 3, 5, 7, 9})
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

