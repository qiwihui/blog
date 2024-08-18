# 使用 Python 集成 GitHub App 和 GitHub Check API，构建持续集成服务


这篇博客的起因是在做项目的过程中要求使用 Python 完成相应功能，现在将这部份代码按教程的流程发布出来。

原文[《使用 Checks API 创建 CI 测试》](https://docs.github.com/en/free-pro-team@latest/developers/apps/creating-ci-tests-with-the-checks-api)中使用 Ruby，现使用 Python 完成文档示例。由于教程已经将大部分内容详细描述了，本文只列出与原来教程有不同的步骤，以及对应的 Python 代码。

<!--more-->

项目地址：[qiwihui/githubappcheckruns](https://github.com/qiwihui/githubappcheckruns)

## 基本要求

文档：https://docs.github.com/cn/developers/apps/setting-up-your-development-environment-to-create-a-github-app

1. 使用本地测试，利用 smee 转发 github 回调到本地

访问 smee.io 并创建一个新的 channel，比如 https://smee.io/LgDQ8xrhy0q2GeET，然后使用 `pysmee` 命令运行如下命令：

```shell
# 安装
pip install pysmee
# 运行命令
pysmee forward https://smee.io/LgDQ8xrhy0q2GeET http://localhost:5000/events
```

或者使用项目目录 smee 中的 node 脚本运行

```shell
npm i
npm run smee
```

## 第 1 部分 创建检查 API 接口

### 步骤 1.1. 更新应用程序权限

主要为以下权限：

- Repository permissions
  - Checks: Read & write
  - Contents: Read & write
  - Pull requests: Read & write
- Subscribe to events
  - check suite
  - check run

### 步骤 1.2. 添加事件处理

对应于 Ruby 中使用 Sinatra 作为 web 框架，我们使用 `Flask` 作为 web 框架，并结合 `PyGithub` 这个库提供的 github API 封装，由于 PyGithub 在发布的版本中还未集成 check run 对应的 API，所以使用其 `master` 分支上的代码，添加 `git+https://github.com/PyGithub/PyGithub.git` 到 requirements.txt 中。

```python
app = Flask(__name__)
APP_NAME = "Octo PyLinter"

app.config["GITHUB_APP_ID"] = config.GITHUB_APP_ID
app.config["GITHUB_KEY_FILE"] = config.GITHUB_KEY_FILE
app.config["GITHUB_SECRET"] = config.GITHUB_SECRET
app.config["GITHUB_APP_ROUTE"] = config.GITHUB_APP_ROUTE

github_app = GithubAppFlask(app)

@github_app.on(
    [
        "check_suite.requested",
        "check_suite.rerequested",
        "check_run.rerequested",
    ]
)
def create_check_run():
    pass
    client = github_app.github_app_installation.get_github_client()
    head_sha = (
        github_app.payload["check_run"]
        if "check_run" in github_app.payload
        else github_app.payload["check_suite"]["head_sha"]
    )
    repo = client.get_repo(github_app.payload["repository"]["full_name"])
    repo.create_check_run(name=APP_NAME, head_sha=head_sha)
```

其中，`GithubAppFlask` 提供三个功能：

1. 提供 github_app 封装；
2. 提供 `on` 装饰器，对于不同 github 动作分发处理；
3. github webhook 认证；

### 步骤 1.3. 创建 check run

使用 PyGithub 库的 `create_check_run` 处理

```python

def create_check_run():
    client = github_app.github_app_installation.get_github_client()
    head_sha = (
        github_app.payload["check_run"]
        if "check_run" in github_app.payload
        else github_app.payload["check_suite"]["head_sha"]
    )
    repo = client.get_repo(github_app.payload["repository"]["full_name"])
    repo.create_check_run(name=APP_NAME, head_sha=head_sha)

```

## 步骤 1.4. 更新 check run

```py
@github_app.on(["check_run.created"])
def initiate_check_run():
    """Start the CI process"""

    # Check that the event is being sent to this app
    if str(github_app.payload["check_run"]["app"]["id"]) == config.GITHUB_APP_ID:
        client = github_app.github_app_installation.get_github_client()
        repo = client.get_repo(github_app.payload["repository"]["full_name"])
        check_run = repo.get_check_run(github_app.payload["check_run"]["id"])
        # Mark the check run as in process
        check_run.edit(
            name=APP_NAME,
            status="in_progress",
            started_at=datetime.now(),
        )

        # ***** RUN A CI TEST *****
        # 暂略

        # Mark the check run as complete!
        check_run.edit(
            name=APP_NAME,
            status="completed",
            completed_at=datetime.now(),
            conclusion=conclusion
        )
```

## 第 2 部分 创建 Octo RuboCop CI 测试

原教程使用 RuboCop 作为 ruby 代码语法检查和格式化工具，相对应，我们使用 `pylint` 作为 python 代码语法检查，使用 `autopep8` 作为格式化工具。
同样，对于git项目的操作，我们使用 `GitPython` 简化操作。

## 步骤 2.1. 添加 Python 文件

添加要操作的 python 文件即可。

### 步骤 2.2. 克隆仓库

使用 GitPython 库处理，使用临时目录进行克隆。

```python
def clone_repository(full_repo_name, repository, ref, installation_token, clean=False):
    repo_dir = tempfile.mkdtemp()
    git.Git(repo_dir).clone(f"https://x-access-token:{installation_token}@github.com/{full_repo_name}.git")
    # pull and chekout
    repo = git.Repo(f"{repo_dir}/{repository}")
    repo.git.pull()
    repo.git.checkout(ref)
    if clean:
        shutil.rmtree(tempdir, ignore_errors=True)
    return repo_dir
```

运行 CI 测试：

```py
        # ***** RUN A CI TEST *****
        full_repo_name = github_app.payload["repository"]["full_name"]
        repository = github_app.payload["repository"]["name"]
        head_sha = github_app.payload["check_run"]["head_sha"]
        repo_dir = clone_repository(
            full_repo_name,
            repository,
            head_sha,
            installation_token=github_app.github_app_installation.token,
            clean=True,
        )
```

### 步骤 2.3. 运行 pylint

pylint 运行并输出json结果。

```py
        command = f"pylint {repo_dir}/{repository}/**/*.py -f json"
        report = subprocess.getoutput(command)
        shutil.rmtree(repo_dir)
        output = json.loads(report)
```

### 步骤 2.4. 收集 pylint 错误

pylint结果与 `rubocop` 类似，收集并解析结果：

```py
        # lint
        max_annotations = 50

        annotations = []

        # RuboCop reports the number of errors found in "offense_count"
        if len(output) == 0:
            conclusion = "success"
            actions = None
        else:
            conclusion = "neutral"
            for file in output:

                file_path = re.sub(f"{repo_dir}/{repository}/", "", file["path"])
                annotation_level = "notice"

                # Parse each offense to get details and location
                # Limit the number of annotations to 50
                if max_annotations == 0:
                    break
                max_annotations -= 1

                start_line = file["line"]
                end_line = file["line"]
                start_column = file["column"]
                end_column = file["column"]
                message = file["message"]

                # Create a new annotation for each error
                annotation = {
                    "path": file_path,
                    "start_line": start_line,
                    "end_line": end_line,
                    "start_column": start_column,
                    "end_column": end_column,
                    "annotation_level": annotation_level,
                    "message": message,
                }
                # # Annotations only support start and end columns on the same line
                # if start_line == end_line:
                #     annotation.merge({"start_column": start_column, "end_column": end_column})

                annotations.append(annotation)
            
            # Need fix action
            actions = [
                {
                    "label": "Fix this",
                    "description": "Automatically fix all linter notices.",
                    "identifier": "fix_rubocop_notices",
                }
            ]
```

### 步骤 2.5. 使用 CI 测试结果更新检查运行

整理结果，并添加修复动作：

```py
        summary = (
            f"Summary\n"
            f"- Offense count: {len(output)}\n"
            f"- File count: {len(set([file['path'] for file in output]))}\n"
        )
        text = "Octo Pylinter version: pylint"
        # Mark the check run as complete!
        check_run.edit(
            name=APP_NAME,
            status="completed",
            completed_at=datetime.now(),
            conclusion=conclusion,
            output={
                "title": "Octo Pylinter",
                "summary": summary,
                "text": text,
                "annotations": annotations,
            },
            actions=actions,
        )
```

### 步骤 2.6. 自动修复错误

沿用 `fix_rubocop_notices` 这个 ID，使用 `autopep8` 做 python 文件的修正，将结果以 PR 的方式提交。

```py
@github_app.on(["check_run.requested_action"])
def take_requested_action():
    full_repo_name = github_app.payload["repository"]["full_name"]
    repository = github_app.payload["repository"]["name"]
    head_branch = github_app.payload["check_run"]["check_suite"]["head_branch"]
    check_run_id = github_app.payload["check_run"]["id"]

    if github_app.payload["requested_action"]["identifier"] == "fix_rubocop_notices":
        repo_dir = clone_repository(
            full_repo_name,
            repository,
            head_branch,
            installation_token=github_app.github_app_installation.token,
        )
        # Automatically correct style errors
        # fix with autopep8
        command = f"autopep8 -a -i {repo_dir}/{repository}/**/*.py"
        report = subprocess.getoutput(command)

        # create new branch
        new_branch = f"fix_rubocop_notices_{check_run_id}"
        pushed = False
        try:
            repo = git.Repo(f"{repo_dir}/{repository}")
            if repo.index.diff(None) or repo.untracked_files:
                current = repo.create_head(new_branch)
                current.checkout()
                repo.config_writer().set_value("user", "name", config.GITHUB_APP_USER_NAME).release()
                repo.config_writer().set_value("user", "email", config.GITHUB_APP_USER_EMAIL).release()
                repo.git.add(update=True)
                repo.git.commit("-m", "Automatically fix Octo RuboCop notices.")
                repo.git.push("--set-upstream", "origin", current)
                pushed = True
            else:
                print("no changes")
        except:
            print("failed to commit and push")
            # # Nothing to commit!
            # print("Nothing to commit")
        finally:
            shutil.rmtree(repo_dir, ignore_errors=True)

        if pushed:
            # create pull request
            client = github_app.github_app_installation.get_github_client()
            repo = client.get_repo(full_repo_name)
            body = """Automatically fix Octo RuboCop notices."""
            pr = repo.create_pull(
                title="Automatically fix Octo RuboCop notices.", body=body, head=new_branch, base="master"
            )
            print(f"Pull Request number: {pr.number}")
```

在以上步骤的基础上，可以构建更复杂的测试过程，完成不同的需求。

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/111)


