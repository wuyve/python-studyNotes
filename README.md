# Flask目录

Flask默认使用static目录存放静态资源，templates目录存放模板，也可以通过设置参数更改：

```python
app = Flask("myapp", static_folder = "path1", template_folder = "path2")
```

以上指定静态资源目录为path1， 模板目录为path2。

# 调试模式

开启调试模式：

```python
app.run(debug=Ture)
```

或下面这种途径

```python
app.debug = True
app.run()
```

开启调试模式后，程序启动后，会自动检测源码是否发生变化，若有编码则自动重启程序。

# bangdingIP和端口

默认情况下，Flask绑定Ip为127.0.0.1，端口为5000.也可以通过下面的方式自定义：

```python
app.run(host='0.0.0.0', port='8080', debug=True)
```

`0.0.0.0`代表电脑的所有Ip。以上为绑定了8080端口。启动服务后访问http://127.0.0.1:8080/

# 获取URL参数

## 列出所有的url参数

在`server.py`中添加以下内容：

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return request.args.__str__()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

然后在浏览器中访问http://127.0.0.1:5000/?name=wuyve&age=18&school=hdu

将显示：ImmutableMultiDict([('name', 'wuyve'), ('age', '18'), ('school', 'hdu')])

较新的浏览器也支持直接在url中输入中文（最新的火狐浏览器内部会帮忙将中文转换成符合URL规范的数据）

## request.full_path和request.path

可以通过request.full_path和request.path查看浏览器传给Flask服务的数据

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    print(request.path)
    print(request.full_path)
    return request.args.__str__()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

然后在浏览器中输入：http://127.0.0.1:5000/?word=你好

可以看到控制台信息

`/`

`/?word=%E4%BD%A0%E5%A5%BD`

## 获取指定的参数值

例如，获取info对应的值

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    # 获取参数中age键的键值
    return request.args.get('age')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行程序之后，在浏览器中输入http://127.0.0.1:5000/?name=wuyve&age=18&school=hdu

则显示`18`

## debug模式下容易出现的异常

1. Flask不允许返回None，若没有在URL参数中找到指定的键，则会报错。

    解决方法：

    1. 先判断它是不是None

    ```python
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        r = request.args.get('info')
        if r == None:
            # do something
            return ''
        return r

    if __name__ == '__main__':
        app.run(port=5000, debug=True)
    ```

    2. 也可以设置默认值，在取不到数据时用这个值：

    ```python
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        r = request.args.get('info', 'welcome')
        return r

    if __name__ == '__main__':
        app.run(port=5000, debug=True)
    ```

## getlist处理多值

如果请求参数中有几个一样的键，可以使用getlist获取所有的app的值

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    r = request.args.getlist('info')
    return str(r)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行软件后在浏览器中输入http://127.0.0.1:5000/?name=wuyve&info=18&school=hdu&info=ppp

页面显示['18', 'ppp']

# 获取POST数据

POST用于向定向的资源提交要被处理的数据。

比如：在网站上注册用户、写文章等的时候，需要将数据传送到网站服务器中。并不适合将数据放到URL参数中，密码放到URL参数中容易被看到，文章数据又太多，浏览器不一定支持太长长度的URL。这时一般使用POST方法。

使用python的requests库模拟浏览器：

安装方法： `pip install requests`

## 获取POST方法传送的数据

以用户注册为例，向服务器/register传送用户名name和密码password。

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    print(request.stream.read())
    return 'welcome'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

`@app.route('/register', methods=['POST'])`是指url`/register`只接受POST方法（可根据需要修改methods参数，如果想让它同时支持GET和POST，可以这样写`@app.route('/register', methods=['GET', 'POST'])`

浏览器模拟工具client.py内容如下：

```python
import requests

user_info = {
    'name': 'wuyve',
    'password': 'wuyve123'
}

r = requests.post('http://127.0.0.1:5000/register', data=user_info)

print(r.text)
```

运行server.py与client.py。则client.py将输出：`welcom`

server.py输出

`Host: 127.0.0.1:5000`

`User-Agent: python-requests/2.23.0`

`Accept-Encoding: gzip, deflate`

`Accept: */*`

`Connection: keep-alive`

`Content-Length: 28`

`Content-Type: application/x-www-form-urlencoded`

`b'name=wuyve&password=wuyve123'`

前6行驶HTTP请求头，由`print(requests.headers)`输出

随后一行是请求体的数据，是由`print(request.stream.read())`输出

## 解析POST数据