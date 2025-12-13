from unittest.mock import Mock, patch

from integrations.crypto.client import CryptoClient


@patch("integrations.crypto.client.requests.get")
def test_get_crypto_data(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "market_data": {"current_price": {"usd": 10000}, "market_cap": {"usd": 1000000000000}}
    }
    mock_get.return_value = mock_response

    client = CryptoClient()
    result = client.get_crypto("bitcoin")

    assert result == {"price": 10000, "market_cap": 1000000000000}
