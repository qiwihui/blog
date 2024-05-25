# 07. Itertools — Python 进阶

Python `itertools` 模块是用于处理迭代器的工具集合。 简而言之，迭代器是可以在for循环中使用的数据类型。 Python中最常见的迭代器是列表。

有关所有可能的 itertools，请参见 [https://docs.python.org/3/library/itertools.html](https://docs.python.org/3/library/itertools.html)。

<!--more-->

### product()

该工具计算输入可迭代项的笛卡尔积。

它等效于嵌套的for循环。 例如，`product(A, B)`返 回的结果与 `((x,y) for x in A for y in B)` 相同。

```python
from itertools import product

prod = product([1, 2], [3, 4])
print(list(prod)) # 请注意，我们将迭代器转换为列表进行打印

# 为了允许可迭代对象自身做乘积，指定重复次数
prod = product([1, 2], [3], repeat=2)
print(list(prod)) # 请注意，我们将迭代器转换为列表进行打印
```

```python
    [(1, 3), (1, 4), (2, 3), (2, 4)]
    [(1, 3, 1, 3), (1, 3, 2, 3), (2, 3, 1, 3), (2, 3, 2, 3)]
```

### permutations()

此工具以所有可能的顺序，以可迭代的方式返回元素的连续长度排列，并且没有重复的元素。

```python
from itertools import permutations

perm = permutations([1, 2, 3])
print(list(perm))

# 可选：排列元组的长度
perm = permutations([1, 2, 3], 2)
print(list(perm))
```

```python
    [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
    [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
```

### combinations() and combinations_with_replacement()

长度r的元组，按排序顺序。 因此，如果对输入的可迭代对象进行排序，则将按排序顺序生成组合元组。 `combinations()`不允许重复的元素，但  `combinations_with_replacement()` 允许。

```python
from itertools import combinations, combinations_with_replacement

# 第二个参数是必需的，它指定输出元组的长度。
comb = combinations([1, 2, 3, 4], 2)
print(list(comb))

comb = combinations_with_replacement([1, 2, 3, 4], 2)
print(list(comb))
```

```python
    [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    [(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (2, 4), (3, 3), (3, 4), (4, 4)]
```

### accumulate()

使迭代器返回累加的总和或其他二进制函数的累加结果。

```python
from itertools import accumulate

# 返回累积和
acc = accumulate([1,2,3,4])
print(list(acc))

# 其他可能的函数是可能的
import operator
acc = accumulate([1,2,3,4], func=operator.mul)
print(list(acc))

acc = accumulate([1,5,2,6,3,4], func=max)
print(list(acc))
```

```python
    [1, 3, 6, 10]
    [1, 2, 6, 24]
    [1, 5, 5, 6, 6, 6]
```

### groupby()

创建一个迭代器，从迭代器返回连续的键和组。 键是为每个元素计算键值的函数。 如果未指定或为None，则键默认为标识函数，并返回不变的元素。 通常，可迭代项需要已经在相同的键函数上进行了排序。

```python
from itertools import groupby

# 使用函数作为键
def smaller_than_3(x):
    return x < 3

group_obj = groupby([1, 2, 3, 4], key=smaller_than_3)
for key, group in group_obj:
    print(key, list(group))

# 或者使用 lambda 表达式，比如：包含 'i' 的词
group_obj = groupby(["hi", "nice", "hello", "cool"], key=lambda x: "i" in x)
for key, group in group_obj:
    print(key, list(group))
    
persons = [{'name': 'Tim', 'age': 25}, {'name': 'Dan', 'age': 25}, 
           {'name': 'Lisa', 'age': 27}, {'name': 'Claire', 'age': 28}]

for key, group in groupby(persons, key=lambda x: x['age']):
    print(key, list(group))
```

```python
    True [1, 2]
    False [3, 4]
    True ['hi', 'nice']
    False ['hello', 'cool']
    25 [{'name': 'Tim', 'age': 25}, {'name': 'Dan', 'age': 25}]
    27 [{'name': 'Lisa', 'age': 27}]
    28 [{'name': 'Claire', 'age': 28}]
```

### 无限迭代器：count(), cycle(), repeat()

```python
from itertools import count, cycle, repeat
# count(x): 从 x 开始计数: x, x+1, x+2, x+3...
for i in count(10):
    print(i)
    if  i >= 13:
        break

# cycle(iterable) : 通过迭代无限循环
print("")
sum = 0
for i in cycle([1, 2, 3]):
    print(i)
    sum += i
    if sum >= 12:
        break

# repeat(x): 无限重复x或重复n次
print("")
for i in repeat("A", 3):
    print(i)
```

```python
    10
    11
    12
    13

    1
    2
    3
    1
    2
    3

    A
    A
    A
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

