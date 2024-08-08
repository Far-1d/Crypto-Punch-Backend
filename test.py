import requests

# url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"
#
# headers = {"accept": "application/json"}
#
# response = requests.get(url, headers=headers)

url = "https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&market_data=false"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-k2MJpGGjiMiW4S9hQVns7q4T"
}

response = requests.get(url, headers=headers)

print(response.json())
