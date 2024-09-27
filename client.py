import requests

response = requests.post("http://127.0.0.1:80/advertisement", json={
    "title": "iPhone 16 Pro",
    "description": "новый",
    "price": 215490.99,
    "owner": 1
})

# response = requests.get("http://127.0.0.1:80/advertisement/1")

# response = requests.get("http://127.0.0.1:80/advertisement/?title=iphone")

# response = requests.patch("http://127.0.0.1:80/advertisement/1", json={
#     "description": "б/у"
# })

# response = requests.delete("http://127.0.0.1:80/advertisement/1")

print(response.status_code)
print(response.json())
