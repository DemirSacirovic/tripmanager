import requests


class CryptoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_crypto(self, name: str):
        url = f"{self.BASE_URL}/coins/{name}"
        response = requests.get(url, timeout=10)
        data = response.json()

        return {
            "price": data["market_data"]["current_price"]["usd"],
            "market_cap": data["market_data"]["market_cap"]["usd"],
        }
