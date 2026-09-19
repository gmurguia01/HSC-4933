##############################
# Gabriel Murguia , USF LAB 4#
##############################

import requests

YEAR = 2020
DATASET = "dec/pl"

URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "538e76ad89aa33fbccdb796e6cf1cd5f52e1b57c"

fips_input = input("Enter FIPS code: ")

variables = input("Enter variables: ")

params = {
    "get":variables,
    "for": f"state:{fips_input}",
    "key": API_KEY
}

response = requests.get(URL, params=params)
data = response.json()

print(f"\nFound {len(data) - 1} Rows of Data.\n")

for row in data:
    print(row)


