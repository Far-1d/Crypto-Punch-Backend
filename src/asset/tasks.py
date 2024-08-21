import time
import requests

def get_coinList_with_marketData():
    for i in range(14):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={i+1}"
        headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": "CG-k2MJpGGjiMiW4S9hQVns7q4T"
        }

        response = requests.get(url, headers=headers)
        json_res = response.json()

        print(len(json_res))

        for coin in json_res:
            sample = {}
            sample['name'] = coin['name']
            sample['symbol'] = coin['symbol']
            sample['price'] = coin['current_price']
            sample['rank'] = coin['market_cap_rank']
            sample['daily_change'] = coin['price_change_24h']
            sample['icon'] = coin['image']
            sample['market_cap'] = coin['market_cap']
            sample['total_volume'] = coin['total_volume']
            sample['fully_diluted_valuation'] = coin['fully_diluted_valuation']
            sample['high_24h'] = coin['high_24h']
            sample['low_24h'] = coin['low_24h']
            sample['price_change_percentage_24h'] = coin['price_change_percentage_24h']
            sample['circulating_supply'] = coin['circulating_supply']
            sample['ath'] = coin['ath']
            sample['ath_change_percentage'] = coin['ath_change_percentage']
            sample['ath_date'] = coin['ath_date']
            sample['atl'] = coin['atl']
            sample['atl_change_percentage'] = coin['atl_change_percentage']
            sample['atl_date'] = coin['atl_date']
            
            if sample['name'] and sample['icon'] and sample['price'] and sample['symbol']:
                yield sample
        
        time.sleep(10)

def get_exchange_date():
    for i in range(14):
        url = f"https://api.coingecko.com/api/v3/exchanges?per_page=250"
        headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": "CG-k2MJpGGjiMiW4S9hQVns7q4T"
        }

        response = requests.get(url, headers=headers)
        json_res = response.json()

        print(len(json_res))

        for coin in json_res:
            sample = {}
            sample['name'] = coin['name']
            sample['url'] = coin['url']
            sample['established'] = coin['year_established']
            sample['country'] = coin['country']
            sample['trust_score'] = coin['trust_score']
            sample['trust_rank'] = coin['trust_score_rank']
            sample['image'] = coin['image']
            sample['daily_volume'] = coin['trade_volume_24h_btc']
            
            if sample['name'] and sample['image'] and sample['url'] and sample['established']:
                yield sample
