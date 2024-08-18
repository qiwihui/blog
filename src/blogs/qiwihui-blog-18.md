# 使用 Git Hooks 实现项目自动部署


自动化部署解放双手，发展生产力，更重要的是可以减少部署过程中的错误操作。
<!--more-->

之前使用git做为我博客的版本控制，使用Github Pages托管我的博客，所以部署方面都交给了github，
但是当我要部署另一个web应用时，显然要部署在自己的VPS上，把VPS做为git服务器的同时，每次push
代码到服务器上都要手动运行一次脚本更新服务，这样做简直劳神伤力。

幸运的是Git提供了Hook机制用来帮助我们实现自动部署。Hooks分为客户端和服务端，可以用来处理不同
的工作，这些hooks都被存储在 Git 目录下的hooks子目录中，
即大部分项目中的`.git/hooks`。 Git 默认会放置一些脚本样本在这个目录中，除了可以作为hooks使用，
这些样本本身是可以独立使用的，这些样本名都是以.sample结尾，必须重新命名。

这次主要用到服务端的hooks: `post-receive`。当用户在本地仓库执行`git push`命令时，服务器上运端
仓库就会对应执行`git receive pack`命令；在所有远程仓库的引用(ref)都更新后，这个钩子就会被调用。
与之对应的是`pre-receive`，这个会在更新之前被调用。

环境要求：

1. 要求客户端和服务端都有git环境，而且服务端最好已经部署好了；
2. 能连上服务器

## 0x01 实践

我们的实践过程会按照下边的过程实施：

```

  +------------------------+          +------------------------+
  |                        |          |                        |
  |  +-----------------+   |   push   |  +-------------------+ |
  |  |local repository |---+----------+->| remote repository | |
  |  +-----------------+   |          |  +-------------------+ |
  |                        |          |             |          |
  +------------------------+          |             |pull      |
                                      |             V          |
       local machine                  |  +-------------------+ |
                                      |  |     deployment    | |
                                      |  +-------------------+ |
                                      |                        |
                                      +------------------------+

                                               server

```

#### 在server上初始化一个远程裸仓库：

```bash
$ cd ~
$ mkdir remoteRepo
$ cd remoteRepo
$ git init --bare webapp.git
```

#### 在server上初始化一个本地仓库，做为web app的代码：

```bash
$ cd ~
$ mkdir deployment
$ cd deployment
$ git clone ~/remoteRepo/webapp.git webapp
```

#### 为远程仓库添加hook：

```bash
$ cd ~/remoteRepo/webapp.git/hooks
$ vim post-receive
$ cat post-receive
```

`post-receive`中的命令：

```
#!/bin/sh
# Check the remote git repository whether it is bare
IS_BARE=$(git rev-parse --is-bare-repository)
if [ -z "$IS_BARE" ]; then
    echo >&2 "fatal: post-receive: IS_NOT_BARE"
    exit 1
fi

unset GIT_DIR
# current user is git
DeployPath=/home/git/deployment/webapp
if [ ! -d $DeployPath ] ; then
    echo >&2 "fatal: post-receive: DEPLOY_DIR_NOT_EXIST: \"$DeployPath\""
    exit 1
fi

cd $DeployPath
git add . -A && git stash
git pull origin master
```

为`post-receive`添加可执行权限

```bash
chmod +x post-receive
```

#### 为local machined的本地仓库添加远程仓库源：

```bash
cd <your-local-repository-folder>
$ git remote add deploy git@<server.ip>:/home/git/remoteRepo/webapp.git

# then you need to merge conflict between local changes and deploy/master before you push it.
# 'git merge remotes/deploy/master' or some other git commands.

$ git push deploy master
```

或者从头开始创建一个项目：

```bash
git init
```

这样，当我们在本地完成更新并push到server上时，这些代码就会被自动更新。

## 0x02 后来

#### 改进1

可以在最初在server上创建裸仓库时使用local machine上的现有项目，即将local machine上
的项目仓库导出为裸仓库 — 即一个不包含当前工作目录的仓库：

```bash
$ git clone --bare my_project my_project.git
```

或者

```bash
$ cp -Rf my_project/.git my_project.git
```

然后将这个裸仓库移到server上

```bash
$ scp -r my_project.git git@<server.ip>:/home/git/remoteRepo
```

之后，其他人要进行更新时就可以clone这个项目了：

```bash
$ git clone git@<server.ip>:/home/git/remoteRepo/my_project.git
```

#### 改进2

有一种情况是当本地更新了webapp，结果push到远程仓库后这个更新被reset了（虽然我觉得这个问题应该避免，
但是还是有可能发生），这是，简单地在hook中使用`git push deploy master`是无法完成这个过程的，因为
远端的代码版本低于deploy端的代码版本，再使用pull的时候就不能实现同步，这时就应该使用另一种方式
更新代码：

```bash
git fetch --all
git reset --hard origin/master
```

即`git reset`把HEAD 指向了新下载的未合并的节点，也就是在local machine上reset之后的。

参考：[git 放弃本地修改 强制更新](http://blog.csdn.net/a06062125/article/details/11727273)


[View on GitHub](https://github.com/qiwihui/blog/issues/18)


