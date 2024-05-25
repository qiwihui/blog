# 01. List — Python 进阶

列表（List）是一种有序且可变的容器数据类型。 与集合（Set）不同，列表允许重复的元素。 它方便保存数据序列并对其进行进一步迭代。 列表用方括号创建。

<!--more-->

`my_list = ["banana", "cherry", "apple"]`

### Python中基本的内置容器数据类型的比较：

- 列表（List）是一个有序且可变的数据类型。 允许重复的成员。
- 元组（Tuple）是有序且不可变的数据类型。 允许重复的成员。
- 集合（Set）是无序和未索引的数据类型。 不允许重复的成员。
- 字典（Dict）是无序，可变和可索引的数据类型。 没有重复的成员。
- 字符串是Unicode代码的不可变序列。

### 创建列表

列表使用方括号创建，或者内置的 list 函数。

```python
list_1 = ["banana", "cherry", "apple"]
print(list_1)

# 或者使用 list 函数创建空列表
list_2 = list()
print(list_2)

# 列表允许不同的数据类
list_3 = [5, True, "apple"]
print(list_3)

# 列表允许重复元素
list_4 = [0, 0, 1, 1]
print(list_4)
```

```python
    ['banana', 'cherry', 'apple']
    []
    [5, True, 'apple']
    [0, 0, 1, 1]
```

### 访问元素

可以通过索引号访问列表项。 请注意，索引从0开始。

```python
item = list_1[0]
print(item)

# 你也可以使用负索引，比如 -1 表示最后一个元素，
# -2 表示倒数第二个元素，以此类推
item = list_1[-1]
print(item)
```

```python
    banana
    apple
```

### 修改元素

只需访问索引并分配一个新值即可。

```python
# 列表创建之后可以被修改
list_1[2] = "lemon"
print(list_1)
```

```python
    ['banana', 'cherry', 'lemon']
```

### 有用的方法

查看Python文档以查看所有列表方法：[https://docs.python.org/3/tutorial/datastructures.html](https://docs.python.org/3/tutorial/datastructures.html)

```python
my_list = ["banana", "cherry", "apple"]

# len() : 获取列表的元素个数
print("Length:", len(my_list))

# append() : 添加一个元素到列表末尾
my_list.append("orange")

# insert() : 添加元素到特定位置
my_list.insert(1, "blueberry")
print(my_list)

# pop() : 移除并返回特定位置的元素，默认为最后一个
item = my_list.pop()
print("Popped item: ", item)

# remove() : 移除列表中的元素
my_list.remove("cherry") # 如果元素没有在列表中，则触发 Value error
print(my_list)

# clear() : 移除列表所有元素
my_list.clear()
print(my_list)

# reverse() : 翻转列表
my_list = ["banana", "cherry", "apple"]
my_list.reverse()
print('Reversed: ', my_list)

# sort() : 升序排列元素
my_list.sort()
print('Sorted: ', my_list)

# 使用 sorted() 得到一个新列表，原来的列表不受影响
# sorted() 对任何可迭代类型起作用，不只是列表
my_list = ["banana", "cherry", "apple"]
new_list = sorted(my_list)

# 创建具有重复元素的列表
list_with_zeros = [0] * 5
print(list_with_zeros)

# 列表拼接
list_concat = list_with_zeros + my_list
print(list_concat)

# 字符串转列表
string_to_list = list('Hello')
print(string_to_list)
```

```python
    Length: 3
    ['banana', 'blueberry', 'cherry', 'apple', 'orange']
    Popped item:  orange
    ['banana', 'blueberry', 'apple']
    []
    Reversed:  ['apple', 'cherry', 'banana']
    Sorted:  ['apple', 'banana', 'cherry']
    [0, 0, 0, 0, 0]
    [0, 0, 0, 0, 0, 'banana', 'cherry', 'apple']
    ['H', 'e', 'l', 'l', 'o']
```

### 复制列表

复制引用（references）时要小心。

```python
list_org = ["banana", "cherry", "apple"]

# 这只是将引用复制到列表中，要小心
list_copy = list_org

# 现在，修改复制的列表也会影响原来的列表
list_copy.append(True)
print(list_copy)
print(list_org)

# 使用 copy(), 或者 list(x) 来真正复制列表
# 切片（slicing）也可以复制：list_copy = list_org[:]
list_org = ["banana", "cherry", "apple"]

list_copy = list_org.copy()
# list_copy = list(list_org)
# list_copy = list_org[:]

# 现在，修改复制的列表不会影响原来的列表
list_copy.append(True)
print(list_copy)
print(list_org)
```

```python
    ['banana', 'cherry', 'apple', True]
    ['banana', 'cherry', 'apple', True]
    ['banana', 'cherry', 'apple', True]
    ['banana', 'cherry', 'apple']
```

### 迭代

```python
# 使用for循环迭代列表
for i in list_1:
    print(i)
```

```python
    banana
    cherry
    lemon
```

### 检查元素是否存在

```python
if "banana" in list_1:
    print("yes")
else:
    print("no")
```

```python
    yes
```

### 切片

和字符串一样，使用冒号（ `:`）访问列表的子部分。

```python
# a[start:stop:step], 默认步长为 1
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = a[1:3] # 主语，最后一个索引不包括
print(b)
b = a[2:] # 知道最后
print(b)
b = a[:3] # 从第一个元素开始
print(b)
a[0:3] = [0] # 替换子部分，需要可迭代
print(a)
b = a[::2] # 从头到为每隔两个元素
print(b)
a = a[::-1] # 使用负步长翻转列表
print(a)
b = a[:] # 使用切片复制元素
print(b)
```

```python
    [2, 3]
    [3, 4, 5, 6, 7, 8, 9, 10]
    [1, 2, 3]
    [0, 4, 5, 6, 7, 8, 9, 10]
    [0, 5, 7, 9]
    [10, 9, 8, 7, 6, 5, 4, 0]
    [10, 9, 8, 7, 6, 5, 4, 0]
```

### 列表推导

一种从现有列表创建新列表的简便快捷方法。

列表推导方括号内包含一个表达式，后跟for语句。

```python
a = [1, 2, 3, 4, 5, 6, 7, 8]
b = [i * i for i in a] # 每个元素平方
print(b)
```

```python
    [1, 4, 9, 16, 25, 36, 49, 64]
```

嵌套列表

```python
a = [[1, 2], [3, 4]]
print(a)
print(a[0])
```

```python
    [[1, 2], [3, 4]]
    [1, 2]
```
