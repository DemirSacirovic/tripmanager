import logging

import requests

logger = logging.getLogger(__name__)


class WeatherClient:
    """Client fot fetching weather data from wttr.in"""

    BASE_URL = "https://wttr.in/"

    def get_weather(self, city: str) -> dict:
        try:
            url = f"{self.BASE_URL}/{city}?format=j1"
            logger.info(f"Fetching weather data for {city}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            current = data["current_condition"][0]

            return {"city": city, "temp_c": current["temp_C"], "condition": current["weatherDesc"][0]["value"]}
        except requests.Timeout:
            logger.error(f"Timeout error while fetching weather data for {city}")
            raise
        except requests.RequestException as e:
            logger.error(f"Error while fetching weather data for {city}: {e}")
            raise
