# 08. Lambda 函数 — Python 进阶


Lambda函数是一个小的（一行）匿名函数，没有函数名称。 Lambda函数可以接受任意数量的参数，但只能具有一个表达式。 虽然使用def关键字定义了普通函数，但在Python中，使用lambda关键字定义了匿名函数。

```python
lambda arguments: expression
```

当简单函数仅在代码中使用一次或短时间时，可以使用Lambda函数。 最常见的用途是作为高阶函数（将其他函数作为参数的函数）的参数。 它们还与诸如 `map()`， `filter()` ， `reduce()`之类的内置函数一起使用。

<!--more-->

```python
# 一个给参数加10的lambda函数
f = lambda x: x+10
val1 = f(5)
val2 = f(100)
print(val1, val2)

# 一个返回两个参数乘积的lambda函数
f = lambda x,y: x*y
val3 = f(2,10)
val4 = f(7,5)
print(val3, val4)
```

```python
    15 110
    20 35
```

### 使用示例：另一个函数内的Lambda函数

从另一个函数返回定制的lambda函数，并根据需要创建不同的函数变体。

```python
def myfunc(n):
    return lambda x: x * n

doubler = myfunc(2)
print(doubler(6))

tripler = myfunc(3)
print(tripler(6))
```

```python
    12
    18
```

### 使用lambda函数作为key参数的自定义排序

key函数会在排序之前转换每个元素。

```python
points2D = [(1, 9), (4, 1), (5, -3), (10, 2)]
sorted_by_y = sorted(points2D, key= lambda x: x[1])
print(sorted_by_y)

mylist = [- 1, -4, -2, -3, 1, 2, 3, 4]
sorted_by_abs = sorted(mylist, key= lambda x: abs(x))
print(sorted_by_abs)
```

```python
    [(5, -3), (4, 1), (10, 2), (1, 9)]
    [-1, 1, -2, 2, -3, 3, -4, 4]
```

### 在 map 函数中使用 Lambda 函数

`map(func, seq)` ，使用函数转换每个元素。

```python
a  = [1, 2, 3, 4, 5, 6]
b = list(map(lambda x: x * 2 , a))

# 但是，尝试使用列表推导
# 如果你已经定义了函数，请使用 map
c = [x*2 for x in a]
print(b)
print(c)
```

```python
    [2, 4, 6, 8, 10, 12]
    [2, 4, 6, 8, 10, 12]
```

### 在 filter 函数中使用 Lambda 函数

`filter(func, seq)` ，返回其 `func` 计算为 `True` 的所有元素。

```python
a = [1, 2, 3, 4, 5, 6, 7, 8]
b = list(filter(lambda x: (x%2 == 0) , a))

# 同样可以使用列表推导实现
c = [x for x in a if x%2 == 0]
print(b)
print(c)
```

```python
    [2, 4, 6, 8]
    [2, 4, 6, 8]
```

### reduce

`reduce(func, seq)` ，重复将 `func` 应用于元素并返回单个值。`func` 需要2个参数。

```python
from functools import reduce
a = [1, 2, 3, 4]
product_a = reduce(lambda x, y: x*y, a)
print(product_a)
sum_a = reduce(lambda x, y: x+y, a)
print(sum_a)
```

```python
    24
    10
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/125)


