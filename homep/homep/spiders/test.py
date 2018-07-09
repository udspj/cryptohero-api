#!/usr/bin/python
#coding:utf-8
import requests

s1 = requests.session()
s1.headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}

url = "https://mainnet.nebulas.io/v1/user/call"
data = {
    "from": "n1Z6SbjLuAEXfhX1UJvXT6BB5osWYxVg3F3",
    "to": "n1gDfiiQLEBu95xDWHGxNi4qToyXjD2vE4D",
    "value": "0",
    "nonce": 0,
    "gasPrice": "1000000",
    "gasLimit": "20000000",
    "contract": {"function": "getTotalSupply", "args": "[]"},
}
z = s1.post(url, json=data)
print(z.json())