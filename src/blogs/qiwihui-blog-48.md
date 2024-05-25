---
title: "在 OS X 上使用 sed 命令的一些注意"
description: "在 OS X 上使用 sed 命令的一些注意"
tags: 
- 技术
top: 48
date: 24/01/2019, 16:32:51
author: qiwihui
update: 31/01/2019, 15:11:44
categories: 技术
---

在 OS X 上使用 `sed` 会和 GNU 上不太一致，在此记录。

1. OS X `sed` 不可忽略备份扩展

<!--more-->
### 不可忽略备份扩展

在 OS X 上进行文本替换时，必须要指定备份扩展，即使扩展可以为空。比如：

```bash
sed -i  's/foo/bar/g' target
```

上面这行代码，可以在 GNU 上运行，作用是将 `foo` 替换为 `bar`，并且直接修改目标文件（`-i`）。但是如果在 OS X 上，这行命令会报错：

```bash
$ sed -i 's/foo/bar/g' target 
sed: 1: "target": undefined label 'arget'
```

原因是在 OS X 上，sed 命令必须指定备份的扩展格式：

```bash
$ man sed

     -i extension
             Edit files in-place, saving backups with the specified extension.  If a zero-length extension is given, no backup will be saved.  It is not recommended to give a
             zero-length extension when in-place editing files, as you risk corruption or partial content in situations where disk space is exhausted, etc.
```

所以需要修改为 

```bash
sed -i '' 's/foo/bar/g' target 
```

没有好的方法避免创建备份文件问题，以下的方法都做不到兼容：

- `sed -i -e ...` - 在 OS X 上不起作用，会创建 `-e` 备份
- `sed -i'' -e ...` - 在 OS X 10.6 不起作用，但在 10.9+ 可行
- `sed -i '' -e ...` - 在 GNU 上不起作用

或者，在 OS X 使用 `gnu-sed` 代替 sed：

```bash
brew install gnu-sed
alias sed=gsed
```

又或者，使用其他命令：

```bash
perl -i -pe's/foo/bar/g' target
```

### 参考

- [sed command with -i option failing on Mac, but works on Linux](https://stackoverflow.com/a/4247319/3218128)

### Comments

