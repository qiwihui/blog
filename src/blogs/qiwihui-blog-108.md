# 用 Rust Actix-web 写一个 Todo 应用（四）── 测试


对程序进行集成测试。

<!--more-->

## 测试前重构

在测试前，先简单重构，方便构建测试。

### 1. 将路由抽取成单独的模块

`routes.rs`

```rust
use crate::handlers;
use actix_web::web;
pub fn routes(cfg: &mut web::ServiceConfig) {
    cfg.service(handlers::hello)
        .route("/todos{_:/?}", web::get().to(handlers::todos))
        .route("/todos{_:/?}", web::post().to(handlers::create_todo))
        .route("/todos/{list_id}{_:/?}", web::get().to(handlers::todo))
        .route(
            "/todos/{list_id}/items{_:/?}",
            web::get().to(handlers::items),
        )
        .route(
            "/todos/{list_id}/items{_:/?}",
            web::post().to(handlers::create_item),
        )
        .route(
            "/todos/{list_id}/items/{item_id}{_:/?}",
            web::get().to(handlers::get_item),
        )
        .route(
            "/todos/{list_id}/items/{item_id}{_:/?}",
            web::put().to(handlers::check_todo),
        );
}
```

并将原来的 `hello` 视图移至 `handlers.rs` 中，此时 `main.rs` 中路由修改为如下：

```rust
+mod routes;
// ... 省略
+use routes::routes;
 
// ... 转移
-#[get("/")]
-async fn hello() -> impl Responder {
-    format!("Hello world!")
-}
-
 #[actix_web::main]
 async fn main() -> io::Result<()> {
     dotenv().ok();
@@ -34,26 +31,7 @@ async fn main() -> io::Result<()> {
         App::new()
             .data(AppState { pool: pool.clone() })
             .wrap(middleware::Logger::default())
// ... 转移
-            .service(hello)
-            .route("/todos{_:/?}", web::get().to(handlers::todos))
-            .route("/todos{_:/?}", web::post().to(handlers::create_todo))
-            .route("/todos/{list_id}{_:/?}", web::get().to(handlers::todo))
-            .route(
-                "/todos/{list_id}/items{_:/?}",
-                web::get().to(handlers::items),
-            )
-            .route(
-                "/todos/{list_id}/items{_:/?}",
-                web::post().to(handlers::create_item),
-            )
-            .route(
-                "/todos/{list_id}/items/{item_id}{_:/?}",
-                web::get().to(handlers::get_item),
-            )
-            .route(
-                "/todos/{list_id}/items/{item_id}{_:/?}",
-                web::put().to(handlers::check_todo),
-            )
+            .configure(routes)
     })
     .bind(format!("{}:{}", cfg.server.host, cfg.server.port))?
     .run()
```

### 2. 增加 `init_pool` 方法

首先我们添加一个配置错误处理：

`errors.rs`：

```rust
@@ -10,6 +12,7 @@ pub enum Error {
     InternalServerError(String),
     NotFound(String),
     PoolError(String),
+    ConfigError(String),
 }
```

在 `config.rs` 中增加 `init_pool` 方法：

```rust
use crate::errors::Error;
use deadpool_postgres::Pool;
use tokio_postgres::NoTls;

// ... 省略

pub fn init_pool(config: &Config) -> Result<Pool, Error> {
    match config.pg.create_pool(NoTls) {
        Ok(pool) => Ok(pool),
        Err(_) => Err(Error::ConfigError("config error".into())),
    }
}
```

## 测试

首先，增加运行时环境包:

```toml
# ...

[dependencies]
actix-rt = "1"
```

创建 `tests` 目录，并添加如下文件，

```shell
src/tests/
├── handlers.rs
├── helpers.rs
└── mod.rs
```

在 main.rs 中增加 `tests` 模块：

```rust
#[cfg(test)]
mod tests;

// ...
```

其中，`handlers.rs` 用于集成测试，`helpers.rs` 提供基本的测试方法。

`mod.rs`：

```rust
mod handlers;
mod helpers;
```

我们先测试一下 `/` 路由下 `hello world` 的功能。

`helpers.rs` 中增加基本的 `get` 测试方法：

```rust
use crate::routes::routes;
use actix_web::dev::ServiceResponse;
use actix_web::{test, App};
// 测试get
pub async fn test_get(route: &str) -> ServiceResponse {
    let mut app = test::init_service(App::new().configure(routes)).await;
    test::call_service(&mut app, test::TestRequest::get().uri(route).to_request()).await
}
// assert get 方法
pub async fn assert_get(route: &str) -> ServiceResponse {
    let response = test_get(route).await;
    assert!(response.status().is_success());
    response
}
```

