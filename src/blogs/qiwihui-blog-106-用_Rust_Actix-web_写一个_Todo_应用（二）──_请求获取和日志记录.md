# 用 Rust Actix-web 写一个 Todo 应用（二）── 请求获取和日志记录


## 如何获取路径参数

添加根据 id 获取数据操作：

```rust
use std::io::{Error, ErrorKind};
// ...省略

pub async fn get_todo(client: &Client, list_id: i32) -> Result<TodoList, Error> {
    let statement = client
        .prepare("select * from todo_list where id = $1")
        .await
        .unwrap();

    let may_todo = client
        .query_opt(&statement, &[&list_id])
        .await
        .expect("Error getting todo lists")
        .map(|row| TodoList::from_row_ref(&row).unwrap());

    match may_todo {
        Some(todo) => Ok(todo),
        None => Err(Error::new(ErrorKind::NotFound, "Not found")),
    }
}
```

设置请求参数，设置使用 `Info` 作为请求路径参数序列化结构体：

```rust
use crate::db::{get_todo, get_todos};
use serde::Deserialize;

// ...省略

#[derive(Deserialize)]
pub struct Info {
    pub list_id: i32,
}

pub async fn todo(info: web::Path<Info>, db_pool: web::Data<Pool>) -> impl Responder {
    let client: Client = db_pool
        .get()
        .await
        .expect("Error connecting to the database");

    let result = get_todo(&client, info.list_id).await;
    match result {
        Ok(todo) => HttpResponse::Ok().json(todo),
        Err(_) => HttpResponse::InternalServerError().into(),
    }
}
```

添加路由：

```rust
use handlers::{todo, todos};

// ...省略
    HttpServer::new(move || {
        App::new()
            .data(pool.clone())
            .service(hello)
            .route("/todos{_:/?}", web::get().to(todos))
            .route("/todos/{list_id}{_:/?}", web::get().to(todo))
    })

```

运行并获取结果：

```shell
$ curl 127.0.0.1:8000/todos/1
{"id":1,"title":"List 1"}
```

## 增加日志记录

为了方便查看操作过程，可以增加日志记录，使用 `env_logger` 方便从环境变量中设置日志记录级别，`log` 用于记录不同级别日志，比如 `info`，`debug`。

`Cargo.toml`：

```toml
[dependencies]
# ...
env_logger = "0.8"
log="0.4"
```

在 `.env` 中可以手动设置日志记录级别，比如

```env
RUST_LOG=info
```

`main.rs`：

```rust
use actix_web::{get, middleware, web, App, HttpServer, Responder};

use env_logger;
use log::info;

// ...

 async fn main() -> io::Result<()> {
     dotenv().ok();
+    if std::env::var("RUST_LOG").is_err() {
+        std::env::set_var("RUST_LOG", "actix_web=info");
+    }
+    env_logger::init();
     let cfg = crate::config::Config::from_env().unwrap();
     let pool = cfg.pg.create_pool(NoTls).unwrap();
+    info!(
         "Starting server at http://{}:{}",
         cfg.server.host, cfg.server.port
     );
     HttpServer::new(move || {
         App::new()
             .data(pool.clone())
+            .wrap(middleware::Logger::default())
// ...

```

运行以查看日志

```shell
$ cargo run
   Compiling todo-list v0.1.0 (/Users/qiwihui/rust/todo-list)
    Finished dev [unoptimized + debuginfo] target(s) in 1m 19s
     Running `target/debug/todo-list`
[2020-10-23T06:43:18Z INFO  todo_list] Starting server at http://127.0.0.1:8000
[2020-10-23T06:43:18Z INFO  actix_server::builder] Starting 4 workers
[2020-10-23T06:43:18Z INFO  actix_server::builder] Starting "actix-web-service-127.0.0.1:8000" service on 127.0.0.1:8000
[2020-10-23T06:45:04Z INFO  actix_web::middleware::logger] 127.0.0.1:63751 "GET /todos HTTP/1.1" 200 79 "" "curl/7.64.1" 0.016465
```

## 如何获取请求体

首先，我们增加插入数据操作，sql 语句中的 `returning id, title` 用于返回插入成功的数据

