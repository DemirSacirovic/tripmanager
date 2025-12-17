import logging

import requests

logger = logging.getLogger(__name__)


class CurrencyClient:
    BASE_URL = "https://open.er-api.com/v6/latest"

    def get_rate(self, from_currency: str, to_currency: str) -> dict:
        url = f"{self.BASE_URL}/{from_currency}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status
            data = response.json()
            rate = data["rates"][to_currency]

            return {"from": from_currency, "to": to_currency, "rate": rate}

        except requests.exceptions.Timeout:
            logger.error("API timeout")
            return {"error": "API timeout"}
        except requests.exceptions.RequestException as e:
            logger.error(f"API error: {e}")
            return {"error": f"API unavailable"}
        except KeyError:
            logger.error(f"Currency: {to_currency} not found")
            return {"error": f"Currency {to_currency} not found"}
