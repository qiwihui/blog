---
title: "Git合并提交"
description: "Git合并提交"
tags: 
- 技术
- tips
top: 70
date: 09/05/2019, 14:40:55
author: qiwihui
update: 09/05/2019, 14:40:55
categories: 
---

在日常开发中，我们的Git提交原则经常是小功能多次提交，但是有时需要在完成功能之后将多个连续的提交合并成一个，或者进行分支合并时，只保留一个提交，以保证分支简介，这时就需要进行squash操作，两种分别称为 Rebase Squash 和 Merge Squash。这篇tip主要记录如何处理这两种操作以及之间的区别，

<!--more-->

## Rebase Squash

用来将多个连续的提交合并为一个，以下面的提交记录为例，`master`是主分支，分支 `featureY` 提交了一系列的修改：

```shell
$ git lg
* 392dc11 - (HEAD -> featureY) Y5 (5 minutes ago) <qiwihui>
* 740e7d2 - Y4 (5 minutes ago) <qiwihui>
* b54cd87 - Y3 (5 minutes ago) <qiwihui>
* fb3a5cf - Y2 (6 minutes ago) <qiwihui>
* 61b5ff9 - Y1 (6 minutes ago) <qiwihui>
* 220e45c - (master) feature X (7 minutes ago) <qiwihui>
```

其中，`lg` 是如下命令：

```conf
[alias]
        lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --
```

这里我们需要合并 `featureY` 功能分支上的 `Y1` 到 `Y5` 这五个提交为一个。git提供了如下命令：

```shell
git rebase --interactive HEAD~[N]
# 或者
git rebase -i HEAD~[N]
```

其中 `[N]` 表示需要合并的数量，从最近一个提交开始数，这里为`5`。在命令行输入 `git rebase --interactive HEAD~5` 进入编辑器进行选择。
注意，这里的提交顺序是 **反** 的，从最早的 `Y1` 开始：

```shell
pick 61b5ff9 Y1
pick fb3a5cf Y2
pick b54cd87 Y3
pick 740e7d2 Y4
pick 392dc11 Y5
```

对应需要合并的提交，将`pick`改成`squash`（或者简化为`s`），修改之后为：

```shell
pick 61b5ff9 Y1
s fb3a5cf Y2
s b54cd87 Y3
s 740e7d2 Y4
s 392dc11 Y5
```

保存并关闭编辑器，这是编辑器会自动跳出并需要你提交一个新的提交：

```shell
# This is a combination of 5 commits.
# This is the 1st commit message:

Y1

# This is the commit message #2:

Y2

# This is the commit message #3:

Y3

# This is the commit message #4:

Y4

# This is the commit message #5:

Y5

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# Date:      Thu May 9 13:45:03 2019 +0800
#
# interactive rebase in progress; onto 220e45c
# Last commands done (5 commands done):
#    squash 740e7d2 Y4
#    squash 392dc11 Y5
# No commands remaining.
# You are currently rebasing branch 'featureY' on '220e45c'.
#
# Changes to be committed:
#    new file:   featY
#
```

可以看到，Git提供了详细的信息指导提交，只需要修改成你需要的信息即可，比如 `featureY`，然后保存。这时就完成了修改，修改之后的提交信息如下：

```shell
$ git lg
* 1b07941 - (HEAD -> featureY) featureY (3 minutes ago) <qiwihui>
* 220e45c - (master) feature X (36 minutes ago) <qiwihui>
```

## Merge Squash

用于在合并分支时，最后只在合并后的分支上保留一个提交。同样以上面的代码提交为例子。

```shell
$ git lg
* 392dc11 - (HEAD -> featureY) Y5 (5 minutes ago) <qiwihui>
* 740e7d2 - Y4 (5 minutes ago) <qiwihui>
* b54cd87 - Y3 (5 minutes ago) <qiwihui>
* fb3a5cf - Y2 (6 minutes ago) <qiwihui>
* 61b5ff9 - Y1 (6 minutes ago) <qiwihui>
* 220e45c - (master) feature X (7 minutes ago) <qiwihui>
```

```shell
$ git checkout master
$ git merge --squash featureY  
Updating 220e45c..392dc11
Fast-forward
Squash commit -- not updating HEAD
 featY | 5 +++++
 1 file changed, 5 insertions(+)
 create mode 100644 featY
```

此时，分支`featureY`保持不变，同时在`master`上多了一个未被提交的更改：

![git-merge-squash](https://user-images.githubusercontent.com/3297411/57431740-503e4680-7266-11e9-88d3-a9a0cb3fb7a5.png)

```shell
$ git status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        new file:   featY
```

这些更改是分支`featureY`中所有提交的合并，现在只需要提交这些更改就可以了：

```shell
git commit -m "featureY"
```

## 区别

从以上的擦坐过程可以看出两者之间的差别：Rebase Squash会合并之前的提交，之前的记录会消失，而Merge Squash只会在合并的分支上新生成提交，原来的那些提交熬还会保留。

## 多说一点

如果需要合并的提交数量很多，数数容易出错，可以使用提交哈希来识别：

```shell
git rebase --interactive [commit-hash]
```

这个`[commit-hash]`是*需要合并的提交之前的一个提交*：

```shell
$ git lg
* 392dc11 - (HEAD -> featureY) Y5 (5 minutes ago) <qiwihui>
* 740e7d2 - Y4 (5 minutes ago) <qiwihui>
* b54cd87 - Y3 (5 minutes ago) <qiwihui>
* fb3a5cf - Y2 (6 minutes ago) <qiwihui>
* 61b5ff9 - Y1 (6 minutes ago) <qiwihui>
* 220e45c - (master) feature X (7 minutes ago) <qiwihui>
```

这里，需要使用 `220e45c` 而不是 `61b5ff9`。

## 参考

- [Squash commits into one with Git](https://www.internalpointers.com/post/squash-commits-into-one-git)


### Comments

