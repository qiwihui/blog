---
title: "用 Rust Actix-web 写一个 Todo 应用（一）── Hello world 和 REST 接口"
description: "用 Rust Actix-web 写一个 Todo 应用（一）── Hello world 和 REST 接口"
tags: 
- 技术
- Rust
top: 105
date: 20/10/2020, 13:46:39
author: qiwihui
update: 26/10/2020, 15:27:56
categories: 技术
---

## Actix

actix 是 Rust 生态中的 Actor 系统。actix-web 是在 actix actor 框架和 Tokio 异步 IO 系统之上构建的高级 Web 框架。

本篇博客实践使用 actix-web 实现一个简单的 todo 应用。基本要求：了解 rust 基本语法，了解一定的 sql 和 docker 知识。

<!--more-->

## 创建一个 Hello world 程序

首先，新建一个 `todo-list` 项目，并在其中增加 `actix-web` 依赖，我们使用最新的 actix 3.0。

```shell
cargo new todo-list
cd todo-list
```

`Cargo.toml`：

```toml
[package]
name = "todo-list"
version = "0.1.0"
authors = ["qiwihui <qwh005007@gmail.com>"]
edition = "2018"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
actix-web = "3"
```

在 `main.rs` 中，使用类似于 python flask 的语法，增加一个最简单的 service。

```rust
use actix_web::{get, App, HttpServer, Responder};
use std::io::Result;

#[get("/")]
async fn hello() -> impl Responder {
    // String 实现了 Responder trait
    format!("Hello world!")
}

#[actix_web::main]
async fn main() -> Result<()> {
    println!("Starting server at http://127.0.0.1:8000");
    HttpServer::new(|| App::new().service(hello))
        .bind("127.0.0.1:8000")?
        .run()
        .await
}
```

运行并测试：

```shell
cargo run
```

在另一个终端中

```shell
$ curl 127.0.0.1:8000
Hello world!
```

## 数据库设计

项目中将使用 postgres 作为数据库存储，为了方便操作和管理，我们使用 docker-compose 进行管理。

`docker-compose.yml`

```yml
version: "3"

services:
  postgres:
    image: postgres:11-alpine
    container_name: postgres
    restart: always
    environment:
      POSTGRES_PASSWORD: actix
      POSTGRES_USER: actix
      POSTGRES_DB: actix
    ports:
      - 5432:5432
```

创建数据库：

```shell
docker-compose up -d
```

然后，我们设计整体数据库表结构，并创建一些基础数据作为测试。表结构如下：

```text

 TodoList           TodoItem
                   +---------+
                   |  id     |
+-------+          +---------+
|  id   + <-- FK --+ list_id |
+-------+          +---------+
| title |          | title   |
+-------+          +---------+
                   | checked |
                   +---------+

```

在 `database.sql` 中手动创建表结构并插入数据：

```sql
drop table if exists todo_list;

drop table if exists todo_item;

create table todo_list (
    id serial primary key,
    title varchar(150) not null
);

create table todo_item (
    id serial primary key,
    title varchar(150) not null,
    checked boolean not null default false,
    list_id integer not null,
    foreign key (list_id) references todo_list(id)
);

insert into
    todo_list (title)
values
    ('List 1'),
    ('List 2');

insert into
    todo_item (title, list_id)
values
    ('item 1', 1),
    ('item 2', 1);
```

创建数据表并查看结果

```shell
$ psql -h 127.0.0.1 -p 5432 -U actix actix < database.sql 
Password for user actix: 
NOTICE:  table "todo_list" does not exist, skipping
DROP TABLE
NOTICE:  table "todo_item" does not exist, skipping
DROP TABLE
CREATE TABLE
CREATE TABLE
INSERT 0 2
INSERT 0 2
```

