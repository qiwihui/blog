# 18. 函数参数 — Python 进阶

在本文中，我们将详细讨论函数形参（parameters）和函数实参（arguments）。 我们将学习：

- 形参和实参之间的区别
- 位置和关键字参数
- 默认参数
- 变长参数（ `*args` 和 `**kwargs`）
- 容器拆包成函数参数
- 局部与全局参数
- 参数传递（按值还是按引用？）

<!--more-->

### 形参和实参之间的区别

- 形数是定义函数时在括号内定义或使用的变量
- 实参是调用函数时为这些参数传递的值

```python
def print_name(name): # name 是形参
    print(name)

print_name('Alex') # 'Alex' 是实参
```

### 位置和关键字参数

我们可以将参数作为位置参数或关键字参数传递。 关键字参数的一些好处可能是：

- 我们可以通过名称来调用参数，以使其更清楚地表示其含义
- 我们可以通过重新排列参数的方式来使参数最易读

```python
def foo(a, b, c):
    print(a, b, c)
    
# 位置参数
foo(1, 2, 3)

# 关键字参数
foo(a=1, b=2, c=3)
foo(c=3, b=2, a=1) # 注意此处顺序不重要

# 混合使用
foo(1, b=2, c=3)

# 以下不允许
# foo(1, b=2, 3) # 位置参数在关键字参数之后
# foo(1, b=2, a=3) # 'a' 有多个值
```

```python
    1 2 3
    1 2 3
    1 2 3
    1 2 3
```

### 默认参数

函数可以具有带有预定义值的默认参数。 可以忽略此参数，然后将默认值传递给函数，或者可以将参数与其他值一起使用。 注意，必须将默认参数定义为函数中的最后一个参数。

```python
# 默认参数
def foo(a, b, c, d=4):
    print(a, b, c, d)

foo(1, 2, 3, 4)
foo(1, b=2, c=3, d=100)

# 不允许：默认参数必需在最后
# def foo(a, b=2, c, d=4):
#     print(a, b, c, d)
```

```python
    1 2 3 4
    1 2 3 100
```

### 变长参数（ `*args` 和 `**kwargs`）

- 如果用一个星号（ `*` ）标记参数，则可以将任意数量的位置参数传递给函数（通常称为 `*args`）
- 如果用两个星号（ `**` ）标记参数，则可以将任意数量的关键字参数传递给该函数（通常称为  `**kwargs` ）。

```python
def foo(a, b, *args, **kwargs):
    print(a, b)
    for arg in args:
        print(arg)
    for kwarg in kwargs:
        print(kwarg, kwargs[kwarg])

# 3, 4, 5 合并入 args
# six and seven 合并入 kwargs
foo(1, 2, 3, 4, 5, six=6, seven=7)
print()

# 也可以省略 args 或 kwargs
foo(1, 2, three=3)
```

```python
    1 2
    3
    4
    5
    six 6
    seven 7

    1 2
    three 3
```

### 强制关键字参数

有时你想要仅使用关键字的参数。 你可以执行以下操作：

- 如果在函数参数列表中输入 `*,`，则此后的所有参数都必须作为关键字参数传递。
- 变长参数后面的参数必须是关键字参数。

```python
def foo(a, b, *, c, d):
    print(a, b, c, d)

foo(1, 2, c=3, d=4)
# 不允许:
# foo(1, 2, 3, 4)

# 变长参数后面的参数必须是关键字参数
def foo(*args, last):
    for arg in args:
        print(arg)
    print(last)

foo(8, 9, 10, last=50)
```

```python
    1 2 3 4
    8
    9
    10
    50
```

### 拆包成参数

- 如果容器的长度与函数参数的数量匹配，则列表或元组可以用一个星号（ `*` ）拆包为参数。
- 字典可以拆包为带有两个星号（ `**` ）的参数，其长度和键与函数参数匹配。

