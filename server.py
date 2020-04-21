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
