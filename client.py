import requests

user_info = {
    'name': 'wuyve',
    'password': 'wuyve123'
}

r = requests.post('http://127.0.0.1:5000/register', data=user_info)

print(r.text)