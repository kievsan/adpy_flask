import requests as requests

# response = requests.delete('http://127.0.0.1:5000')
# print(response.status_code)
# print(response.json())

# response = requests.get('http://127.0.0.1:5000/user/1000')
# print(response.status_code)
# print(response.json())

response = requests.post(
    'http://127.0.0.1:5000/user/',
    json={
        "username": "user_111",
        "password": "psw123456"
    })
print(response.status_code)
print(response.json())

response = requests.patch(
    'http://127.0.0.1:5000/user/1',
    json={
        "username": "user_911",
    }
)
print(response.status_code)
print(response.json())

# response = requests.get('http://127.0.0.1:5000/user/2')
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     'http://127.0.0.1:5000/ad/',
#     json={
#         "header": "ad_111",
#         "user_id": "1"
#     })
# print(response.status_code)
# print(response.json())

response = requests.post(
    'http://127.0.0.1:5000/ad/',
    json={
        "user_id": "1"
    })
print(response.status_code)
print(response.json())

# response = requests.get('http://127.0.0.1:5000/ad/1')
# print(response.status_code)
# print(response.json())

# response = requests.post(
#     'http://127.0.0.1:5000/ad/',
#     json={
#         "user_id": "2"
#     })
# print(response.status_code)
# print(response.json())

response = requests.patch(
    'http://127.0.0.1:5000/ad/1',
    json={
        "header": "patch ad",
    }
)
print(response.status_code)
try:
    print(response.json())
except Exception:
    print(response.text)

# response = requests.get('http://127.0.0.1:5000/ad/3')
# print(response.status_code)
# print(response.json())

