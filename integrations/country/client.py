import requests


class CountriesData:
    BASE_URL = "https://restcountries.com/v3.1"

    def get_country_data(self, name: str):
        url = f"{self.BASE_URL}/name/{name}"
        response = requests.get(url, timeout=10)

        data = response.json()
        grad = data[0]["capital"][0]
        populacija = data[0]["population"]

        return {"capital": grad, "population": populacija}
