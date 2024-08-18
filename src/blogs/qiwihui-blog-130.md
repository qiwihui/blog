# 19. 星号操作符 — Python 进阶


星号（ `*` ）可用于Python中的不同情况：

- 乘法和幂运算
- 创建具有重复元素的列表，元组或字符串
- `*args`， `**kwargs` 和仅关键字参数
- 拆包列表/元组/字典的函数参数
- 拆包容器
- 将可迭代对象合并到列表中/合并字典

<!--more-->

### 乘法和幂运算

```python
# 乘法
result = 7 * 5
print(result)

# 幂运算
result = 2 ** 4
print(result)
```

```python
    35
    16
```

### 创建具有重复元素的列表，元组或字符串

```python
# list
zeros = [0] * 10
onetwos = [1, 2] * 5
print(zeros)
print(onetwos)

# tuple
zeros = (0,) * 10
onetwos = (1, 2) * 5
print(zeros)
print(onetwos)

# string
A_string = "A" * 10
AB_string = "AB" * 5
print(A_string)
print(AB_string)
```

```python
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    (1, 2, 1, 2, 1, 2, 1, 2, 1, 2)
    AAAAAAAAAA
    ABABABABAB
```

### `*args`， `**kwargs` 和仅关键字参数

- 对可变长度参数使用 `*args`
- 对长度可变的关键字参数使用 `**kwargs`
- 使用 `*`，后跟更多函数参数以强制使用仅关键字的参数

```python
def my_function(*args, **kwargs):
    for arg in args:
        print(arg)
    for key in kwargs:
        print(key, kwargs[key])
        
my_function("Hey", 3, [0, 1, 2], name="Alex", age=8)

# '*' 或 '* identifier' 之后的参数是仅关键字参数，只能使用关键字参数传递。
def my_function2(name, *, age):
    print(name)
    print(age)

# my_function2("Michael", 5) --> 这会引发 TypeError 错误
my_function2("Michael", age=5)
```

```python
    Hey
    3
    [0, 1, 2]
    name Alex
    age 8
    Michael
    5
```

### 拆包函数参数

- 如果长度与参数匹配，则列表/元组/集合/字符串可以用 `*` 拆成函数参数。
- 如果长度和键与参数匹配，则字典可以用两个 `**` 拆包。

```python
def foo(a, b, c):
    print(a, b, c)

# 长度必需匹配
my_list = [1, 2, 3]
foo(*my_list)

my_string = "ABC"
foo(*my_string)

# 长度和键必需匹配
my_dict = {'a': 4, 'b': 5, 'c': 6}
foo(**my_dict)
```

```python
    1 2 3
    A B C
    4 5 6
```

### 拆包容器

将列表，元组或集合的元素拆包为单个和多个剩余元素。 请注意，即使被拆包的容器是元组或集合，也将多个元素组合在一个列表中。

```python
numbers = (1, 2, 3, 4, 5, 6, 7, 8)

*beginning, last = numbers
print(beginning)
print(last)

print()

first, *end = numbers
print(first)
print(end)

print()
first, *middle, last = numbers
print(first)
print(middle)
print(last)
```

```python
    [1, 2, 3, 4, 5, 6, 7]
    8

    1
    [2, 3, 4, 5, 6, 7, 8]

    1
    [2, 3, 4, 5, 6, 7]
    8
```

### 将可迭代对象合并到列表中/合并字典

由于PEP 448（[https://www.python.org/dev/peps/pep-0448/](https://www.python.org/dev/peps/pep-0448/)），从Python 3.5开始，这是可能的。

```python
# 将可迭代对象合并到列表中
my_tuple = (1, 2, 3)
my_set = {4, 5, 6}
my_list = [*my_tuple, *my_set]
print(my_list)

# 用字典拆包合并两个字典
dict_a = {'one': 1, 'two': 2}
dict_b = {'three': 3, 'four': 4}
dict_c = {**dict_a, **dict_b}
print(dict_c)
```

```python
    [1, 2, 3, 4, 5, 6]
    {'one': 1, 'two': 2, 'three': 3, 'four': 4}
```

但是，请注意以下合并解决方案。 如果字典中有任何非字符串键，则它将不起作用：[https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression/39858#39858](https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression/39858#39858)

```python
dict_a = {'one': 1, 'two': 2}
dict_b = {3: 3, 'four': 4}
dict_c = dict(dict_a, **dict_b)
print(dict_c)

# 以下可行:
# dict_c = {**dict_a, **dict_b}
```

```python
---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-52-2660fb90a60f> in <module>
          1 dict_a = {'one': 1, 'two': 2}
          2 dict_b = {3: 3, 'four': 4}
    ----> 3 dict_c = dict(dict_a, **dict_b)
          4 print(dict_c)
          5 
    TypeError: keywords must be strings
```

推荐进一步阅读：

- [https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/](https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/)
- [https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/](https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/)

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/130)


