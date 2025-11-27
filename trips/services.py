"""
External API integration services.

This module provides service classes for interacting with external flight
and hotel APIs. In production, these would connect to real providers like
Amadeus GDS or Booking.com.
"""
import logging
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class FlightService:
    """
    Service for searching and booking flights.

    In production: Integrates with Amadeus GDS API
    For demo: Returns mock data

    Features:
    - Retry logic with exponential backoff
    - Request timeout handling
    - Structured error logging
    """

    BASE_URL = "https://api.amadeus.com/v2"
    MAX_RETRIES = 3
    INITIAL_BACKOFF = 1  # seconds

    def search_flights(
        self,
        origin: str,
        destination: str,
        date: str
    ) -> Optional[dict]:
        """
        Search for available flights.

        Args:
            origin: IATA airport code (e.g., 'BEG')
            destination: IATA airport code (e.g., 'BCN')
            date: Travel date in YYYY-MM-DD format

        Returns:
            Dict containing flight results or None if unavailable
        """
        # Mock data for demo - in production would call real API
        return {
            "flights": [
                {
                    "id": "FL001",
                    "airline": "Lufthansa",
                    "airline_code": "LH",
                    "price": 250.00,
                    "currency": "EUR",
                    "departure": "08:00",
                    "arrival": "10:30",
                    "duration_minutes": 150,
                },
                {
                    "id": "FL002",
                    "airline": "Air Serbia",
                    "airline_code": "JU",
                    "price": 180.00,
                    "currency": "EUR",
                    "departure": "14:00",
                    "arrival": "16:30",
                    "duration_minutes": 150,
                },
                {
                    "id": "FL003",
                    "airline": "Swiss",
                    "airline_code": "LX",
                    "price": 320.00,
                    "currency": "EUR",
                    "departure": "06:30",
                    "arrival": "08:45",
                    "duration_minutes": 135,
                },
            ],
            "origin": origin,
            "destination": destination,
            "date": date,
            "currency": "EUR",
        }

    def _call_api_with_retry(
        self,
        url: str,
        params: dict,
        method: str = "GET"
    ) -> Optional[dict]:
        """
        Make API call with exponential backoff retry logic.

        Implements retry pattern for handling transient failures:
        - Timeout errors: Retry with backoff
        - 5xx errors: Retry with backoff
        - 4xx errors: Do not retry (client error)

        Args:
            url: Full API endpoint URL
            params: Query parameters or request body
            method: HTTP method (GET or POST)

        Returns:
            JSON response as dict, or None if all retries fail
        """
        backoff = self.INITIAL_BACKOFF

        for attempt in range(self.MAX_RETRIES):
            try:
                if method == "GET":
                    response = requests.get(url, params=params, timeout=10)
                else:
                    response = requests.post(url, json=params, timeout=10)

                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                logger.warning(
                    f"Timeout on attempt {attempt + 1}/{self.MAX_RETRIES} "
                    f"for {url}"
                )
            except requests.exceptions.HTTPError as e:
                if response.status_code >= 500:
                    logger.warning(
                        f"Server error {response.status_code} on attempt "
                        f"{attempt + 1}/{self.MAX_RETRIES}"
                    )
                else:
                    # Client error - don't retry
                    logger.error(f"Client error: {e}")
                    return None
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")

            # Exponential backoff before retry
            if attempt < self.MAX_RETRIES - 1:
                logger.info(f"Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff

        logger.error(f"All {self.MAX_RETRIES} retry attempts failed for {url}")
        return None


class HotelService:
    """
    Service for searching and booking hotels.

    In production: Integrates with Booking.com or Expedia API
    For demo: Returns mock data
    """

    def search_hotels(
        self,
        city: str,
        check_in: str,
        check_out: str
    ) -> Optional[dict]:
        """
        Search for available hotels.

        Args:
            city: City name or code
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)

        Returns:
            Dict containing hotel results
        """
        return {
            "hotels": [
                {
                    "id": "HT001",
                    "name": "Grand Hotel Barcelona",
                    "stars": 4,
                    "price_per_night": 150.00,
                    "currency": "EUR",
                    "rating": 8.5,
                },
                {
                    "id": "HT002",
                    "name": "City Center Inn",
                    "stars": 3,
                    "price_per_night": 85.00,
                    "currency": "EUR",
                    "rating": 7.8,
                },
            ],
            "city": city,
            "check_in": check_in,
            "check_out": check_out,
        }
