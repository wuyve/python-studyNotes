import requests

file_data = {'image': open('flask.png', 'rb')}
user_info = {'info': 'flask'}

r = requests.post('http://127.0.0.1:5000/upload', data=user_info, files=file_data)

print(r.text)
