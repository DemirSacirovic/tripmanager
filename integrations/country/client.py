import logging

import requests

logger = logging.getLogger(__name__)


class CountryClient:
    BASE_URL = "https://restcountries.com/v3.1"

    def get_country_data(self, name: str):
        url = f"{self.BASE_URL}/name/{name}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {"capital": data[0]["capital"][0], "population": data[0]["population"]}
        except requests.exceptions.Timeout:
            logger.error("API timeout")
            return {"error": "API timeout"}
        except requests.exceptions.RequestException as e:
            logger.error(f"API error: {e}")
            return {"error": "API unavailable"}
        except (KeyError, IndexError):
            logger.error(f"Country {name} not found")
            return {"error": "Country not found"}
