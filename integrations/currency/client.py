import logging

import requests

logger = logging.getLogger(__name__)


class CurrencyClient:
    BASE_URL = "https://open.er-api.com/v6/latest"

    def get_rate(self, from_currency: str, to_currency: str) -> dict:
        url = f"{self.BASE_URL}/{from_currency}"

        response = requests.get(url, timeout=10)
        data = response.json()
        rate = data["rates"][to_currency]

        return {"from": from_currency, "to": to_currency, "rate": rate}
