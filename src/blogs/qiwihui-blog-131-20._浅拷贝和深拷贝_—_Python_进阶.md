# 20. 浅拷贝和深拷贝 — Python 进阶


在Python中，赋值语句（`obj_b = obj_a`）不会创建真实副本。 它仅使用相同的引用创建一个新变量。 因此，当你想制作可变对象（列表，字典）的实际副本并且想要在不影响原始对象的情况下修改副本时，必须格外小心。

对于“真实”副本，我们可以使用 `copy` 模块。 但是，对于复合/嵌套对象（例如嵌套列表或字典）和自定义对象，**浅拷贝**和**深拷贝**之间存在重要区别：

- 浅拷贝： *仅深一层*。 它创建一个新的集合对象，并使用对嵌套对象的引用来填充它。 这意味着修改副本中嵌套对象的深度超过一层会影响原始对象。
- 深拷贝： *完整的独立克隆*。 它创建一个新的集合对象，然后递归地使用在原始对象中找到的嵌套对象的副本填充它。

<!--more-->

### 赋值操作

这只会创建具有相同引用的新变量。 修改其中一个会影响另一个。

```python
list_a = [1, 2, 3, 4, 5]
list_b = list_a

list_a[0] = -10
print(list_a)
print(list_b)
```

```python
    [-10, 2, 3, 4, 5]
    [-10, 2, 3, 4, 5]
```

### 浅拷贝

一层深。 在级别1上进行修改不会影响其他列表。 使用 `copy.copy()` 或特定于对象的复制函数/复制构造函数。

```python
import copy
list_a = [1, 2, 3, 4, 5]
list_b = copy.copy(list_a)

# 不会影响其他列表
list_b[0] = -10
print(list_a)
print(list_b)
```

```python
    [1, 2, 3, 4, 5]
    [-10, 2, 3, 4, 5]
```

但是对于嵌套对象，在2级或更高级别上进行修改确实会影响其他对象！

```python
import copy
list_a = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
list_b = copy.copy(list_a)

# 会影响其他列表!
list_a[0][0]= -10
print(list_a)
print(list_b)
```

```python
    [[-10, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    [[-10, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
```

注意：你还可以使用以下内容来创建浅拷贝：

```python
# 浅拷贝
list_b = list(list_a)
list_b = list_a[:]
list_b = list_a.copy()
```

### 深拷贝

完全独立的克隆。 使用 `copy.deepcopy()`。

```python
import copy
list_a = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
list_b = copy.deepcopy(list_a)

# 不影响其他
list_a[0][0]= -10
print(list_a)
print(list_b)
```

```python
    [[-10, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
```

### 自定义对象

你可以使用 `copy` 模块来获取自定义对象的浅拷贝或深拷贝。

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
                
# 只复制引用
p1 = Person('Alex', 27)
p2 = p1
p2.age = 28
print(p1.age)
print(p2.age)
```

```python
    28
    28
```

```python
# 浅拷贝
import copy
p1 = Person('Alex', 27)
p2 = copy.copy(p1)
p2.age = 28
print(p1.age)
print(p2.age)
```

```python
    27
    28
```

现在让我们创建一个嵌套对象：

```python
class Company:
    def __init__(self, boss, employee):
        self. boss = boss
        self.employee = employee

# 浅拷贝会影响嵌套对象
boss = Person('Jane', 55)
employee = Person('Joe', 28)
company = Company(boss, employee)

company_clone = copy.copy(company)
company_clone.boss.age = 56
print(company.boss.age)
print(company_clone.boss.age)

print()
# 深拷贝不会影响嵌套对象
boss = Person('Jane', 55)
employee = Person('Joe', 28)
company = Company(boss, employee)
company_clone = copy.deepcopy(company)
company_clone.boss.age = 56
print(company.boss.age)
print(company_clone.boss.age)
```

```python
    56
    56

    55
    56
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/131)


