# 02. Tuple — Python 进阶


元组（Tuple）是对象的集合，它有序且不可变。 元组类似于列表，主要区别在于不可变性。 在Python中，元组用圆括号和逗号分隔的值书写。

<!--more-->

```python
my_tuple = ("Max", 28, "New York")
```

### 使用元组而不使用列表的原因

- 通常用于属于同一目标的对象。
- 将元组用于异构（不同）数据类型，将列表用于同类（相似）数据类型。
- 由于元组是不可变的，因此通过元组进行迭代比使用列表进行迭代要快一些。
- 具有不可变元素的元组可以用作字典的键。 使用列表做为键是不可能的。
- 如果你有不变的数据，则将其实现为元组将确保其有写保护。

### 创建元组

用圆括号和逗号分隔的值创建元组，或使用内置的 `tuple` 函数。

```python
tuple_1 = ("Max", 28, "New York")
tuple_2 = "Linda", 25, "Miami" # 括弧可选

# 特殊情况：只有一个元素的元组需要在在最后添加逗号，否则不会被识别为元组
tuple_3 = (25,)
print(tuple_1)
print(tuple_2)
print(tuple_3)

# 或者使用内置 tuple 函数将可迭代对象（list，dict，string）转变为元组
tuple_4 = tuple([1,2,3])
print(tuple_4)
```

```python
    ('Max', 28, 'New York')
    ('Linda', 25, 'Miami')
    (25,)
    (1, 2, 3)
```

### 访问元素

可以通过引用索引号访问元组项。 请注意，索引从0开始。

```python
item = tuple_1[0]
print(item)
# 你也可以使用负索引，比如 -1 表示最后一个元素，-2 表示倒数第二个元素，以此类推
item = tuple_1[-1]
print(item)
```

```python
    Max
    New York
```

### 添加或者修改元素

不可能，会触发 `TypeError` 错误。

```python
tuple_1[2] = "Boston"
```

```bash
---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-5-c391d8981369> in <module>
    ----> 1 tuple_1[2] = "Boston"

    TypeError: 'tuple' object does not support item assignment
```

### 删除元组

```python
del tuple_2
```

### 迭代

```python
# 使用 for 循环迭代元组
for i in tuple_1:
    print(i)
```

```python
    Max
    28
    New York
```

### 检查元素是否存在

```python
if "New York" in tuple_1:
    print("yes")
else:
    print("no")
```

```python
    yes
```

### 有用的方法

```python
my_tuple = ('a','p','p','l','e',)

# len() : 获取元组元素个数
print(len(my_tuple))

# count(x) : 返回与 x 相等的元素个数
print(my_tuple.count('p'))

# index(x) : 返回与 x 相等的第一个元素索引
print(my_tuple.index('l'))

# 重复
my_tuple = ('a', 'b') * 5
print(my_tuple)

# 拼接
my_tuple = (1,2,3) + (4,5,6)
print(my_tuple)

# 将列表转为元组，以及将元组转为列表
my_list = ['a', 'b', 'c', 'd']
list_to_tuple = tuple(my_list)
print(list_to_tuple)

tuple_to_list = list(list_to_tuple)
print(tuple_to_list)

# convert string to tuple
string_to_tuple = tuple('Hello')
print(string_to_tuple)
```

```python
    5
    2
    3
    ('a', 'b', 'a', 'b', 'a', 'b', 'a', 'b', 'a', 'b')
    (1, 2, 3, 4, 5, 6)
    ('a', 'b', 'c', 'd')
    ['a', 'b', 'c', 'd']
    ('H', 'e', 'l', 'l', 'o')
```

### 切片

和字符串一样，使用冒号（`:`）访问列表的子部分。

```python
# a[start:stop:step], 默认步长为 1
a = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
b = a[1:3] # 注意，最后一个索引不包括
print(b)
b = a[2:] # 知道最后
print(b)
b = a[:3] # 从最前头开始
print(b)
b = a[::2] # 从前往后没两个元素
print(b)
b = a[::-1] # 翻转元组
print(b)
```

```python
    (2, 3)
    (3, 4, 5, 6, 7, 8, 9, 10)
    (1, 2, 3)
    (1, 3, 5, 7, 9)
    (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
```

元组解包

```python
# 变量个数必需与元组元素个数相同
tuple_1 = ("Max", 28, "New York")
name, age, city = tuple_1
print(name)
print(age)
print(city)

# 提示: 使用 * 解包多个元素到列表
my_tuple = (0, 1, 2, 3, 4, 5)
item_first, *items_between, item_last = my_tuple
print(item_first)
print(items_between)
print(item_last)
```

```python
    Max
    28
    New York
    0
    [1, 2, 3, 4]
    5
```

### 嵌套元组

```python
a = ((0, 1), ('age', 'height'))
print(a)
print(a[0])
```

```python
    ((0, 1), ('age', 'height'))
    (0, 1)
```

### 比较元组和列表

元组的不可变性使Python可以进行内部优化。 因此，在处理大数据时，元组可以更高效。

```python
# 比较大小
import sys
my_list = [0, 1, 2, "hello", True]
my_tuple = (0, 1, 2, "hello", True)
print(sys.getsizeof(my_list), "bytes")
print(sys.getsizeof(my_tuple), "bytes")

# 比较列表和元组创建语句的执行时间
import timeit
print(timeit.timeit(stmt="[0, 1, 2, 3, 4, 5]", number=1000000))
print(timeit.timeit(stmt="(0, 1, 2, 3, 4, 5)", number=1000000))
```

```python
    104 bytes
    88 bytes
    0.12474981700000853
    0.014836141000017733
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/119)