```shell
$ psql -h 127.0.0.1 -p 5432 -U actix actix
Password for user actix: 
psql (12.4, server 11.9)
Type "help" for help.

actix=# \d
              List of relations
 Schema |       Name       |   Type   | Owner 
--------+------------------+----------+-------
 public | todo_item        | table    | actix
 public | todo_item_id_seq | sequence | actix
 public | todo_list        | table    | actix
 public | todo_list_id_seq | sequence | actix
(4 rows)

actix=# select * from todo_list;
 id | title  
----+--------
  1 | List 1
  2 | List 2
(2 rows)
```

## 获取 todo 列表

首先，添加我们需要的库，其中 `serde` 用于序列化，`tokio-postgres` 是一直支持异步的 PostgreSQL 客户端，`deadpool-postgres` 用于连接池的管理。

```toml
[dependencies]
actix-web = "3"
serde="1.0.117"
deadpool-postgres = "0.5.0"
tokio-postgres = "0.5.1"
```

增加 `models.rs` 用于管理数据模型，并支持序列化和反序列化。

```rust
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct TodoList {
    pub id: i32,
    pub title: String,
}

#[derive(Serialize, Deserialize)]
pub struct TodoItem {
    pub id: i32,
    pub title: String,
    pub checked: bool,
    pub list_id: i32,
}
```

增加 `db.rs` 用于管理数据操作，例如 `get_todos` 从数据库中获取数据并序列化为 `TodoList` 的数组：

```rust
use crate::models::{TodoItem, TodoList};
use deadpool_postgres::Client;
use std::io::Error;
use tokio_postgres::Row;

// 将每条记录转为 TodoList
fn row_to_todo(row: &Row) -> TodoList {
    let id: i32 = row.get(0);
    let title: String = row.get(1);
    TodoList { id, title }
}

pub async fn get_todos(client: &Client) -> Result<Vec<TodoList>, Error> {
    let statement = client
        .prepare("select * from todo_list order by id desc")
        .await
        .unwrap();
    let todos = client
        .query(&statement, &[])
        .await
        .expect("Error getting todo lists")
        .iter()
        .map(|row| row_to_todo(row))
        .collect::<Vec<TodoList>>();

    Ok(todos)
}

```

增加 `handlers.rs` 用于处理服务：

```rust
use crate::db::get_todos;
use actix_web::{web, HttpResponse, Responder};
use deadpool_postgres::{Client, Pool};

pub async fn todos(db_pool: web::Data<Pool>) -> impl Responder {
    let client: Client = db_pool
        .get()
        .await
        .expect("Error connecting to the database");
    let result = get_todos(&client).await;
    match result {
        Ok(todos) => HttpResponse::Ok().json(todos),
        Err(_) => HttpResponse::InternalServerError().into(),
    }
}
```

最后，在 `main.rs` 中创建连接池并添加路由：

```rust
mod db;
mod handlers;
mod models;

use actix_web::{get, web, App, HttpServer, Responder};
use deadpool_postgres;
use handlers::todos;
use std::io;
use tokio_postgres::{self, NoTls};

#[get("/")]
async fn hello() -> impl Responder {
    format!("Hello world!")
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    println!("Starting server at http://127.0.0.1:8000");
    // 创建连接池
    let mut cfg = tokio_postgres::Config::new();
    cfg.host("localhost");
    cfg.port(5432);
    cfg.user("actix");
    cfg.password("actix");
    cfg.dbname("actix");
    let mgr = deadpool_postgres::Manager::new(cfg, NoTls);
    let pool = deadpool_postgres::Pool::new(mgr, 100);
    HttpServer::new(move || {
        App::new()
            .data(pool.clone())
            .service(hello)
            .route("/todos{_:/?}", web::get().to(todos))
    })
    .bind("127.0.0.1:8000")?
    .run()
    .await
}
```

运行并测试：

```shell
$ cargo run

# 另一个总端，jq 用于格式化返回的 json
$ curl 127.0.0.1:8000/todos | jq
[
  {
    "id": 2,
    "title": "List 2"
  },
  {
    "id": 1,
    "title": "List 1"
  }
]
```

