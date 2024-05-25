# 10. 日志记录 — Python 进阶

Python中的日志记录模块是功能强大的内置模块，因此你可以快速将日志记录添加到应用程序中。

```python
import logging
```

<!--more-->

## 日志级别

有5种不同的日志级别指示事件的严重程度。 默认情况下，系统仅记录 *警告(WARNING)* 级别及更高级别的事件。

```python
import logging
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
```

```python
    WARNING:root:This is a warning message
    ERROR:root:This is an error message
    CRITICAL:root:This is a critical message
```

## 配置

使用 `basicConfig(**kwargs)`，你可以自定义根记录器。 最常见的参数是 `level`， `format` 和 `filename`。查看全部可能的参数：[https://docs.python.org/3/library/logging.html#logging.basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig)。查看可能的 format ：[https://docs.python.org/3/library/logging.html#logrecord-attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)。查看如何设置时间字符串：[https://docs.python.org/3/library/time.html#time.strftime](https://docs.python.org/3/library/time.html#time.strftime)。请注意，此函数仅应调用一次，通常在导入模块后首先调用。 如果根记录器已经配置了处理程序，则该设置无效。 例如，在 `basicConfig` 之前调用 `logging.info(...)` 将提前设置处理程序。

```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
# 现在，调试消息也将以其他格式记录。
logging.debug('Debug message')

# 这将记录到文件而不是控制台。
# logging.basicConfig(level=logging.DEBUG, filename='app.log')
```

## 模块内记录和记录器层次结构

在具有多个模块的应用程序中，最佳实践是使用 `__name__` 全局变量创建内部记录器。 这将使用你的模块名称创建一个记录器，并确保没有名称冲突。 日志记录模块创建记录器的层次结构，从根记录器开始，然后将新的记录器添加到该层次结构中。 如果随后将模块导入另一个模块，则可以通过记录器名称将日志消息与正确的模块关联。 请注意，更改根记录器的 `basicConfig` 还将影响层次结构中其他（下部）记录器的日志事件。

```python
# helper.py
# -------------------------------------
import logging
logger = logging.getLogger(__name__)
logger.info('HELLO')

# main.py
# -------------------------------------
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
import helper

# --> 当运行 main.py 时的输出
# helper - INFO - HELLO
```

## 传播

默认情况下，除了附加到创建的记录器的任何处理程序外，所有创建的记录器还将日志事件传递给高级记录器的处理程序。 你可以通过设置 `propagate = False` 来禁用此功能。 有时，当你想知道为什么看不到来自另一个模块的日志消息时，则可能是此属性。

```python
# -------------------------------------
import logging
logger = logging.getLogger(__name__)
logger.propagate = False
logger.info('HELLO')

# main.py
# -------------------------------------
import logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
import helper

# --> 运行main.py时无输出，因为 helper 模块记录器不会将其消息传播到根记录器
```

## 日志处理程序

处理程序对象负责将适当的日志消息调度到处理程序的特定目标。 例如，你可以使用不同的处理程序通过HTTP或通过电子邮件将消息发送到标准输出流，文件。 通常，你为每个处理程序配置一个级别（ `setLevel()` ），一个格式化程序（ `setFormatter()`）和一个可选的过滤器（ `addFilter()` ）。 有关可能的内置处理程序，请参见 [https://docs.python.org/3/howto/logging.html#useful-handlers](https://docs.python.org/3/howto/logging.html#useful-handlers)。 当然，你也可以通过派生这些类来实现自己的处理程序。

```python
import logging

logger = logging.getLogger(__name__)

# 创建处理器
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('file.log')

# 配置级别和格式化程序，并添加到处理器上
stream_handler.setLevel(logging.WARNING) # 警告及以上级别日志记录到流中
file_handler.setLevel(logging.ERROR) # 错误及以上级别记录到文件中

stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

# 添加处理器到日志记录器上
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.warning('This is a warning') # 记录到流中
logger.error('This is an error') # 记录到流和文件中
```

### 过滤器例子

```python
class InfoFilter(logging.Filter):
    
    # 覆盖此方法。 仅此方评估为True的日志记录将通过过滤器。
    def filter(self, record):
        return record.levelno == logging.INFO

# 现在只有 INFO 级别的消息会被记录。
stream_handler.addFilter(InfoFilter())
logger.addHandler(stream_handler)
```

## 其他配置方法

我们已经看到了如何配置日志，从而在代码中显式地创建日志记录器，处理程序和格式化程序。 还有其他两种配置方法：

- 创建日志记录配置文件并使用 `fileConfig()` 函数读取它。 请参见下面的示例。
- 创建配置信息字典并将其传递给 `dictConfig()` 函数。 有关更多信息，请参见[https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)。

### .conf文件

创建一个 *.conf*（或有时存储为 *.ini*）文件，定义记录器，处理程序和格式化程序，并提供名称作为键。 定义其名称后，可以通过在其名称之间用下划线分隔之前添加单词 *logger*， *handler* 和 *formatter* 进行配置。 然后，你可以为每个记录器，处理程序和格式化程序设置属性。 在下面的示例中，将使用 StreamHandler 配置根记录器和名为 *simpleExample* 的记录器。

```python
# logging.conf
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

```python
# 在代码中使用配置文件
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# 使用配置文件中的名称创建记录器。
# 该记录器现在具有带有 DEBUG 级别和指定格式的 StreamHandler
logger = logging.getLogger('simpleExample')

logger.debug('debug message')
logger.info('info message')
```

## 捕获堆栈跟踪

将跟踪记录记录在异常日志中对于解决问题非常有用。 你可以通过将 *excinfo* 参数设置为True来捕获 `logging.error()` 中的回溯。

```python
import logging

try:
    a = [1, 2, 3]
    value = a[3]
except IndexError as e:
    logging.error(e)
    logging.error(e, exc_info=True)
```

```python
    ERROR:root:list index out of range
    ERROR:root:list index out of range
    Traceback (most recent call last):
      File "<ipython-input-6-df97a133cbe6>", line 5, in <module>
        value = a[3]
    IndexError: list index out of range
```

如果未捕获正确的 Exception，则还可以使用 *traceback.formatexc()* 方法记录该异常。

## 滚动 FileHandler

当你有一个大型应用程序将许多事件记录到一个文件中，而你只需要跟踪最近的事件时，请使用RotatingFileHandler来使文件保持较小。 当日志达到一定数量的字节时，它将被“滚动”。 你还可以保留多个备份日志文件，然后再覆盖它们。

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 2KB后滚动，并保留备份日志为 app.log.1, app.log.2 等.
handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
logger.addHandler(handler)

for _ in range(10000):
    logger.info('Hello, world!')
```

## TimedRotatingFileHandler

如果你的应用程序将长时间运行，则可以使用 TimedRotatingFileHandler。 这将根据经过的时间创建一个轮换日志。 *when* 参数的可能时间条件是：

- second (s)
- minute (m)
- hour (h)
- day (d)
- w0-w6 (工作日, 0=星期一)
- midnight

```python
import logging
import time
from logging.handlers import TimedRotatingFileHandler
 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 这将每分钟创建一个新的日志文件，并在覆盖旧日志之前创建一个带有时间戳的5个备份文件。
handler = TimedRotatingFileHandler('timed_test.log', when='m', interval=1, backupCount=5)
logger.addHandler(handler)
 
for i in range(6):
    logger.info('Hello, world!')
    time.sleep(50)
```

## 以JSON格式登录

如果你的应用程序从不同的模块（特别是在微服务体系结构中）生成许多日志，那么定位重要的日志以进行分析可能会很困难。 因此，最佳实践是以JSON格式记录你的消息，并将其发送到集中式日志管理系统。 然后，你可以轻松地搜索，可视化和分析日志记录。

我建议使用此开源JSON记录器：[https://github.com/madzak/python-json-logger](https://github.com/madzak/python-json-logger)

```bash
pip install python-json-logger
```

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

