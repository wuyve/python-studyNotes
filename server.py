from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    print(request.stream.read())
    return 'welcome'

if __name__ == '__main__':
    app.run(port=5000, debug=True)