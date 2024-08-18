# 9个值得知道的cURL的用法


对于 HTTP 工程师和 API 设计师来说，使用命令行操作 HTTP 是非常有用的技能。[cURL](http://curl.haxx.se/)
库和 `curl` 命令可以给你设计请求，放入管道并查看相应的能力。`curl` 能力的缺点在于它能覆盖多广的
命令选项。使用 `curl --help` 会展示出150条不同的选项。这篇文章演示了9个基本的，现实程序用到的 `curl` 命令。
<!--more-->

在这篇教程中我们会使用httpkit的 [echo](http://echo.httpkit.com/) 服务做为端点，回显服务的响应
是它收到 HTTP 请求的 JSON 表示。

## 创建请求

我们从最简单的 `curl` 命令开始。

**请求**  

```
curl http://echo.httpkit.com
```

**响应** 

```
{
  "method": "GET",
  "uri": "/",
  "path": {
    "name": "/",
    "query": "",
    "params": {}
  },
  "headers": {
    "host": "echo.httpkit.com",
    "user-agent": "curl/7.24.0 ...",
    "accept": "*/*"
  },
  "body": null,
  "ip": "28.169.144.35",
  "powered-by": "http://httpkit.com",
  "docs": "http://httpkit.com/echo"
}
```

就这样，我们用 `curl` 创建了一个请求，`curl` 使用的 HTTP 动词默认为 `GET`，请求的资源指向的是
 [httpkit](http://httpkit.com/) 的 [echo](http://httpkit.com/echo) 服务：`http://echo.httpkit.com`。

你可以添加路径和查询变量：

**请求**  

```
curl http://echo.httpkit.com//path?query=string
```

**响应** 

```
{ ...
  "uri": "/path?query=string",
  "path": {
    "name": "/path",
    "query": "?query=string",
    "params": {
      "query": "string"
    }
  }, ...
}
```

## 设置请求方法

`curl`默认的请求方法为 `GET` ，可以用 `-X` 参数设置成任何你想要的方法，通常为 `POST`，`PUT`，`DELETE`
方法，甚至是自定义的方法。

**请求**  

```
curl -X POST echo.httpkit.com
```

**响应** 

```
{
    "method": "POST",
    ...
}
```

正如你看到的，`http://` 协议前缀可以不使用，因为这是默认假定的。接着实施 `DELETE` 方法：


**请求**  

```
curl -X DELETE echo.httpkit.com
```

**响应** 

```
{
    "method": "DELETE",
    ...
}
```

## 设置请求头部

请求头部允许客户端给服务器提供诸如授权，内容类型等信息。比如，OAuth2 使用 `Authorization` 头
来传递访问令牌（access tokens）。`curl` 使用 `-H` 选项设置自定义头部。

**请求**  

```
curl -H "Authorization: OAuth 2c4419d1aabeec" \
     http://echo.httpkit.com
```

**响应** 

```
{...
"headers": {
    "host": "echo.httpkit.com",
    "authorization": "OAuth 2c4419d1aabeec",
  ...},
...}
```

可以使用 `-H` 多次来设置多个头部。

**请求**  

```
curl -H "Accept: application/json" \
     -H "Authorization: OAuth 2c3455d1aeffc" \
     http://echo.httpkit.com
```

**响应** 

```
{ ...
  "headers": { ...
    "host": "echo.httpkit.com",
    "accept": "application/json",
    "authorization": "OAuth 2c3455d1aeffc" 
   }, ...
}
```

## 发送请求体

现今许多有名的 HTTP API 使用 `application/json` 和 `application/xml` 来 `POST` 和 `PUT` 资源，
而不是用HTML化的数据。我们试试 `PUT` 一些 JSON 数据到服务器上。

**请求**  

```
curl -X PUT \
     -H 'Content-Type: application/json' \
     -d '{"firstName":"Kris", "lastName":"Jordan"}'
     echo.httpkit.com
```

**响应** 

```
{
   "method": "PUT", ...
   "headers": { ...
     "content-type": "application/json",
     "content-length": "40"
   },
   "body": "{\"firstName\":\"Kris\",\"lastName\":\"Jordan\"}",
   ...
 }
```

## 使用文件作为请求体

将 JSON/XML 写到命令行中是令人头疼的，尤其有时这个文件很大时。幸运的是， `curl` 的 `@readfile` 
可以很容易地读取文件的文本。如果上面例子中的 JSON 保存为文件 `example.json`， 我们可以这么做：

**请求**  

```
curl -X PUT \
     -H 'Content-Type: application/json' \
     -d @example.json
     echo.httpkit.com
```

## 发送 HTML 表单数据

如果不能发送带有数据的请求体，可以设置类似 `POST` 的方法真是没什么用。也许我们可以试试发送 HTML 
表单数据。使用 `-d` 选项，我们可以制定 URL 编码的名称和值。

**请求**  

```
curl -d "firstName=Kris" \
     -d "lastName=Jordan" \
     echo.httpkit.com
```

**响应** 

```
{
  "method": "POST", ...
  "headers": {
    "content-length": "30",
    "content-type":"application/x-www-form-urlencoded"
  },
  "body": "firstName=Kris&lastName=Jordan", ...
}
```

注意到 `POST` 这个方法，即使我们没有指明方法，当 `curl` 看到表单数据时它会指定 `POST` 方法。
可以使用 `-X` 选项来覆盖这个方法。请求的 `Content-Type` 也被自动设置为 `application/x-www-form-urlencoded`，
这样服务器就知道怎么解析数据了。最终，请求体由编码了每一个表单域的 URL 构成。

## 发送 HTML Multipart/file 表单（上传文件）

当涉及到文件上传的表单时，正如你从写上传文件表单时知道的那样，这些使用 `multipart/form-data` 文本类型，
带有 `enctype` 属性。cURL 使用 `-F` 配合上面介绍的 `@readFile` 宏来处理。

**请求**  

```
curl -F "firstName=Kris" \
     -F "publicKey=@idrsa.pub;type=text/plain" \
     echo.httpkit.com
```

**响应** 

```
{
  "method": "POST",
  ...
  "headers": {
    "content-length": "697",
    "content-type": "multipart/form-data;
    boundary=----------------------------488327019409",
    ... },
  "body": "------------------------------488327019409\r\n
           Content-Disposition: form-data;
           name=\"firstName\"\r\n\r\n
           Kris\r\n
           ------------------------------488327019409\r\n
           Content-Disposition: form-data;
           name=\"publicKey\";
           filename=\"id_rsa.pub\"\r\n
           Content-Type: text/plain\r\n\r\n
           ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAkq1lZYUOJH2
           ... more [a-zA-Z0-9]* ...
           naZXJw== krisjordan@gmail.com\n\r\n
           ------------------------------488327019409
           --\r\n",
...}
```

像 `-d` 选项一样，当使用 `-d` 选项时 `curl` 会自动地默认使用 `POST` 方法，`multipart/form-data` 文件
类型头部，计算长度并组成请求体。请注意 `@readFile`  宏是怎样读取一个文件的文本为任何字符的，这个不是
一个单独的操作，`;text/plain` 指定了文件的 MIME 文本类型。在未指定的情况下，`curl` 会尝试嗅探文本类型。

## 测试虚拟主机，不使用 DNS

通常，在不修改 DNS 覆盖主机的情况下测试一个虚拟主机或者是缓存代理时很有用的。只需使用 cURL 将请求指向
主机的 IP 地址 并覆写 `Host` 头。

**请求**  

```
curl -H "Host: google.com" 50.112.251.120
```

**响应** 

```
{
  "method": "GET", ...
  "headers": {
    "host": "google.com", ...
  }, ...
}
```

## 查看响应头部

API 正越来越多的利用响应头部来提供授权，速率限制，缓存等方面的信息。cURL 使用 `-i` 选项来查看响应头部
和响应体。

**请求**  

```
curl -i echo.httpkit.com 
```

**响应** 

```
HTTP/1.1 200 OK
Server: nginx/1.1.19
Date: Wed, 29 Aug 2012 04:18:19 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 391
Connection: keep-alive
X-Powered-By: http://httpkit.com

{
  "method": "GET",
  "uri": "/", ...
}
```

原文：[9 uses for cURL worth knowing](http://httpkit.com/resources/HTTP-from-the-Command-Line/)


[View on GitHub](https://github.com/qiwihui/blog/issues/19)