`db.rs`：

```rust
pub async fn create_todo(client: &Client, title: String) -> Result<TodoList, Error> {
    let statement = client
        .prepare("insert into todo_list (title) values ($1) returning id, title")
        .await
        .unwrap();

    client
        .query(&statement, &[&title])
        .await
        .expect("Error creating todo list")
        .iter()
        .map(|row| TodoList::from_row_ref(row).unwrap())
        .collect::<Vec<TodoList>>()
        .pop()
        .ok_or(Error::new(ErrorKind::Other, "Error creating todo list"))
}
```

增加请求处理，`CreateTodoList` 用于序列化请求的数据：

`handles.rs`

```rust

#[derive(Deserialize)]
pub struct CreateTodoList {
    pub title: String,
}

pub async fn create_todo(
    info: web::Json<CreateTodoList>,
    state: web::Data<AppState>,
) -> impl Responder {
    let client: Client = state
        .pool
        .get()
        .await
        .expect("Error connecting to the database");
    let result = db::create_todo(&client, info.0.title.clone()).await;
    match result {
        Ok(todo) => HttpResponse::Ok().json(todo),
        Err(_) => HttpResponse::InternalServerError().into(),
    }
}
```

其中，`state: web::Data<AppState>` 将 原来的 pool 做了简单的封装，好处在于可以传入多个数据作为 `web::Data`。

```rust
// .. 省略
pub struct AppState {
    pub pool: Pool,
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    // .. 省略
    HttpServer::new(move || {
        App::new()
            .data(AppState { pool: pool.clone() })
```

同时添加路由：

```rust
  App::new()
    // 省略
    .route("/todos{_:/?}", web::post().to(handlers::create_todo))
```

完成后运行 `cargo run`，在使用 curl 进行请求时，注意添加 `-H "Content-Type: application/json"` 头部信息，否则无法处理。

```shell
$ curl -X POST 127.0.0.1:8000/todos -d '{"title": "list 3"}' -H "Content-Type: application/json"
{"id":3,"title":"list 3"}
```

## 其他操作

继续添加其他操作，如获取创建单个项，以及完成项目（`check_todo`）

```rust
pub async fn get_items(client: &Client, list_id: i32) -> Result<Vec<TodoItem>, Error> {
    // ...
}

pub async fn get_item(client: &Client, list_id: i32, item_id: i32) -> Result<TodoItem, Error> {
    // ...
}

pub async fn create_item(client: &Client, list_id: i32, title: String) -> Result<TodoItem, Error> {
    // ...
}

pub async fn check_todo(client: &Client, list_id: i32, item_id: i32) -> Result<bool, Error> {
    // ...
}
```

以及对应的路由和请求处理：

```rust
  .route("/todos/{list_id}/items{_:/?}", web::get().to(handlers::items))
  .route("/todos/{list_id}/items{_:/?}", web::post().to(handlers::create_item))
  .route("/todos/{list_id}/items/{item_id}{_:/?}", web::get().to(handlers::get_item))
  .route("/todos/{list_id}/items/{item_id}{_:/?}", web::put().to(handlers::check_todo))
```

```rust

pub async fn items(info: web::Path<GetTodoList>, state: web::Data<AppState>) -> impl Responder {
    // ...
}
pub async fn create_item(
    todo: web::Path<GetTodoList>,
    info: web::Json<CreateTodoItem>,
    state: web::Data<AppState>,
) -> impl Responder {
    // ...
}

pub async fn get_item(info: web::Path<GetTodoItem>, state: web::Data<AppState>) -> impl Responder {
    // ...
}
pub async fn check_todo(
    info: web::Path<GetTodoItem>,
    state: web::Data<AppState>,
) -> impl Responder {
    // ...
}

```

## 小结

1. 获取路径参数
2. 获取请求体
3. 设置日志记录

## 参考文档和项目

1. [Creating a simple TODO service with Actix](https://www.youtube.com/watch?v=gQwA0g0NNSI)
2. [actix-web 官方文档](actix.rs)
3. [官方 actix-web 示例](https://github.com/actix/examples)


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/106)


