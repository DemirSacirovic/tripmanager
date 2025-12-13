from unittest.mock import Mock, patch

from integrations.currency.client import CurrencyClient


@patch("integrations.currency.client.requests.get")
def test_get_rate_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"EUR": 0.85}}
    mock_get.return_value = mock_response
    client = CurrencyClient()
    result = client.get_rate("USD", "EUR")

    assert result["rate"] == 0.85
    assert result["from"] == "USD"
    assert result["to"] == "EUR"
