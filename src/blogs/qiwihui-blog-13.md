---
title: "Git 小结"
description: "Git 小结"
tags: 
- 技术
- tips
top: 13
date: 10/09/2018, 13:28:43
author: qiwihui
update: 12/02/2019, 14:14:52
categories: 技术
---

整理自[手把手教你用git](http://www.cnblogs.com/tugenhua0707/p/4050072.html).
<!--more-->

1. `git reflog` 查看历史记录的版本号id
2. Discard:
    * `git reset --hard HEAD^`
    * `git reset --hard HEAD~100`
    * `git reset --hard <one commit>`
3. `git checkout -- <file>`
    + 修改后，还没有放到暂存区，使用 撤销修改就回到和版本库一模一样的状态。
    + 另外一种是第一次修改已经放入暂存区了，接着又作了修改，撤销修改就回到添加暂存区后的状态。
4. 暂存区 -> 工作区
    + `git reset HEAD <file>`
    + HEAD严格来说不是指向提交，而是指向master，master才是指向提交的，所以，HEAD指向的就是当前分支。
5. push
    + `git remote add origin https://github.com/username/project_name.git` 关联一个远程库
    + `git push –u origin master` (第一次要用-u, 以后不需要)
6. 分支管理策略: 
    + 通常合并分支时，git一般使用”Fast forward”模式，在这种模式下，删除分支后，会丢掉分支信息。可以使用带参数 –no-ff来禁用”Fast forward”模式。`git merge --no-ff -m "comments" <branch_name>`
    + 分支策略：首先master主分支应该是非常稳定的，也就是用来发布新版本，一般情况下不允许在上面干活，干活一般情况下在新建的dev分支上干活，干完后，比如上要发布，或者说dev分支代码稳定后可以合并到主分支master上来。
7. `git stash`: 可以把当前工作现场 ”隐藏起来”，等以后恢复现场后继续工作。
    + `git stash list`: 查看
    + 恢复：
        1. `git stash apply` 恢复，恢复后，stash内容并不删除，你需要使用命令`git stash drop`来删除。
        2. 另一种方式是使用`git stash pop`,恢复的同时把stash内容也删除了。
8. 多人协作：
    + 推送分支：
        1. master分支是主分支，因此要时刻与远程同步。
        2. 一些修复bug分支不需要推送到远程去，可以先合并到主分支上，然后把主分支master推送到远程去。
    + 抓取分支：
        1. push非master分支(e.g. dev)：`git checkout  –b dev origin/dev`, edit something, `git push origin dev`
        2. 另一个同伴更新：`git branch --set-upstream dev origin/dev`, `git pull`, edit something, `git push origin dev`
    + 协作模式：
        1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改.
        2. 如果推送失败，则因为远程分支比你的本地更新早，需要先用git pull试图合并。
        3. 如果合并有冲突，则需要解决冲突，并在本地提交。再用`git push origin <branch-name>`推送。
9. delete remote branch
    + `git push origin —delete <branch_name>`
10. get remote branch locally
    + `git branch --set-upstream dev origin/dev`


### Comments

