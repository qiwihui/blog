---
title: "用 Rust Actix-web 写一个 Todo 应用（三）── migrations 和错误处理"
description: "用 Rust Actix-web 写一个 Todo 应用（三）── migrations 和错误处理"
tags: 
- 技术
- Rust
top: 107
date: 24/10/2020, 17:53:14
author: qiwihui
update: 26/10/2020, 15:31:11
categories: 技术
---

## 使用 diesel 管理数据库变化

diesel 是一个用 rust 写的 ORM 库，支持多种数据库，同时 diesel 提供了对数据库结构的管理功能。我们将使用 diesel 对我们的数据库结构变化进行管理。

<!--more-->

首先，安装命令行工具 `diesel_cli`，并初始化数据库设置

```shell
# 安装 diesel_cli，支持 postgres
cargo install diesel_cli --no-default-features --features postgres

# 设置数据库连接
echo DATABASE_URL=postgres://actix:actix@localhost:5432/actix >> .env
# 生成 diesel.toml 文件指向 schema 所在
diesel setup
# 创建数据库 migration
diesel migration generate create_db
```

在生成的 `migrations` 目录中，填入数据库变化的 sql 语句，`up.sql` 用于修改，`down.sql` 用于撤销修改。

`up.sql`：

```sql
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
```

`down.sql`：

```sql
drop table if exists todo_item;
drop table if exists todo_list;
```

由于之前已经有对应的数据表结构，需要将原来的表结构删除，再运行数据库变更：

```shell
# 删除原有的数据表之后
diesel migrations run
```

其中，对应生成的 schema 为：

```rust
table! {
    todo_item (id) {
        id -> Int4,
        title -> Varchar,
        checked -> Bool,
        list_id -> Int4,
    }
}

table! {
    todo_list (id) {
        id -> Int4,
        title -> Varchar,
    }
}

joinable!(todo_item -> todo_list (list_id));

allow_tables_to_appear_in_same_query!(
    todo_item,
    todo_list,
);
```

此时，数据库中的表机构就和我们之前是一样的，同时增加了一个用于记录已经做过的 migrations 的数据库。

## ORM

鉴于 diesel 没有 async 版本，以及 quaint 不是 type-safe，不做 ORM 的支持。

## 错误处理

自定义错误，并将常见的错误统一处理。

新增 `errors.rs`：

```rust
use actix_web::http::StatusCode;
use actix_web::{HttpResponse, ResponseError};
use deadpool_postgres::PoolError;
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug)]
#[allow(dead_code)]
pub enum Error {
    InternalServerError(String),
    NotFound(String),
    PoolError(String),
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ErrorResponse {
    errors: Vec<String>,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self)
    }
}

impl ResponseError for Error {
    fn error_response(&self) -> HttpResponse {
        match self {
            Error::NotFound(message) => {
                HttpResponse::NotFound().json::<ErrorResponse>(message.into())
            }
            _ => HttpResponse::new(StatusCode::INTERNAL_SERVER_ERROR),
        }
    }
}

// 支持 字符串 into
impl From<&String> for ErrorResponse {
    fn from(error: &String) -> Self {
        ErrorResponse {
            errors: vec![error.into()],
        }
    }
}

// 处理 PoolError
impl From<PoolError> for Error {
    fn from(error: PoolError) -> Self {
        Error::PoolError(error.to_string())
    }
}
```

修改 `db.rs`：

```rust
+use crate::errors::Error;

// ...

-        None => Err(Error::new(ErrorKind::NotFound, "Not found")),
+        None => Err(Error::NotFound("Not found".into())),
```

修改 `handlers.rs`，其中一个请求处理

```rust
+use crate::errors::Error;
// error_response：items from traits can only be used if the trait is in scope
+use actix_web::ResponseError;

// ...

-pub async fn todos(state: web::Data<AppState>) -> impl Responder {
+pub async fn todos(state: web::Data<AppState>) -> Result<HttpResponse, Error> {
     let client: Client = state
         .pool
         .get()
@@ -33,12 +34,15 @@ pub async fn todos(state: web::Data<AppState>) -> impl Responder {
         .expect("Error connecting to the database");
     let result = db::get_todos(&client).await;
     match result {
-        Ok(todos) => HttpResponse::Ok().json(todos),
-        Err(_) => HttpResponse::InternalServerError().into(),
+        Ok(todos) => Ok(HttpResponse::Ok().json(todos)),
+        Err(e) => Ok(e.error_response()),
     }
 }
```

## 小结

1. 管理数据库结构变更；
2. 自定义错误处理

## 参考文档和项目

1. [Creating a simple TODO service with Actix](https://www.youtube.com/watch?v=gQwA0g0NNSI)
2. [actix-web 官方文档](actix.rs)
3. [官方 actix-web 示例](https://github.com/actix/examples)


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

