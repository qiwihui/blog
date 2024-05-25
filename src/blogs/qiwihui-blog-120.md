---
title: "03. 字典 — Python 进阶"
description: "03. 字典 — Python 进阶"
tags: 
- 技术
- Python
top: 120
date: 21/03/2021, 21:12:12
author: qiwihui
update: 22/03/2021, 10:48:55
categories: 技术
---

字典是无序，可变和可索引的集合。 字典由键值对的集合组成。 每个键值对将键映射到其关联值。 字典用大括号书写。 每对键值均以冒号（ `:` ）分隔，并且各项之间以逗号分隔。

<!--more-->

```python
my_dict = {"name":"Max", "age":28, "city":"New York"}
```

### 创建字典

使用大括号或者内置的 `dict` 函数创建。

```python
my_dict = {"name":"Max", "age":28, "city":"New York"}
print(my_dict)

# 或者使用字典构造器，注意：键不需要引号。
my_dict_2 = dict(name="Lisa", age=27, city="Boston")
print(my_dict_2)
```

```python
    {'name': 'Max', 'age': 28, 'city': 'New York'}
    {'name': 'Lisa', 'age': 27, 'city': 'Boston'}
```

### 访问元素

```python
name_in_dict = my_dict["name"]
print(name_in_dict)

# 如果键没有找到，引发 KeyError 错误
# print(my_dict["lastname"])
```

```python
    Max
```

### 添加或修改元素

只需添加或访问键并分配值即可。

```python
# 添加新键
my_dict["email"] = "max@xyz.com"
print(my_dict)

# 覆盖已经存在的键
my_dict["email"] = "coolmax@xyz.com"
print(my_dict)
```

```python
    {'name': 'Max', 'age': 28, 'city': 'New York', 'email': 'max@xyz.com'}
    {'name': 'Max', 'age': 28, 'city': 'New York', 'email': 'coolmax@xyz.com'}
```

### 删除元素

```python
# 删除键值对
del my_dict["email"]

# pop 返回值并删除键值对
print("popped value:", my_dict.pop("age"))

# 返回并移除最后插入的价值对
# （在 Python 3.7 之前，移除任意键值对）
print("popped item:", my_dict.popitem())

print(my_dict)

# clear() : 移除所有键值对
# my_dict.clear()
```

```python
    popped value: 28
    popped item: ('city', 'New York')
    {'name': 'Max'}
```

检查键

```python
my_dict = {"name":"Max", "age":28, "city":"New York"}
# 使用 if .. in ..
if "name" in my_dict:
    print(my_dict["name"])

# 使用 try except
try:
    print(my_dict["firstname"])
except KeyError:
    print("No key found")
```

```python
    Max
    No key found
```

### 遍历字典

```python
# 遍历键
for key in my_dict:
    print(key, my_dict[key])

# 遍历键
for key in my_dict.keys():
    print(key)

# 遍历值
for value in my_dict.values():
    print(value)

# 遍历键和值
for key, value in my_dict.items():
    print(key, value)
```

```python
    name Max
    age 28
    city New York
    name
    age
    city
    Max
    28
    New York
    name Max
    age 28
    city New York
```

### 复制字典

复制索引时请注意。

```python
dict_org = {"name":"Max", "age":28, "city":"New York"}

# 这只复制字典的引用，需要小心
dict_copy = dict_org

# 修改复制字典也会影响原来的字典
dict_copy["name"] = "Lisa"
print(dict_copy)
print(dict_org)

# 使用 copy() 或者 dict(x) 来真正复制字典
dict_org = {"name":"Max", "age":28, "city":"New York"}

dict_copy = dict_org.copy()
# dict_copy = dict(dict_org)

# 现在修改复制字典不会影响原来的字典
dict_copy["name"] = "Lisa"
print(dict_copy)
print(dict_org)
```

```python
    {'name': 'Lisa', 'age': 28, 'city': 'New York'}
    {'name': 'Lisa', 'age': 28, 'city': 'New York'}
    {'name': 'Lisa', 'age': 28, 'city': 'New York'}
    {'name': 'Max', 'age': 28, 'city': 'New York'}
```

### 合并两个字典

```python
# 使用 update() 方法合两个字典
# 存在的键会被覆盖，新键会被添加
my_dict = {"name":"Max", "age":28, "email":"max@xyz.com"}
my_dict_2 = dict(name="Lisa", age=27, city="Boston")

my_dict.update(my_dict_2)
print(my_dict)
```

```python
    {'name': 'Lisa', 'age': 27, 'email': 'max@xyz.com', 'city': 'Boston'}
```

### 可能的键类型

任何不可变的类型（例如字符串或数字）都可以用作键。 另外，如果元组仅包含不可变元素，则可以使用它作为键。

```python
# 使用数字做键，但要小心
my_dict = {3: 9, 6: 36, 9:81}
# 不要将键误认为是列表的索引，例如，在这里无法使用 my_dict[0]
print(my_dict[3], my_dict[6], my_dict[9])

# 使用仅包含不可变元素（例如数字，字符串）的元组
my_tuple = (8, 7)
my_dict = {my_tuple: 15}

print(my_dict[my_tuple])
# print(my_dict[8, 7])

# 不能使用列表，因为列表是可变的，会抛出错误：
# my_list = [8, 7]
# my_dict = {my_list: 15}
```

```python
    9 36 81
    15
```

### 嵌套字典

值也可以是容器类型（例如列表，元组，字典）。

```python
my_dict_1 = {"name": "Max", "age": 28}
my_dict_2 = {"name": "Alex", "age": 25}
nested_dict = {"dictA": my_dict_1,
               "dictB": my_dict_2}
print(nested_dict)
```

```python
    {'dictA': {'name': 'Max', 'age': 28}, 'dictB': {'name': 'Alex', 'age': 25}}
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

