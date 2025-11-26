import logging
from typing import Optional
from venv import logger

import requests
from rest_framework.utils.formatting import re

logger = logging.getLogger(__name__)


class FlightService:
    """
    Service for interacting with flight data.
    U produkciji: Amadeus API
    Za ucenje: mock podaci
    """

    BASE_URL = "https://api.example.com"
    MAX_RETRIES = 3

    def search_flights(self, origin: str, destination: str, date: str) -> Optional[dict]:
        return {
            "flights": [
                {"id": "FL001", "airile": "Lufthansa", "price": 250.00, "departure": "08:00", "arrival": "10:30"},
                {"id": "FL002", "airline": "Air Serbia", "price": 180.00, "departure": "14:00", "arrival": "16:30"},
            ],
            "origin": origin,
            "destination": destination,
            "date": date,
        }

    def _call_api_with_retry(self, url: str, params: dict) -> Optional[dict]:
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout attempt {attempt + 1}/{self.MAX_RETRIES}")
            except requests.exceptions.RequestException as e:
                logger.error(f"API error: {e}")
        return None
