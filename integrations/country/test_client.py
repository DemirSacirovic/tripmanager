from unittest.mock import Mock, patch

import requests

from integrations.country.client import CountryClient


@patch("integrations.country.client.requests.get")
def test_get_country_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [{"capital": ["Paris"], "population": 21610000}]
    mock_get.return_value = mock_response

    client = CountryClient()

    result = client.get_country_data("France")
    assert result == {"capital": "Paris", "population": 21610000}


@patch("integrations.country.client.requests.get")
def test_get_country_not_found(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")
    mock_get.return_value = mock_response

    client = CountryClient()
    result = client.get_country_data("FAKECOUNTRY")
    assert "error" in result
