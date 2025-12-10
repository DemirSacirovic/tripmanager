import requests


class CryptoData:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_crypto_data(self, name: str):
        url = f"{self.BASE_URL}/coins/{name}"
        response = requests.get(url, timeout=10)

        data = response.json()
        price = data["market_data"]["current_price"]["usd"]
        market_cap = data["market_data"]["market_cap"]["usd"]

        return {"price": price, "market_cap": market_cap}