## 两个改进

1. 数据库的连接信息硬编码在代码中，在实际使用中会使用环境变量进行设置

添加 `.env` 配置数据库连接信息和服务端口：

```conf
SERVER.HOST=127.0.0.1
SERVER.PORT=8000
PG.USER=actix
PG.PASSWORD=actix
PG.HOST=127.0.0.1
PG.PORT=5432
PG.DBNAME=actix
PG.POOL.MAX_SIZE=30
```

同时，通过环境变量获取对应配置。首先增加 `dotenv` 和 `config` 依赖：

```toml
[dependencies]
# ... 省略
dotenv = "0.15.0"
config = "0.10.1"
```

然后增加 `config.rs`，增加从环境变量中获取配置并生成连接池方法 `from_env`：

```rust
use config::{self, ConfigError};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct ServerConfig {
    pub host: String,
    pub port: i32,
}

#[derive(Deserialize, Debug)]
pub struct Config {
    pub server: ServerConfig,
    pub pg: deadpool_postgres::Config,
}

impl Config {
    pub fn from_env() -> Result<Self, ConfigError> {
        let mut cfg = config::Config::new();
        cfg.merge(config::Environment::new())?;
        cfg.try_into()
    }
}

```

在 `main.rs` 中使用环境变量创建连接池：

```rust
mod config;

use dotenv::dotenv;

// ...省略

#[actix_web::main]
async fn main() -> io::Result<()> {
    // 环境变量
    dotenv().ok();
    // 连接池
    let cfg = crate::config::Config::from_env().unwrap();
    let pool = cfg.pg.create_pool(NoTls).unwrap();
    println!(
        "Starting server at http://{}:{}",
        cfg.server.host, cfg.server.port
    );
    HttpServer::new(move || {
        App::new()
            .data(pool.clone())
            .service(hello)
            .route("/todos{_:/?}", web::get().to(todos))
    })
    .bind(format!("{}:{}", cfg.server.host, cfg.server.port))?
    .run()
    .await
}
```

2. `db.rs` 中 `row_to_todo` 函数太麻烦，使用 `tokio_pg_mapper` 做处理，简化操作：

```toml
[dependencies]
# ... 省略
tokio-pg-mapper = "0.1"
tokio-pg-mapper-derive = "0.1"
```

在 `models.rs` 中添加 `PostgresMapper`，

```rust
use serde::{Deserialize, Serialize};
use tokio_pg_mapper_derive::PostgresMapper;

#[derive(Serialize, Deserialize, PostgresMapper)]
#[pg_mapper(table = "todo_list")]
pub struct TodoList {
    pub id: i32,
    pub title: String,
}

#[derive(Serialize, Deserialize, PostgresMapper)]
#[pg_mapper(table = "todo_item")]
pub struct TodoItem {
    pub id: i32,
    pub title: String,
    pub checked: bool,
    pub list_id: i32,
}
```

使用 `from_row_ref` 方法将记录进行转换：

```rust

use tokio_pg_mapper::FromTokioPostgresRow;

pub async fn get_todos(client: &Client) -> Result<Vec<TodoList>, Error> {
    // ... 省略
    let todos = client
        .query(&statement, &[])
        .await
        .expect("Error getting todo lists")
        .iter()
        // 修改
        .map(|row| TodoList::from_row_ref(row).unwrap())
        .collect::<Vec<TodoList>>();

    Ok(todos)
}

```

## 小结

1. 创建 hello world 程序；
2. 创建数据库连接和获取数据；
3. 使用环境变量；

## 参考文档和项目

1. [Creating a simple TODO service with Actix](https://www.youtube.com/watch?v=gQwA0g0NNSI)
2. [actix-web 官方文档](actix.rs)
3. [actix/example](https://github.com/actix/examples)



> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

---
> from: [**qiwihui**](https://github.com/qiwihui/blog/issues/105#issuecomment-712695653) on: **10/20/2020**

cool
