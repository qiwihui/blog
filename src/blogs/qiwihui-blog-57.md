# 使用 Sphinx 撰写技术文档并生成 PDF 总结

这几天准备编排部分翻译的书籍和文档，找了好些工具，最终定格在 Sphinx 上，并基于 [ReadTheDocs](https://readthedocs.org) 提供的 SaaS 服务进行分发和分享。本篇博客是对整个过程的一次记录和总结。

项目代码：[qiwihui/sphinx-doc-starter](https://github.com/qiwihui/sphinx-doc-starter)

## 认识 Sphinx

[Sphinx](http://sphinx-doc.org/) 是一个基于 Python 的文档生成项目。最早只是用来生成 [Python](https://docs.python.org/3/) 的项目文档，使用 *reStructuredText* 格式。但随着项目的逐渐完善，很多非 Python 的项目也采用 Sphinx 作为文档写作工具，甚至完全可以用 Sphinx 来写书。

使用 [Sphinx 生成文档的优点](http://sphinx-doc-zh.readthedocs.org/en/latest/)包括：

- *丰富的输出格式*: 支持输出为 HTML（包括 Windows 帮助文档），LaTeX（可以打印PDF版本）, manual pages（man 文档）, 纯文本等若干种格式；
- *完备的交叉引用*: 语义化的标签，并可以自动化链接函数、类、引文、术语等；
- *明晰的分层结构*: 轻松定义文档树，并自动化链接同级/父级/下级文章；
- *美观的自动索引*: 可自动生成美观的模块索引；
- *精确的语法高亮*: 基于 Pygments 自动生成语法高亮；
- *开放的扩展*: 支持代码块的自动测试，自动包含 Python 的模块自述文档，等等。

<!--more-->

## 开始

这个过程包括如下步骤：

- 安装 Sphinx
- 第一个文档
- 在线托管
- 生成 PDF

### 安装 Sphinx

Sphinx 依赖于 Python，并提供了 Python 包，所以使用 pip 安装既可。这里我只安装了 `sphinx-doc` 这个包。

```shell
pip install sphinx-doc
```

这时，通过 bash 自动补全（连续两下 `tab`），可以看到有几个命令，Sphinx 推荐使用 `sphinx-quickstart`，这是一个设置向导。

```shell
$ sphinx-
sphinx-apidoc      sphinx-autogen     sphinx-build       sphinx-quickstart
```

### 设置 Sphinx

运行 `sphinx-quickstart`，以下主要设置项目名称，作者名称以及语言（`zh_CN`）即可，其他默认。

```shell
$ sphinx-quickstart
Welcome to the Sphinx 1.8.4 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

Inside the root directory, two more directories will be created; "_templates"
for custom HTML templates and "_static" for custom stylesheets and other static
files. You can enter another prefix (such as ".") to replace the underscore.
> Name prefix for templates and static dir [_]: 

The project name will occur in several places in the built documentation.
> Project name: 一本书
> Author name(s): qiwihui
> Project release []: 0.0.1

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
http://sphinx-doc.org/config.html#confval-language.
> Project language [en]: zh_CN

The file name suffix for source files. Commonly, this is either ".txt"
or ".rst".  Only files with this suffix are considered documents.
> Source file suffix [.rst]: 

One document is special in that it is considered the top node of the
"contents tree", that is, it is the root of the hierarchical structure
of the documents. Normally, this is "index", but if your "index"
document is a custom template, you can also set this to another filename.
> Name of your master document (without suffix) [index]: 
Indicate which of the following Sphinx extensions should be enabled:
> autodoc: automatically insert docstrings from modules (y/n) [n]: 
> doctest: automatically test code snippets in doctest blocks (y/n) [n]: 
> intersphinx: link between Sphinx documentation of different projects (y/n) [n]: 
> todo: write "todo" entries that can be shown or hidden on build (y/n) [n]: 
> coverage: checks for documentation coverage (y/n) [n]: 
> imgmath: include math, rendered as PNG or SVG images (y/n) [n]: 
> mathjax: include math, rendered in the browser by MathJax (y/n) [n]: 
> ifconfig: conditional inclusion of content based on config values (y/n) [n]: 
> viewcode: include links to the source code of documented Python objects (y/n) [n]: 
> githubpages: create .nojekyll file to publish the document on GitHub pages (y/n) [n]: 

A Makefile and a Windows command file can be generated for you so that you
only have to run e.g. `make html` instead of invoking sphinx-build
directly.
> Create Makefile? (y/n) [y]: 
> Create Windows command file? (y/n) [y]: 

Creating file ./source/conf.py.
Creating file ./source/index.rst.
Creating file ./Makefile.
Creating file ./make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file ./source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```

解释1，整个设置过程包括：

1. 是否分离源文件目录 `source` 和生成文件目录 `build`，默认否；
2. 模板目录 `templates` 和静态文件目录 `static` 前缀，默认为`_`；
3. 项目名称；
4. 项目作者；
5. 项目版本，默认为空；
6. 项目语言，默认为 `en`；
7. 文档扩展名，默认为 `.rst`；
8. 首页文件名，默认为 `index`；
9. 开启的扩展，均默认为否：

    - autodoc
    - doctest
    - intersphinx
    - todo
    - coverage
    - imgmath
    - mathjax
    - ifconfig
    - viewcode
    - githubpages

10. 生成 Makefile，默认是；
11. 生成 Windows 用命令行，默认是。

解释2，项目目录文件结构如下：

```shell
sphinx-test
├── Makefile
├── build
├── make.bat
└── source
    ├── _static
    ├── _templates
    ├── conf.py
    └── index.rst
```

其中：

- `Makefile`：可以看作是一个包含指令的文件，在使用 make 命令时，可以使用这些指令来构建文档输出。
- `build`：生成的文件的输出目录。
- `make.bat`：Windows 用命令行。
- `_static`：静态文件目录，比如图片等。
- `_templates`：模板目录。
- `conf.py`：存放 Sphinx 的配置，包括在 `sphinx-quickstart` 时选中的那些值，可以自行定义其他的值。
- `index.rst`：文档项目起始文件。

接下来看看默认生成的内容：

```shell
$ make html
Running Sphinx v1.8.4
loading translations [zh_CN]... done
making output directory...
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 1 source files that are out of date
updating environment: 1 added, 0 changed, 0 removed
reading sources... [100%] index                                                                                                         looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] index                                                                                                          generating indices... genindex
writing additional pages... search
copying static files... done
copying extra files... done
dumping search index in Chinese (code: zh) ... done
dumping object inventory... done
build succeeded.

The HTML pages are in build/html.
```

然后直接在浏览器中打开 `build/html/index.html` 这个文件。

![initial](https://user-images.githubusercontent.com/3297411/53294694-86068e00-3826-11e9-93e6-4f3ad80cc245.png)

默认风格为 `alabaster`，可以改成 ReadTheDocs 的风格： `sphinx_rtd_theme`。

```py
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
```

![rtd_theme](https://user-images.githubusercontent.com/3297411/53294697-9585d700-3826-11e9-9eab-13d1d4e46aa4.png)

### 第一个文档

我们以一下文档为例：

```rst
This is a Title
===============
That has a paragraph about a main subject and is set when the '='
is at least the same length of the title itself.

Subject Subtitle
----------------
Subtitles are set with '-' and are required to have the same length
of the subtitle itself, just like titles.

Lists can be unnumbered like:

 * Item Foo
 * Item Bar

Or automatically numbered:

 #. Item 1
 #. Item 2

Inline Markup
-------------
Words can have *emphasis in italics* or be **bold** and you can define
code samples with back quotes, like when you talk about a command: ``sudo``
gives you super user powers!
```

将之写入 `example.rst` 中，并修改 `index.rst` 为:

```rst
Welcome to 一本书's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: 目录:

   example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

重新编译，这时文档已经改变。

![first_doc](https://user-images.githubusercontent.com/3297411/53294701-a5052000-3826-11e9-972f-85631118b372.png)
![first_doc_page](https://user-images.githubusercontent.com/3297411/53294703-a9c9d400-3826-11e9-9c63-9fd73f19792c.png)


### 在线托管

[ReadTheDocs](https://readthedocs.org) 可是直接用于托管 sphinx 生成的网页文档。
将之前的文档用 Git 管理，并推送到 Github，然后在 ReadTheDocs 中 `Import a Project` 即可。

![rtd](https://user-images.githubusercontent.com/3297411/53294710-dd0c6300-3826-11e9-9b50-f257ccc9049d.png)

另外，可以设置自定义域名：

1. 在域名管理中添加 DNS 的 CNAME 记录到 `readthedocs.io`，比如 `onebook.qiwihui.com`
2. 在项目的 `Admin` -> `Domains` 中设置上一步添加的域名，开启 HTTPS，保存即可。

![add_new_domain](https://user-images.githubusercontent.com/3297411/53294706-b4846900-3826-11e9-8cc7-570d0f6e4430.png)

过程很简单。

### 生成 PDF

Sphinx 生成 PDF 的过程先将 rst 转换为 tex，再生成 PDF。这个过程遇到了比较多的坑，最后总结下来过程如下：

首先，安装 Tex 环境。在 Mac 上，推荐安装 `MacTex` 而不是 `BasicTex`，对于新手来说 BasicTex 上需要自己处理很多依赖问题。完成后使用 `tlmgr` 更新 TexLive。

```shell
$ brew cask install mactex
$ sudo tlmgr update --self
```

然后，在 con.py 中设置 `latex_engine` 和 `latex_elements` 两个参数，同时也可以设置 `latex_documents` 参数来设置文档。因为 ReadTheDocs 上只有 pdflatex 引擎，如果需要同时在 ReadTheDocs 和本地化都能顺利编译中文pdf的话，可以在 conf.py 中添加如下配置：

```py
# -- Options for LaTeX output ------------------------------------------------
# 检查是否为 READTHEDOCS 环境
import os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    latex_elements = {
        'preamble': r'''
\hypersetup{unicode=true}
\usepackage{CJKutf8}
\DeclareUnicodeCharacter{00A0}{\nobreakspace}
\DeclareUnicodeCharacter{2203}{\ensuremath{\exists}}
\DeclareUnicodeCharacter{2200}{\ensuremath{\forall}}
\DeclareUnicodeCharacter{2286}{\ensuremath{\subseteq}}
\DeclareUnicodeCharacter{2713}{x}
\DeclareUnicodeCharacter{27FA}{\ensuremath{\Longleftrightarrow}}
\DeclareUnicodeCharacter{221A}{\ensuremath{\sqrt{}}}
\DeclareUnicodeCharacter{221B}{\ensuremath{\sqrt[3]{}}}
\DeclareUnicodeCharacter{2295}{\ensuremath{\oplus}}
\DeclareUnicodeCharacter{2297}{\ensuremath{\otimes}}
\begin{CJK}{UTF8}{gbsn}
\AtEndDocument{\end{CJK}}
''',
    }
else:
    # 本地
    latex_engine = 'xelatex'
    latex_elements = {
        'papersize': 'a4paper',
        'pointsize': '11pt',
        'preamble': r'''
\usepackage{xeCJK}
\setCJKmainfont[BoldFont=STZhongsong, ItalicFont=STKaiti]{STSong}
\setCJKsansfont[BoldFont=STHeiti]{STXihei}
\setCJKmonofont{STFangsong}
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\parindent 2em
\definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
\setcounter{tocdepth}{3}
\renewcommand\familydefault{\ttdefault}
\renewcommand\CJKfamilydefault{\CJKrmdefault}
'''
    }
# 设置文档
latex_documents = [
    (master_doc, 'sphinx.tex', '你的第一本 Sphinx 书',
     '作者：qiwihui', 'manual', True),
]
```

最后，编译：

```shell
$ make latexpdf
```

`make latexpdf` 会完成 rst转换为 tex 并将 tex 生成 PDF，可以手动分开：

```shell
$ make latex
$ cd build/latex
$ make
```

在 `build/latex` 下可以查看到生成的 PDF 文档。

#### 字体

使用 `fc-list` 来获取字体信息，修改相应字体设置即可。

```shell
$ brew install fontconfig
$ fc-list :lang=zh
```

#### 遇到的问题:

1. 遇到 `"! LaTeX Error: File '*.sty' not found."` 类的问题：

解决：使用 `sudo tlmgr install` 安装相应的包即可。

## 总结

简单过了一下整个文档的流程，总体来说，Sphinx非常适合用来编写项目文档，reStructuredText 比起 Markdown 也有太多的优势，值得推荐。