```python
def foo(a, b, c):
    print(a, b, c)

# list/tuple 拆包，长度必需匹配
my_list = [4, 5, 6] # or tuple
foo(*my_list)

# dict 拆包，键和长度必需匹配
my_dict = {'a': 1, 'b': 2, 'c': 3}
foo(**my_dict)

# my_dict = {'a': 1, 'b': 2, 'd': 3} # 不可能，因为关键字错误
```

```python
    4 5 6
    1 2 3
```

### 局部变量与全局变量

可以在函数体内访问全局变量，但是要对其进行修改，我们首先必须声明 `global var_name` 才能更改全局变量。

```python
def foo1():
    x = number # 全局变量只能在这里访问
    print('number in function:', x)

number = 0
foo1()

# 修改全局变量
def foo2():
    global number # 现在可以访问和修改全局变量
    number = 3

print('number before foo2(): ', number)
foo2() # 修改全局变量
print('number after foo2(): ', number)
```

```python
    number in function: 0
    number before foo2():  0
    number after foo2():  3
```

如果我们不写 `global var_name` 并给与全局变量同名的变量赋一个新值，这将在函数内创建一个局部变量。 全局变量保持不变。

```python
number = 0

def foo3():
    number = 3 # 这是局部变量

print('number before foo3(): ', number)
foo3() # 不会修改全局变量
print('number after foo3(): ', number)
```

```python
    number before foo3():  0
    number after foo3():  0
```

### 参数传递

Python使用一种称为“对象调用”或“对象引用调用”的机制。必须考虑以下规则：

- 传入的参数实际上是对对象的引用（但引用是按值传递）
- 可变和不可变数据类型之间的差异

这意味着：

1. 可变对象（例如列表，字典）可以在方法中进行更改。但是，如果在方法中重新绑定引用，则外部引用仍将指向原始对象。
2. 不能在方法中更改不可变的对象（例如int，string）。但是**包含在**可变对象中的不可变对象可以在方法中重新分配。

```python
# 不可变对象 -> 不变
def foo(x):
    x = 5 # x += 5 也无效，因为x是不可变的，必须创建一个新变量

var = 10
print('var before foo():', var)
foo(var)
print('var after foo():', var)
```

```python
    var before foo(): 10
    var after foo(): 10
```

```python
# 可变对象 -> 可变
def foo(a_list):
    a_list.append(4)
    
my_list = [1, 2, 3]
print('my_list before foo():', my_list)
foo(my_list)
print('my_list after foo():', my_list)
```

```python
    my_list before foo(): [1, 2, 3]
    my_list after foo(): [1, 2, 3, 4]
```

```python
# 不可变对象包含在可变对象内 -> 可变
def foo(a_list):
    a_list[0] = -100
    a_list[2] = "Paul"
    
my_list = [1, 2, "Max"]
print('my_list before foo():', my_list)
foo(my_list)
print('my_list after foo():', my_list)
```

```python
# 重新绑定可变引用 -> 不变
def foo(a_list):
    a_list = [50, 60, 70] # a_list 是函数内新的局部变量
    a_list.append(50)
    
my_list = [1, 2, 3]
print('my_list before foo():', my_list)
foo(my_list)
print('my_list after foo():', my_list)
```

```python
    my_list before foo(): [1, 2, 3]
    my_list after foo(): [1, 2, 3]
```

对于可变类型，请小心使用 `+=` 和 `=` 操作。 第一个操作对传递的参数有影响，而后者则没有：

```python
# 重新绑定引用的另一个例子
def foo(a_list):
    a_list += [4, 5] # 这会改变外部变量
    
def bar(a_list):
    a_list = a_list + [4, 5] # 在会重新绑定引用到本地变量

my_list = [1, 2, 3]
print('my_list before foo():', my_list)
foo(my_list)
print('my_list after foo():', my_list)

my_list = [1, 2, 3]
print('my_list before bar():', my_list)
bar(my_list)
print('my_list after bar():', my_list)
```

```python
    my_list before foo(): [1, 2, 3]
    my_list after foo(): [1, 2, 3, 4, 5]
    my_list before bar(): [1, 2, 3]
    my_list after bar(): [1, 2, 3]
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