`handlers.rs`：

```rust
use crate::tests::helpers::assert_get;

#[actix_rt::test]
async fn test_hello_world() {
    assert_get("/").await;
}
```

运行测试：

```shell
$ cargo test

running 1 test
test tests::handlers::tests::test_hello_world ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

可以看到这个测试成功了。

## 测试 `POST` 接口

我们增加 `lazy_static` 和 `serde_json` 库，前者用于延后执行，后者用于方便处理 json 数据。

```toml
# ...

[dev-dependencies]
lazy_static = "1.4.0"
serde_json = "1.0.48"
```

在集成测试中，我们将使用数据库链接进行测试，首先 `helpers.rs` 中增加 `AppState` 用于测试：

```rust
lazy_static! {
    pub static ref APP_STATE: models::AppState = {
        dotenv().ok();
        let config = Config::from_env().unwrap();
        let pool = init_pool(&config).unwrap();
        models::AppState { pool: pool.clone() }
    };
}
```

以及对应的 post 测试断言：

```rust
// 其中 `AppState` 需要增加 `Clone` 宏
pub async fn test_post<T: Serialize>(route: &str, params: T) -> ServiceResponse {
    let mut app = test::init_service(App::new().data(APP_STATE.clone()).configure(routes)).await;
    test::call_service(
        &mut app,
        test::TestRequest::post()
            .set_json(&params)
            .uri(route)
            .to_request(),
    )
    .await
}

pub async fn assert_post<T: Serialize>(route: &str, params: T) -> ServiceResponse {
    let response = test_post(route, params).await;
    assert!(response.status().is_success());
    response
}
```

然后，我们增加一个创建 todo_list 的测试，包含创建并检测是否存在：

`tests/handlers.rs`：

```rust
#[actix_rt::test]
async fn test_create_todos() {
    let todo_title = "Create todo List";

    let params = CreateTodoList {
        title: todo_title.into(),
    };
    let response = assert_post("/todos", params).await;
    // 检查放返回数据
    let body = test::read_body(response).await;
    let try_created: Result<models::TodoList, serde_json::error::Error> =
        serde_json::from_slice(&body);
    assert!(try_created.is_ok(), "Response couldn't not be parsed");
    // 使用接口查看数据
    let created_list = try_created.unwrap();
    let resp = assert_get("/todos").await;
    let todos: Vec<models::TodoList> = test::read_body_json(resp).await;
    let maybe_list = todos.iter().find(|todo| todo.id == created_list.id);
    assert!(maybe_list.is_some(), "Item not found!");
}
```

其中 `CreateTodoList` 需要增加 `Clone` 宏，才能在传入 `params` 参数时正常使用。

运行测试，查看结果

```shell
$ cargo test

running 2 tests
test tests::handlers::test_hello_world ... ok
test tests::handlers::test_create_todos ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

## 测试 `GET` 接口

最后添加 `GET` 集成测试：

```rust
use crate::db::create_todo;
use crate::tests::helpers::{assert_get, assert_post, APP_STATE};
use deadpool_postgres::Client;
// ...

#[actix_rt::test]
async fn test_get_todos() {
    // create data in db
    let todo_title = "New Todo List";
    let client: Client = APP_STATE
        .pool
        .get()
        .await
        .expect("Error connecting to the database");
    let new_todo = create_todo(&client, todo_title.into()).await;
    assert!(new_todo.is_ok(), "Failed to create new test todo");
    // get and check
    let new_todo = new_todo.unwrap();
    let response = assert_get("/todos").await;
    let todos: Vec<models::TodoList> = test::read_body_json(response).await;
    let maybe_list = todos.iter().find(|todo| todo.id == new_todo.id);
    assert!(maybe_list.is_some(), "Item not found!");
}
```

运行结果：

```rust
$ cargo test

running 3 tests
test tests::handlers::test_hello_world ... ok
test tests::handlers::test_get_todos ... ok
test tests::handlers::test_create_todos ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

## 小结

1. 简单重构，抽象工具函数；
2. 抽象测试工具函数；
3. 创建 `GET` 和 `POST` 测试。

## 参考文档和项目

1. [Creating a simple TODO service with Actix](https://www.youtube.com/watch?v=gQwA0g0NNSI)
2. [actix-web 官方文档](actix.rs)
3. [官方 actix-web 示例](https://github.com/actix/examples)


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/108)


