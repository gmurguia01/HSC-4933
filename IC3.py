import requests

YEAR = 2020
DATASET = "dec/pl"

URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "538e76ad89aa33fbccdb796e6cf1cd5f52e1b57c"

params = {
    "get": "NAME,P1_001N",
    "for": "state:*",
    "key": API_KEY,
}

response = requests.get(URL, params=params)
response.raise_for_status()
if response.status_code !=200:
    print(f"Request failed ({response.status_code})")
    print(response.text)
    raise SystemExit(1)
data = response.json()






header = data[0]
rows = data[1:]

print(f"Got {len(data) - 1} rows back.")

for row in rows:
    print(row)