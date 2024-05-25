---
title: "重命名本地和远程 Git 分支名称"
description: "重命名本地和远程 Git 分支名称"
tags: 
- 技术
- tips
top: 54
date: 12/02/2019, 14:12:50
author: qiwihui
update: 12/02/2019, 14:12:50
categories: 技术
---

如果不小心写错了分支名称又将分支推送到了远端，这时可以使用以下步骤进行修正：

<!--more-->

1. 重命名本地分支：

    ```shell
    git branch -m old-name new-name
    ```

    若当前在 `old-name` 分支上，则可以省略 `old-name`：

    ```shell
    git branch -m new-name
    ```

2. 删除远程老分支：

    ```shell
    git push origin :old-name
    ```

3. 推送新的本地分支，并设置本地新分支追踪远程分支：

    ```shell
    git push origin -u new-name
    ```

### Comments

