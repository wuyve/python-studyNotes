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
    print(request.st
    ream.read())
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

Flask的内置的解析器request.from，可以把post参数中的键值取出来。

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    # print(request.stream.read()) # 不要用，否则下面的form取不到数据
    print(request.form)
    print(request.form['name'])
    print(request.form.get('name'))
    print(request.form.getlist('name'))
    print(request.form.get('nickname', default='little apple'))
    return 'welcome'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行server.py与client.py后，server.py控制台输出：

`Host: 127.0.0.1:5000`

`User-Agent: python-requests/2.23.0`

`Accept-Encoding: gzip, deflate`

`Accept: */*`

`Connection: keep-alive`

`Content-Length: 28`

`Content-Type: application/x-www-form-urlencoded`


`ImmutableMultiDict([('name', 'wuyve'), ('password', 'wuyve123')])`

`wuyve`

`wuyve`

`['wuyve']`

`little apple`

## 获取POST中的列表数据

若name有多个值，可以使用request.form.getlist('name'),该方法将返回一个列表。

修改client.py如下：

```python
import requests

user_info = {
    'name': ['wuyve', 'wuyve123', 'wu_yve'],
    'password': 'wuyve123'
}

r = requests.post('http://127.0.0.1:5000/register', data=user_info)

print(r.text)
```

运行之后，server.py控制台将输出：

`ImmutableMultiDict([('name', 'wuyve'), ('name', 'wuyve123'), ('name', 'wu_yve'), ('password', 'wuyve123')])`

`wuyve`

`wuyve`

`['wuyve', 'wuyve123', 'wu_yve']`

`little apple`


# 处理和相应JSON数据

## 处理和相应JSON数据

使用HTTP POST方法传到网站服务器的数据格式有很多种，可以是通过&符号分割的键值对格式，也可以使用JSON格式、XML格式。相比XML的重量、规范繁琐，JSON显得非常小巧和易用。

如果POST数据是JSON格式，request.json会自动将json数据转换为python类型（字典或列表）。

server.py:

```python
from flask import Flask, request

app = Flask("myapp")

@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json['n1'] + request.json['n2']
    return str(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

client.py:

```
import requests

json_data = {'n1': 5, 'n2': 3}

r = requests.post('http://127.0.0.1:5000/add', json=json_data)

