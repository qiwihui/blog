# 12. 随机数 — Python 进阶

Python定义了一组用于生成或操作随机数的函数。 本文介绍：

- `random` 模块
- 用 `random.seed()` 再生产数字
- 使用 `secrets` 模块创建密码学上强的随机数
- 用 `numpy.random` 创建随机 nd 数组

### `random` 模块

该模块为各种版本实现伪随机数生成器。它使用Mersenne Twister算法（[https://en.wikipedia.org/wiki/Mersenne_Twister](https://en.wikipedia.org/wiki/Mersenne_Twister)）作为其核心生成器。 之所以称其为伪随机数，是因为数字看起来是随机的，但是是可重现的。

<!--more-->

```python
import random

# [0,1) 之间随机浮点数
a = random.random()
print(a)

# [a,b] 之间随机浮点数
a = random.uniform(1,10)
print(a)

# [a,b] 之间随机整数，b 包括。
a = random.randint(1,10)
print(a)

# 之间随机整数，b 不包括。
a = random.randrange(1,10)
print(a)

# 参数为 mu 和 sigma 的正态分布随机浮点数
a = random.normalvariate(0, 1)
print(a)

# 从序列中随机选择元素
a = random.choice(list("ABCDEFGHI"))
print(a)

# 从序列中随机选择 k 个唯一元素
a = random.sample(list("ABCDEFGHI"), 3)
print(a)

# 选择可重复的k个元素，并返回大小为k的列表
a = random.choices(list("ABCDEFGHI"),k=3)
print(a)

# 原地随机排列
a = list("ABCDEFGHI")
random.shuffle(a)
print(a)
```

```python
    0.10426373452067317
    3.34983979352444
    3
    4
    -1.004568769635799
    E
    ['G', 'C', 'B']
    ['E', 'D', 'E']
    ['D', 'I', 'G', 'H', 'E', 'B', 'C', 'F', 'A']
```

### 种子生成器

使用 `random.seed()`，可以使结果可重复，并且 `random.seed()` 之后的调用链将产生相同的数据轨迹。 随机数序列变得确定，或完全由种子值确定。

```python
print('Seeding with 1...\n')

random.seed(1)
print(random.random())
print(random.uniform(1,10))
print(random.choice(list("ABCDEFGHI")))

print('\nRe-seeding with 42...\n')
random.seed(42)  # 重设随机种子

print(random.random())
print(random.uniform(1,10))
print(random.choice(list("ABCDEFGHI")))

print('\nRe-seeding with 1...\n')
random.seed(1)  # 重设随机种子

print(random.random())
print(random.uniform(1,10))
print(random.choice(list("ABCDEFGHI")))

print('\nRe-seeding with 42...\n')
random.seed(42)  # 重设随机种子

print(random.random())
print(random.uniform(1,10))
print(random.choice(list("ABCDEFGHI")))
```

```python
    Seeding with 1...

    0.13436424411240122
    8.626903632435095
    B

    Re-seeding with 42...

    0.6394267984578837
    1.2250967970040025
    E

    Re-seeding with 1...

    0.13436424411240122
    8.626903632435095
    B

    Re-seeding with 42...

    0.6394267984578837
    1.2250967970040025
    E
```

### `secrets` 模块

`secrets` 模块用于生成适合于管理数据（例如密码，帐户身份验证，安全令牌和相关机密）的密码学上强的随机数。

特别是，应优先使用`secrets` 而不是 `random` 模块中默认的伪随机数生成器，后者是为建模和仿真而设计的，而不是安全或加密技术。

```python
import secrets

# [0, n) 之间的随机整数。
a = secrets.randbelow(10)
print(a)

# 返回具有k个随机位的整数。
a = secrets.randbits(5)
print(a)

# 从序列中选择一个随机元素
a = secrets.choice(list("ABCDEFGHI"))
print(a)
```

```python
    6
    6
    E
```

### NumPy的随机数

为多维数组创建随机数。NumPy伪随机数生成器与Python标准库伪随机数生成器不同。

重要的是，设置Python伪随机数生成器种子不会影响NumPy伪随机数生成器，必须单独设置和使用。

```python
import numpy as np

np.random.seed(1)
# rand(d0,d1,…,dn)
# 生成随机浮点数的多维数组, 数组大小为 (d0,d1,…,dn)
print(np.random.rand(3))
# 重设随机种子
np.random.seed(1)
print(np.random.rand(3))

# 生成 [a,b) 之间随机整数的多维数组，大小为 n
values = np.random.randint(0, 10, (5,3))
print(values)

# 使用正态分布值生成多维数组，数组大小为 (d0,d1,…,dn)
# 来自标准正态分布的平均值为0.0且标准偏差为1.0的值
values = np.random.randn(5)
print(values)

# 随机排列一个多维数组.
# 仅沿多维数组的第一轴随机排列数组
arr = np.array([[1,2,3], [4,5,6], [7,8,9]])
np.random.shuffle(arr)
print(arr)
```

```python
    [4.17022005e-01 7.20324493e-01 1.14374817e-04]
    [4.17022005e-01 7.20324493e-01 1.14374817e-04]
    [[5 0 0]
     [1 7 6]
     [9 2 4]
     [5 2 4]
     [2 4 7]]
    [-2.29230928 -1.41555249  0.8858294   0.63190187  0.04026035]
    [[4 5 6]
     [7 8 9]
     [1 2 3]]
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

