# 11. JSON — Python 进阶

JSON（JavaScript对象表示法）是一种轻量级数据格式，用于数据交换。 在Python中具有用于编码和解码JSON数据的内置 `json` 模块。 只需导入它，就可以使用JSON数据了：

```python
import json
```

JSON的一些优点：

- JSON作为“字节序列”存在，在我们需要通过网络传输（流）数据的情况下非常有用。
- 与XML相比，JSON小得多，可转化为更快的数据传输和更好的体验。
- JSON非常文本友好，因为它是文本形式的，并且同时也是机器友好的。

<!--more-->

## JSON格式

```json
{
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "swimming", "singing"],
    "age": 28,
    "children": [
        {
            "firstName": "Alex",
            "age": 5
        },
        {
            "firstName": "Bob",
            "age": 7
        }
    ]
}
```

JSON支持基本类型（字符串，数字，布尔值）以及嵌套的数组和对象。 根据以下转换，将简单的Python对象转换为JSON：

[Python 和 JSON 转换](https://www.notion.so/c16eeb7ba08841a3bbfc63c268bcfe54)

## 从Python到JSON（序列化，编码）

使用 `json.dumps()` 方法将Python对象转换为JSON字符串。

```python
import json

person = {"name": "John", "age": 30, "city": "New York", "hasChildren": False, "titles": ["engineer", "programmer"]}

# 转为 JSON:
person_json = json.dumps(person)
# 使用不用的格式
person_json2 = json.dumps(person, indent=4, separators=("; ", "= "), sort_keys=True)

# 结果为 JSON 字符串
print(person_json) 
print(person_json2)
```

```python
    {"name": "John", "age": 30, "city": "New York", "hasChildren": false, "titles":["engineer", "programmer"]}
    {
        "age"= 30; 
        "city"= "New York"; 
        "hasChildren"= false; 
        "name"= "John"; 
        "titles"= [
            "engineer"; 
            "programmer"
        ]
    }
```

或将Python对象转换为JSON对象，然后使用 `json.dump()` 方法将其保存到文件中。

```python
import json

person = {"name": "John", "age": 30, "city": "New York", "hasChildren": False, "titles": ["engineer", "programmer"]}

with open('person.json', 'w') as f:
    json.dump(person, f) # 你也可以设置缩进等
```

## 从JSON到Python（反序列化，解码）

使用 `json.loads()` 方法将JSON字符串转换为Python对象。 结果将是一个Python字典。

```python
import json
person_json = """
{
    "age": 30, 
    "city": "New York",
    "hasChildren": false, 
    "name": "John",
    "titles": [
        "engineer",
        "programmer"
    ]
}
"""
person = json.loads(person_json)
print(person)
```

```python
    {'age': 30, 'city': 'New York', 'hasChildren': False, 'name': 'John', 'titles': ['engineer', 'programmer']}
```

或从文件加载数据，然后使用 `json.load()`方法将其转换为Python对象。

```python
import json

with open('person.json', 'r') as f:
    person = json.load(f)
    print(person)
```

```python
    {'name': 'John', 'age': 30, 'city': 'New York', 'hasChildren': False, 'titles': ['engineer', 'programmer']}
```

## 使用自定义对象

### 编码

使用默认的 `JSONEncoder` 编码自定义对象将引发 `TypeError`。 我们可以指定一个自定义的编码函数，该函数将类名和所有对象变量存储在字典中。 将此函数用作 `json.dump()` 方法中的 `default` 参数。

```python
import json
def encode_complex(z):
    if isinstance(z, complex):
        # 只是类名的键很重要，值可以是任意的。
        return {z.__class__.__name__: True, "real":z.real, "imag":z.imag}
    else:
        raise TypeError(f"Object of type '{z.__class__.__name__}' is not JSON serializable")

z = 5 + 9j
zJSON = json.dumps(z, default=encode_complex)
print(zJSON)
```

```python
    {"complex": true, "real": 5.0, "imag": 9.0}
```

你还可以创建一个自定义的 Encoder 类，并覆盖 `default()` 方法。 将其用于 `json.dump()` 方法中的 `cls` 参数，或直接使用编码器。

```python
from json import JSONEncoder
class ComplexEncoder(JSONEncoder):
    
    def default(self, o):
        if isinstance(z, complex):
            return {z.__class__.__name__: True, "real":z.real, "imag":z.imag}
        # 让基类的默认方法处理其他对象或引发TypeError
        return JSONEncoder.default(self, o)
    
z = 5 + 9j
zJSON = json.dumps(z, cls=ComplexEncoder)
print(zJSON)
# 或者直接使用编码器
zJson = ComplexEncoder().encode(z)
print(zJSON)
```

```python
    {"complex": true, "real": 5.0, "imag": 9.0}
    {"complex": true, "real": 5.0, "imag": 9.0}
```

### 解码

可以使用默认 JSONDecoder 解码自定义对象，但是它将被解码为字典。 编写一个自定义解码函数，该函数将以字典作为输入，并在可以在字典中找到对象类名称的情况下创建自定义对象。 将此函数用于 `json.load()` 方法中的 `object_hook` 参数。

```python
# 可能但解码为字典
z = json.loads(zJSON)
print(type(z))
print(z)

def decode_complex(dct):
    if complex.__name__ in dct:
        return complex(dct["real"], dct["imag"])
    return dct

# 现在，对象在解码后的类型为complex
z = json.loads(zJSON, object_hook=decode_complex)
print(type(z))
print(z)
```

```python
    <class 'dict'>
    {'complex': True, 'real': 5.0, 'imag': 9.0}
    <class 'complex'>
    (5+9j)
```

## 模板编码和解码函数

如果在 `__init__` 方法中提供了所有类变量，则此方法适用于所有自定义类。

```python
class User:
		# 自定义类在 __init__() 中包含所有类变量
    def __init__(self, name, age, active, balance, friends):
        self.name = name
        self.age = age
        self.active = active
        self.balance = balance
        self.friends = friends
        
class Player:
    # 其他自定义类
    def __init__(self, name, nickname, level):
        self.name = name
        self.nickname = nickname
        self.level = level
          
            
def encode_obj(obj):
    """
    接受一个自定义对象，并返回该对象的字典表示形式。 此字典表示形式还包括对象的模块和类名称。
    """
  
		# 用对象元数据填充字典
    obj_dict = {
      "__class__": obj.__class__.__name__,
      "__module__": obj.__module__
    }
  
    # 用对象属性填充字典
    obj_dict.update(obj.__dict__)
  
    return obj_dict

def decode_dct(dct):
    """
    接受字典并返回与该字典关联的自定义对象。
    它利用字典中的 "__module__" 和 "__class__" 元数据来了解要创建的对象类型。
    """
    if "__class__" in dct:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = dct.pop("__class__")
        
        # Get the module name from the dict and import it
        module_name = dct.pop("__module__")
        
        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)
        
        # Get the class from the module
        class_ = getattr(module,class_name)

        # Use dictionary unpacking to initialize the object
        # Note: This only works if all __init__() arguments of the class are exactly the dict keys
        obj = class_(**dct)
    else:
        obj = dct
    return obj

# User 类适用于我们的编码和解码方法
user = User(name = "John",age = 28, friends = ["Jane", "Tom"], balance = 20.70, active = True)

userJSON = json.dumps(user,default=encode_obj,indent=4, sort_keys=True)
print(userJSON)

user_decoded = json.loads(userJSON, object_hook=decode_dct)
print(type(user_decoded))

# Player 类也适用于我们的编码和解码方法
player = Player('Max', 'max1234', 5)
playerJSON = json.dumps(player,default=encode_obj,indent=4, sort_keys=True)
print(playerJSON)

player_decoded = json.loads(playerJSON, object_hook=decode_dct)
print(type(player_decoded))
```

```python
    {
        "__class__": "User",
        "__module__": "__main__",
        "active": true,
        "age": 28,
        "balance": 20.7,
        "friends": [
            "Jane",
            "Tom"
        ],
        "name": "John"
    }
    <class '__main__.User'>
    {
        "__class__": "Player",
        "__module__": "__main__",
        "level": 5,
        "name": "Max",
        "nickname": "max1234"
    }
    <class '__main__.Player'>
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

