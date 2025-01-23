import requests

class SupportedBlockchain:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def retrieve_supported_blockchains(self, offset=0, limit=30):
        """
        Fetch a list of supported blockchains with pagination.

        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing supported blockchains
        """
        url = f"{self.base_url}/blockchains?offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to retrieve supported blockchains: {str(e)}")