print(r.text)
```

运行后，server.py控制台输出：

`Host: 127.0.0.1:5000`

`User-Agent: python-requests/2.23.0`

`Accept-Encoding: gzip, deflate`

`Accept: */*`

`Connection: keep-alive`

`Content-Length: 18`

`Content-Type: application/json`


`<class 'dict'>`

`{'n1': 5, 'n2': 3}`

注意，请求头中`Content-Type`的值是`application/json`

## 响应JSON

相应JSON时，除了要把响应体改成JSON格式，响应头的Content-Type也要设置为application/json。

server.py:

```python
from flask import Flask, request, Response
import json

app = Flask("myapp")

@app.route('/add', methods=['POST'])
def add():
    result = {'sum': request.json['n1'] + request.json['n2']}
    return Response(json.dumps(result), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

client.py:

```python
import requests

json_data = {'n1': 5, 'n2': 3}

r = requests.post('http://127.0.0.1:5000/add', json=json_data)

print(r.headers)
print(r.text)
```

运行之后，client.py控制台输出：

`{'Content-Type': 'application/json', 'Content-Length': '10', 'Server': 'Werkzeug/1.0.1 Python/3.7.7', 'Date': 'Tue, 21 Apr 2020 06:36:13 GMT'}`

`{"sum": 8}`

如果需要服务器的HTTP响应头具有更好的可定制性，比如自定义server，可以修改add()函数：

```python
@app.route('/add', methods=['POST'])
def add():
    result = {'sum': request.json['n1'] + request.json['n2']}
    resp = Response(json.dumps(result), mimetype='application/json')
    resp.headers.add('Server', 'python flask')
    return resp
```

运行之后，client.py控制台输出：

`{'Content-Type': 'application/json', 'Content-Length': '10', 'Server': 'python flask', 'Date': 'Tue, 21 Apr 2020 06:40:39 GMT'}`

`{"sum": 8}`

### 使用jsonify工具函数

使用jsonify工具函数

server.py:

```python
from flask import Flask, request, jsonify
import json

app = Flask("myapp")

@app.route('/add', methods=['POST'])
def add():
    result = {'sum': request.json['n1'] + request.json['n2']}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

client.py:

```python
import requests

json_data = {'n1': 5, 'n2': 3}

r = requests.post('http://127.0.0.1:5000/add', json=json_data)

print(r.headers)
print(r.text)
```

运行之后，client.py控制台输出：

`{'Content-Type': 'application/json', 'Content-Length': '15', 'Server': 'Werkzeug/1.0.1 Python/3.7.7', 'Date': 'Tue, 21 Apr 2020 06:44:47 GMT'}`

```
{
  "sum": 8
}
```

# 上传文件

使用Flask处理文件上传很简单，只需要在HTML表单中设置enctype="multipart/form-data"属性，浏览器才会发送文件。

已上传的文件存储在内存或是文件系统中一个临时的位置。可以通过请求对象的files属性访问它们。美分上传的文件都会存储在字典中。它表现近乎为一个标准的python file对象，但它还有一个save()方法，这个方法允许把文件保存到服务器的文件系统上。

以上传图片为例：假设将上传的图片只允许'png'、'jpg'、'jpeg'、'gif'这四种格式，通过url/upload使用POST上传，上传的图片存放在服务器端的static/uploads目录下。

首先在项目中创建目录static/uploads。

然后安装werkzeug库，可以判断文件名是否安全： `pip install werkzeug`

server.py:

```python
from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 文件上传目录
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# 支持的文件格式
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} # 集合类型

# 判断文件名是否是我们支持的格式
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1) [1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['image']
    
    if upload_file and allowed_file(upload_file.filename): # 上传前文件在客户端的文件名
        filename = secure_filename(upload_file.filename)
        # 将文件保存到 static/uploads 目录，文件名同上传时使用的文件名
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        return 'info is' + request.form.get('info', '') + '. success'
    else:
        return 'failed'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

app.config中的config是字典的子类，可以用来设置自有的配置信息，也可以设置自己的配置信息。

函数allowed_file(filename)用来判断filename是否有后缀以及后缀是否在app.config['ALLOWED_EXTENSIONS']中。

upload_file是上传文件对应的对象。

app.root_path获取server.py所在目录在文件系统中的绝对路径。

upload_file.save(path)用来将upload_file保存在服务器的文件系统中，参数最好是绝对路径。函数os.path.join()用来将使用合适的路径分隔符将路径组合起来。


client.py:

```python
import requests

file_data = {'image': open('flask.png', 'rb')}
user_info = {'info': 'flask'}

r = requests.post('http://127.0.0.1:5000/upload', data=user_info, files=file_data)

print(r.text)
```

要控制上传文件的大小，可以设置请求实体的大小，例如：
`app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 *  1024 # 16MB`

在上传文件的时候，需要使用try:...except:...

如果要获取上传文件的如容可以：
`file_content = request.files['image'].stream.read()`

# Restful URL

## Restful URL - 变量规则

Restful URL可以看作是对URL参数的替代。

server.py

```python:
from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def user(username):
    print(username)
    print(type(username))
    return 'hello ' + username

@app.route('/user/<username>/friends')
def user_friends(username):
    print(username)
    print(type(username))
    return 'In user_frinends get username: ' + username

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行server.py，之后在浏览器中输出http://127.0.0.1:5000/user/wuyve, server.py将输出hello wuyve。

访问http://127.0.0.1:5000/user/wuyve/， 则会报错：

`Not Found`

`The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.`

访问http://127.0.0.1:5000/user/wuyve/friends，将输出`In user_frinends get username: wuyve`

## 转换类型

使用Restful URL得到的变量默认为str对象。可以使用flask内置的转换机制，即在route中指定转换类型

server.py:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/page/<int:num>')
def page(num):
    print(num)
    print(type(num))
    return 'hello world'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行server.py，在浏览器中输入http://127.0.0.1:5000/page/2，server.py控制台输出：`2 <class 'int'>`

如果访问的是http://127.0.0.1:5000/page/wuyve，则会得到404相应。

**有3个默认的转换器：**

int 接受整数

float 同int， 但是接受浮点数

path 和默认的相似，但也接受斜线

## 编写转换器

自定义的转换器是一个继承werkzeug.routing.BaseConverter的类，修改to_python和to_url方法即可。

to_python方法用于将url中变量转换后供被@app.route包装的函数使用，to_url方法用于flask.url_for中的参数转换。

server.py:

```python
from flask import Flask, url_for
from werkzeug.routing import BaseConverter
 
class MyIntConverter(BaseConverter):
 
    def __init__(self, url_map):
        super(MyIntConverter, self).__init__(url_map)
 
    def to_python(self, value):
        return int(value)
 
    def to_url(self, value):
        return value * 2
 
 
app = Flask(__name__)
app.url_map.converters['my_int'] = MyIntConverter
 
@app.route('/page/<my_int:num>')
def page(num):
    print(num)
    print(url_for('page', num='145'))   # page 对应的是 page函数 ，num 对应对应`/page/<my_int:num>`中的num，必须是str
    return 'hello world'
 
if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行后，访问http://127.0.0.1:5000/page/28后，server.py的输出信息：

`28`

`/page/145145`

# 使用url_for生成链接

工具函数url_for可以以编码的形式生成url，提供开发效率

server.py

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():
    pass

@app.route('/user/<name>')
def user(name):
    pass

@app.route('/page/<int:num>')
def page(num):
    pass

@app.route('/test')
def test():
    print(url_for('test'))
    print(url_for('user', name='wuyve'))
    print(url_for('page', num=1, q='welcome to mypage 15%2'))
    print(url_for('static', filename='uploads/flask.png'))
    return 'Hello'


if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行server.py，访问http://127.0.0.1:5000/test，控制台将会输出：

`/test`

`/user/wuyve`

`/page/1?q=welcome+to+mypage+15%252`

`/static/uploads/flask.png`

**构建URL而非在模板中硬编码的三个有点**

1. 反向构建通常比硬编码的描述性更好。更重要的是，它允许一次性修改URL，而不是到处边找边改。
2. URL构建会转义特殊字符和Unicode数据，免去很多麻烦。
3. 如果应用不位于URL的根路径，url_for()会妥善处理这个问题

# 使用redirect重定向网址

运行server.py，在浏览器中访问http://127.0.0.1:5000/old，浏览器的url就会变成http://127.0.0.1:5000/new，并显示：redirect函数用于重定向。

实现机制很简单，向客户端（浏览器）发送一个重定向的HTTP报文，浏览器就会去访问报文里指定的url。

使用redirect时，给它一个字符串类型的惨啊书就行了。

server.py:

```python
from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route('/old')
def old():
    print('this is old')
    return redirect(url_for('new'))

@app.route('/new')
def new():
    print('this is new')
    return 'this is new'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行server.py，访问http://127.0.0.1:5000/old, 浏览器的url就会变成http://127.0.0.1:5000/new

# Jinja2

jinja2是Flask作者开发的一个模板系统，起初是仿django模板的一个模板引擎，为Flask提供模板支持，由于其领过，快速和安全等优点被广泛使用。

## 优点

1. 相对于Template，jinja2更加灵活，它提供了控制结构，表达式和继承等。
2. 相对于Mako，jinja2仅有控制结构，不允许在模板中编写太多的业务逻辑。
3. 相对于Django模板，jinja2性能更好。
4. jinja2模板的可读性很棒。

## jinja2语法

作为一个模板系统，它还提供了特殊的语法，按照它支持的语法进行编写后，就能使用jinja2模板进行渲染。基本语法在jinja2中，存在三种语法：

1. 控制结构 {% %}
2. 变量取值 {{}}
3. 注释 {# #}

例如：

{# This is jinja code #}

{% for file in filenames %}

...

{% endfor %}


可以看到，for循环的使用方式和python比较类似，但是没有了句尾的冒号，另外需要使用endfor作为最后结尾。if也如此。

## jinja2变量

jinja2模板中使用{{}}语法表示一个变量，它是一种特殊的占位符。

当利用jinja2进行渲染的时候，它会把这些特殊的占位符进行填充/替换，jinja2支持python中所有的python数据类型比如列表、元组、对象等。




(暂时跳过模板引擎)



# 自定义404等错误的响应

## 自定义404等相应

要处理HTTP错误，可以使用flask.abort函数

server.py:

```python
from flask import Flask, render_template_string, abort

app = Flask(__name__)

@app.route('/user')
def user():
    abort(401) # Unauthorized 未授权
    print('Unauthorized, 请先登录')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

运行之后，访问http://127.0.0.1:5000/user， 则会出现Unauthorized错误。

注意：*server.py中abort(401)后的print并没有执行*

## 自定义错误页面

server.py:

```python
from flask import Flask, render_template_string, abort

app = Flask(__name__)

@app.route('/user')
def user():
    abort(401) # Unauthorized 未授权

@app.errorhandler(401)
def page_unauthorized(error):
    return render_template_string('<h1>Unauthorized </h1><h2>{{ error_info }}</h2>', error_info=error), 401

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

page_unauthorized 函数返回的是一个元组，401 代表HTTP 响应状态码。

如果省略401，则响应状态码会变成默认的 200。
运行server.py，访问http://127.0.0.1:5000/user，就可以看见401错误。

# 用户会话

session用来记录用户的登陆状态，一般基于cookie实现

server.py:

```python
from flask import Flask, render_template_string, session, request, redirect, url_for

app = Flask(__name__)

app.secret_key = 'LoenDSdtj\9bX#%@!!*(0&^%)'

@app.route('/login')
def login():
    page = '''
    <form action="{{url_for('do_login')}}" method="post">
        <p>name: <input type="text" name="user_name" /> </p>
        <input type="submit" value="submit" />
    </form>
    '''
    return render_template_string(page)

@app.route('/do_login', methods=['POST'])
def do_login():
    name = request.form.get('user_name')
    session['user_name'] = name
    return 'success'

@app.route('/show')
def show():
    return session['user_name']

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)

```

代码含义：

app.secret_key用于给session加密

在/login中将向用户展示一个表单，要求输入一个名字，submit后将数据以post的方式传递给/do_login, /do_login将名字存放在session中。

如果用户登陆成功，访问/show时会显示用户的名字，此时，打开调试工具，选择session面板，会看到有一个cookie的名称为session。

/logout用于登出，通过将session中的user_name字段pop即可。Flask中的session基于字典类型实现，调用pop方法时会返回pop的键对应的值；如果pop的键并不存在，那么返回的值是pop()的第二个参数。

使用redirect()重定向时，一定要在前面加上return。

访问http://127.0.0.1:5000/login，会出现登录表单，输入之后点击 submit。url会跳至http://127.0.0.1:5000/do_login。

## 设置session的有效时间

设置session的有效时间为5分钟：

```python
from datetime import timedelta
from flask import session, app

session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=5)
```

# 使用cookie

cookie是存储在客户端的记录访问者状态的数据。

常用的用于记录用户登陆状态的session大多是基于cookie实现的。

cookie可以借助flask.Response来实现。

server.py:

```python
from flask import Flask, request, Response, make_response
import time


app = Flask(__name__)

@app.route('/add')
def login():
    res = Response('add cookies')
    res.set_cookie(key='name', value='wuyve', expires=time.time()+6*60)
    return res

@app.route('/show')
def show():
    return request.cookies.__str__()

@app.route('/del')
def del_cookie():
    res = Response('delete cookies')
    res.set_cookie('name', '', expires=0)
    return res

if __name__ == '__main__':
    app.run(port=5000, debug=True)

```

使用Response.set_cookie添加和删除cookie。

expires参数用来设置cookie有效时间，值 可以是datetime对象或者unix时间戳。

`res.set_cookie(key='name', value='wuyve', expires=time.time()+6*60)`表示cookie在从现在开始的6分钟内都是有效的。

要删除cookie，将expire参数的值设为0即可：
res.set_cookie('name', '', expires=0)

运行server.py，在浏览器中打开http://127.0.0.1:5000/add，浏览器界面会显示add cookies，可以查看cookie

# 闪存系统 flashing system

Flask的闪存系统用于向用户提供反馈信息，这些反馈信息一般是对用户上一次操作的反馈。

反馈信息是存储在服务器端的，当服务器向客户端返回反馈信息后，这些反馈信息会被服务器端删除。

