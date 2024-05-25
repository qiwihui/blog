# 05. 字符串 — Python 进阶

字符串是字符序列。 Python中的字符串用双引号或单引号引起来。

```python
my_string = 'Hello'
```

Python字符串是不可变的，这意味着它们在创建后就无法更改。

<!--more-->

### 创建

```python
# 使用单引号后者双引号
my_string = 'Hello'
my_string = "Hello"
my_string = "I' m  a 'Geek'"

# 转义反斜杠
my_string = 'I\' m  a "Geek"'
my_string = 'I\' m a \'Geek\''
print(my_string)

# 多行字符串使用三个引号
my_string = """Hello
World"""
print(my_string)

# 如果需要字符串在下一行继续，使用反斜杠
my_string = "Hello \
World"
print(my_string)
```

```python
    I' m a 'Geek'
    Hello
    World
    Hello World
```

### 访问字符和子字符串

```python
my_string = "Hello World"

# 使用索引获取字符
b = my_string[0]
print(b)

# 通过切片获取子字符串
b = my_string[1:3] # 注意，最后一个索引不包括
print(b)
b = my_string[:5] # 从第一个元素开始
print(b)
b = my_string[6:] # 直到最后
print(b)
b = my_string[::2] # 从头到为每隔两个元素
print(b)
b = my_string[::-1] # 使用负步长翻转列表
print(b)
```

```python
    H
    el
    Hello
    World
    HloWrd
    dlroW olleH
```

### 连接两个或多个字符串

```python
# 使用 + 拼接字符串
greeting = "Hello"
name = "Tom"
sentence = greeting + ' ' + name
print(sentence)
```

```python
Hello Tom
```

### **迭代**

```python
# 使用for循环迭代列表
my_string = 'Hello'
for i in my_string:
    print(i)
```

```python
    H
    e
    l
    l
    o
```

### 检查字符或子字符串是否存在

```python
if "e" in "Hello":
    print("yes")
if "llo" in "Hello":
    print("yes")
```

```python
    yes
    yes
```

### 有用的方法

```python
my_string = "     Hello World "

# 去除空格
my_string = my_string.strip()
print(my_string)

# 字符的个数
print(len(my_string))

# 大小写
print(my_string.upper())
print(my_string.lower())

# startswith 和 endswith
print("hello".startswith("he"))
print("hello".endswith("llo"))

# 找到子字符串的第一个索引，没有则返回 -1
print("Hello".find("o"))

# 计算字符或者子字符串的个数
print("Hello".count("e"))

# 使用其他字符串代替子字符串（当且仅当子字符串存在时）
# 注意：原字符串保持不变
message = "Hello World"
new_message = message.replace("World", "Universe")
print(new_message)

# 将字符串切分为为列表
my_string = "how are you doing"
a = my_string.split() # default argument is " "
print(a)
my_string = "one,two,three"
a = my_string.split(",")
print(a)

# 将列表拼接为字符串
my_list = ['How', 'are', 'you', 'doing']
a = ' '.join(my_list) # 给出的字符串是分隔符，比如在每个元素之间添加 ' '
print(a)
```

```python
    Hello World
    11
    HELLO WORLD
    hello world
    ['how', 'are', 'you', 'doing']
    ['one', 'two', 'three']
    True
    True
    4
    1
    Hello Universe
    How are you doing
```

### 格式化

新样式使用 `format()` 方法，旧样式使用 `%` 操作符。

```python
# 使用大括号做占位符
a = "Hello {0} and {1}".format("Bob", "Tom")
print(a)

# 默认顺序时位置可以不写
a = "Hello {} and {}".format("Bob", "Tom")
print(a)

a = "The integer value is {}".format(2)
print(a)

# 一些数字的特殊格式化规则
a = "The float value is {0:.3f}".format(2.1234)
print(a)
a = "The float value is {0:e}".format(2.1234)
print(a)
a = "The binary value is {0:b}".format(2)
print(a)

# old style formatting by using % operator
# 旧的方式使用 % 操作符
print("Hello %s and %s" % ("Bob", "Tom")) # 多个参数时必需是元组
val =  3.14159265359
print("The decimal value is %d" % val)
print("The float value is %f" % val)
print("The float value is %.2f" % val)
```

```python
    Hello Bob and Tom
    Hello Bob and Tom
    The integer value is 2
    The float value is 2.123
    The float value is 2.123400e+00
    The binary value is 10
    Hello Bob and Tom
    The decimal value is 10
    The float value is 10.123450
    The float value is 10.12
```

### f-Strings

从 Python 3.6 起，可以直接在花括号内使用变量。

```python
name = "Eric"
age = 25
a = f"Hello, {name}. You are {age}."
print(a)
pi = 3.14159
a = f"Pi is {pi:.3f}"
print(a)
# f-Strings 在运行时计算，可以允许表达式
a = f"The value is {2*60}"
print(a)
```

```python
    Hello, Eric. You are 25.
    Pi is 3.142
    The value is 120
```

### 更多关于不变性和拼接

```python
# 因为字符串不可变，所以使用 + 或者 += 拼接字符串总是生成新的字符串
# 因此，多个操作时更加耗时。使用 join 方法更快。
from timeit import default_timer as timer
my_list = ["a"] * 1000000

# bad
start = timer()
a = ""
for i in my_list:
    a += i
end = timer()
print("concatenate string with + : %.5f" % (end - start))

# good
start = timer()
a = "".join(my_list)
end = timer()
print("concatenate string with join(): %.5f" % (end - start))
```

```python
    concat string with + : 0.34527
    concat string with join(): 0.01191
```

```python
# a[start:stop:step], 默认步长为 1
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = a[1:3] # 注意，最后一个索引不包括
print(b)
b = a[2:] # 直到最后
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

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

