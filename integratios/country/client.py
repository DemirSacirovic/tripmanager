import requests


class CountryClient:
    BASE_URL = "https://restcountries.com/v3.1"

    def get_country_data(self, name: str):
        url = f"{self.BASE_URL}/name/{name}"
        response = requests.get(url, timeout=10)
        data = response.json()

        return {"capital": data[0]["capital"][0], "population": data[0]["population"]}
