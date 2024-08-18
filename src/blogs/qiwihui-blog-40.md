# Making kernels for jupyter


一个内核是运行和解析用户代码的程序。IPython包含了一个运行和解析Python代码的内核，而且人们已经写了多种语言的内核。

当Jupyter开始一个内核的时候，它会传递它一个连接文件。它指定了如何与前端开始通信。

<!--more-->
以下是实践：

### 安装环境

```shell
$ conda create -n py365400 python=3.6.5 jupyter ipykernel
$ conda activate py365
```

### 列出当前内核

在Unix系统中，可用的内核列在如下文件夹中（[Kernel specs](https://jupyter-client.readthedocs.io/en/latest/kernels.html#kernel-specs)）:

System:

  - `/usr/share/jupyter/kernels`
  - `/usr/local/share/jupyter/kernels`

Env:

  - `{sys.prefix}/share/jupyter/kernels`

User:

  - `~/.local/share/jupyter/kernels (Linux)`
  - `~/Library/Jupyter/kernels (Mac)`

用户位置的优先级高于系统级别的，忽略名字的大小写。因此不论系统是否大小写敏感，都可以以同样的烦噶事来获取内核。因为内核名字会在URL出现，因此内核名字需要是一个简单的，只使用ASCII字母，数字和简单的分隔符`-`，`.`， `_`。
如果设置了 `JUPYTER_PATH` 环境变量的话，也会搜索其他位置。

例如在我的Mac上，有两个个内核，一个是 python 3 的，另一个是 pyspark(python 2) 的。

```shell
$  jupyter kernelspec list
Available kernels:
  pyspark2    /Users/qiwihui/Library/Jupyter/kernels/pyspark2
  python3     /usr/local/miniconda3/envs/py365/share/jupyter/kernels/python3
```

在内核文件夹下，现在会使用三种类型的文件。`kernel.json`, `kernel.js`和log图片文件。目前，没有使用其他文件，但是将来可能会改变。

最重要的文件是 `kernel.json`，应该是一个json序列化的字典包含以下字段

- `argv`: 用来启动内核的命令行参数列表。`{connection_file}` 将会被实际的连接文件的路径替换。
- `display_name`: 在UI上展示的内核名字。不像在API中使用的内核名字，这里的名字可以包含任意字符。
- `language`: 内核的语言名字。当载入notebook的时候，如果没有找到匹配的内核，那么匹配相应语言的内核将会被启动。这样允许一个写了任何Python或者julia内核的notebook可以与用户的Python或者julia内核合适的联系起来，即使它们没有在与用户内核同样的名字下。
- `interrupt_mode`：可能是signal或者message指定了客户端如何在这个内核中停止单元运行。是通过发送一个信号呢，还是发送一个`interrupt_request`消息在`control channel`。如果没有指定，将默认使用signal模式。
- `env`：为内核设置的环境变量。在内核启动前，会添加到当前的环境变量里。
- `metadata`：关于这个内核的其他相关属性。帮助客户端选择内核。

比如：

```shell
$ cat /usr/local/miniconda3/envs/py365/share/jupyter/kernels/python3/kernel.json 
{
 "argv": [
  "/usr/local/miniconda3/envs/py365/bin/python",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python 3",
 "language": "python"
}
```

当内核开始的时候将会传入一个连接文件的路径，这个文件只对当前用户可用，会包含类似下面的一个JSON字典。

```json
{
  "control_port": 50160,
  "shell_port": 57503,
  "transport": "tcp",
  "signature_scheme": "hmac-sha256",
  "stdin_port": 52597,
  "hb_port": 42540,
  "ip": "127.0.0.1",
  "iopub_port": 40885,
  "key": "a0436f6c-1916-498b-8eb9-e81ab9368e84"
}
```

`transport`, `ip` 和设定了该使用 ZeroMQ 绑定的五个_port。比如 shell 套接字的地址应该是：`tcp://127.0.0.1:57503`。在每个内核开始的时候会指定随意的端口。`signature_scheme` 和 `key` 用来加密信息，因此系统的其他用户不能发送代码来运行内核。

现在我需要自己定义一个内核，这个内核可以执行我们定义的逻辑。

### 添加新内核

这是简单的重用 IPython  的内核机制来实现这个新的内核。

步骤：

子类化ipykernel.kernelbase.Kernel，然后实现下面的方法和属性

class MyKernel

    - implementation
    - implementation_version
    - banner
        Kernel info会返回的信息。Implementation指的是内核而不是语言，比如IPython而不是Python。banner是在控制UI上显示第一个提示符之前的东西。这些都是字符串

    - language_info
        Kernel info会返回的信息字典。应该包含mimetype键，值是目标语言的mimetype，比如text/x-python。name键是实现的语言比如python，file_extension比如.py，而且也可能根据不同语言包含codemirror_mode和pygments_lexer

    - do_execute(code, silent, store_history=True, user_expressions=None, allow_stdin=False)

        执行用户代码

            - code：要执行的代码
            - silent：是否展示输出
            - store_history: 是否在历史里记录代码，并且增加执行次数。
            - user_expressions：在代码被执行后对这些表达式求值
            - allow_stdin：前端是否提供输入请求

        你的方法应该返回一个字典，包含在Execution results规定的字典。为了展现输出，它可以使用send_response() 来发送消息。

为了启动你的内核，在模块后面加上：

```py
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MyKernel)
```

现在创建一个JSON的内核说明文件，然后通过 `jupyter kernelspec install </path/to/kernel>`。将你的内核模块放在Python可以导入的地方，一般是当前目录(做测试)。最后，你可以使用 `jupyter console --kernel <mykernelname>` 来运行你的内核。

例子：

```shell
$ ls echo/
echokernel.py kernel.json
```

`echokernel.py`:

```py
from ipykernel.kernelbase import Kernel

class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=EchoKernel)
```

`kernel.json`:

```json
{
    "argv":["python","-m","echokernel", "-f", "{connection_file}"],
    "display_name":"Echo"
}
```

安装

```
$ jupyter kernelspec install echo --user
```

这里，只为当前用户添加这个kernel。

### 查看

```shell
$ jupyter notebook
```

选择新创建的内核创建 notebook，并运行代码。

![jupyter with new kernel echo](https://user-images.githubusercontent.com/3297411/47489844-1bdedc00-d87a-11e8-8294-3c412fbcdb52.png)

![image](https://user-images.githubusercontent.com/3297411/47490179-bf2ff100-d87a-11e8-85b3-3469efa7edc2.png)

### 一些坑

1. 运行 notebook 时无法找到 `echokernel` 模块：

```shell
[I 15:48:27.754 NotebookApp] Kernel started: 77759cfa-db55-4b70-be23-c14d69f8d87d
/usr/local/miniconda3/envs/py365/bin/python: No module named echokernel
[I 15:48:30.750 NotebookApp] KernelRestarter: restarting kernel (1/5), new random ports
/usr/local/miniconda3/envs/py365/bin/python: No module named echokernel
[I 15:48:33.766 NotebookApp] KernelRestarter: restarting kernel (2/5), new random ports
/usr/local/miniconda3/envs/py365/bin/python: No module named echokernel
[I 15:48:36.789 NotebookApp] KernelRestarter: restarting kernel (3/5), new random ports
/usr/local/miniconda3/envs/py365/bin/python: No module named echokernel
[I 15:48:39.812 NotebookApp] KernelRestarter: restarting kernel (4/5), new random ports
/usr/local/miniconda3/envs/py365/bin/python: No module named echokernel
```

需要将 `echokernel.py` 放置在 python PATH 中 ，这样在执行命令时才能访问到。

### 更多命令

```sh
$ jupyter kernelspec help
Manage Jupyter kernel specifications.

Subcommands
-----------

Subcommands are launched as `jupyter kernelspec cmd [args]`. For information on
using subcommand 'cmd', do: `jupyter kernelspec cmd -h`.

list
    List installed kernel specifications.
install
    Install a kernel specification directory.
uninstall
    Alias for remove
remove
    Remove one or more Jupyter kernelspecs by name.
install-self
    [DEPRECATED] Install the IPython kernel spec directory for this Python.

To see all available configurables, use `--help-all`
```

### 删除内核

```shell
$ jupyter kernelspec uninstall echo
```


### 参考

 - [Making simple Python wrapper kernels](https://jupyter-client.readthedocs.io/en/stable/wrapperkernels.html)
 - [题 如何将python3内核添加到jupyter（IPython）](http://landcareweb.com/questions/879/ru-he-jiang-python3nei-he-tian-jia-dao-jupyter-ipython)
 - [翻译 - Making kernels for Jupyter](https://skyrover.me/2017/12/07/making_kernels_for_jupyter/)

[View on GitHub](https://github.com/qiwihui/blog/issues/40)


