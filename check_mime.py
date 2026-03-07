import requests
try:
    r = requests.get('http://localhost:8000/assets/index--iS3Xt5U.js')
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type')}")
    print(f"Content (start): {r.text[:100]}")
except Exception as e:
    print(e)
