# 14. 生成器 — Python 进阶

生成器是可以在运行中暂停和恢复的函数，返回可以迭代的对象。 与列表不同，它们是懒惰的，因此一次仅在被询问时才产生一项。 因此，在处理大型数据集时，它们的内存效率更高。

生成器的定义类似于普通函数，但是使用 `yield` 语句而不是 `return`。

```python
def my_generator():
    yield 1
    yield 2
    yield 3
```

<!--more-->

### 执行生成器函数

调用该函数不会执行它，而是函数返回一个生成器对象，该对象用于控制执行。 生成器对象在调用 `next()` 时执行。 首次调用 `next()` 时，执行从函数的开头开始，一直持续到第一个 `yield` 语句，在该语句中返回语句右边的值。 随后对 `next()` 的调用从 `yield` 语句继续（并循环），直到达到另一个 `yield`。 如果由于条件而未调用 `yield` 或到达末尾，则会引发 `StopIteration` 异常：

```python
def countdown(num):
    print('Starting')
    while num > 0:
        yield num
        num -= 1

# 这不会打印 'Starting'
cd = countdown(3)

# 这会打印 'Starting' 以及第一个值
print(next(cd))

# 会打印第二个值
print(next(cd))
print(next(cd))

# 这会引发 StopIteration
print(next(cd))
```

```python
    Starting
    3
    2
    1
    ---------------------------------------------------------------------------
    StopIteration                             Traceback (most recent call last)
    <ipython-input-1-3941498e0bf0> in <module>
         16 
         17 # this will raise a StopIteration
    ---> 18 print(next(cd))

    StopIteration:
```

```python
# 你可以使用 for 循环来遍历一个生成器对象
cd = countdown(3)
for x in cd:
    print(x)
```

```python
    Starting
    3
    2
    1
```

```python
# 你可以将其用于接受可迭代对象作为输入的函数
cd = countdown(3)
sum_cd = sum(cd)
print(sum_cd)

cd = countdown(3)
sorted_cd = sorted(cd)
print(sorted_cd)
```

```python
    Starting
    6
    Starting
    [1, 2, 3]
```

最大的优点：迭代器节省内存！

由于这些值是延迟生成的，即仅在需要时才生成，因此可以节省大量内存，尤其是在处理大数据时。 此外，我们不必等到所有元素生成后再开始使用它们。

```python
# 如果没有生成器，则必须将完整序列存储在此处的列表中
def firstn(n):
    num, nums = 0, []
    while num < n:
        nums.append(num)
        num += 1
    return nums

sum_of_first_n = sum(firstn(1000000))
print(sum_of_first_n)
import sys
print(sys.getsizeof(firstn(1000000)), "bytes")
```

```python
    499999500000
    8697464 bytes
```

```python
# 使用生成器，不需要额外的序列来存储数字
def firstn(n):
    num = 0
    while num < n:
        yield num
        num += 1

sum_of_first_n = sum(firstn(1000000))
print(sum_of_first_n)
import sys
print(sys.getsizeof(firstn(1000000)), "bytes")
```

```python
    499999500000
    120 bytes
```

### 另一个例子：斐波那契数列

```python
def fibonacci(limit):
    a, b = 0, 1 # 前两个数
    while a < limit:
        yield a
        a, b = b, a + b

fib = fibonacci(30)
# 生成器对象可以被转为列表（这儿只是用来打印）
print(list(fib))
```

```python
    [0, 1, 1, 2, 3, 5, 8, 13, 21]
```

### 生成器表达式

就像列表推导一样，生成器可以用相同的语法编写，除了用括号代替方括号。 注意不要混淆它们，因为由于函数调用的开销，生成器表达式通常比列表理解要慢（[https://stackoverflow.com/questions/11964130/list-comprehension-vs-generator-expressions-weird-timeit-results/11964478#11964478](https://stackoverflow.com/questions/11964130/list-comprehension-vs-generator-expressions-weird-timeit-results/11964478#11964478)）。

```python
# 生成器表达式
mygenerator = (i for i in range(1000) if i % 2 == 0)
print(sys.getsizeof(mygenerator), "bytes")

# 列表推导式
mylist = [i for i in range(1000) if i % 2 == 0]
print(sys.getsizeof(mylist), "bytes")
```

```python
    120 bytes
    4272 bytes
```

### 生成器背后的概念

这个类将生成器实现为可迭代的对象。 它必须实现 `__iter__` 和 `__next__` 使其可迭代，跟踪当前状态（在这种情况下为当前数字），并注意 `StopIteration`。 它可以用来理解生成器背后的概念。 但是，有很多样板代码，其逻辑并不像使用 `yield` 关键字的简单函数那样清晰。

```python
class firstn:
    def __init__(self, n):
        self.n = n
        self.num = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.num < self.n:
            cur = self.num
            self.num += 1
            return cur
        else:
            raise StopIteration()
             
firstn_object = firstn(1000000)
print(sum(firstn_object))
```

```python
    499999500000
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

