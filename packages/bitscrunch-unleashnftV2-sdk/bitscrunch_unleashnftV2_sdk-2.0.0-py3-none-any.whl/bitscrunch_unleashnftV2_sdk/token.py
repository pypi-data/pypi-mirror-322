import requests
from .exceptions import APIError

class Token:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_token_balance(self, blockchain, token_address, address, offset=0, limit=30):
        """
        Retrieve token balance details.

        :param blockchain: str, blockchain network (e.g., 'ethereum')
        :param token_address: str, address of the token
        :param address: str, wallet address to retrieve the balance for
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30, max is 100)
        :return: dict, the JSON response containing token balance details
        """
        # Validate inputs
        if not blockchain:
            raise ValueError("blockchain is a required parameter.")
        if not token_address:
            raise ValueError("token_address is a required parameter.")
        if not address:
            raise ValueError("address is a required parameter.")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")

        params = {
            "blockchain": blockchain,
            "token_address": token_address,
            "address": address,
            "offset": offset,
            "limit": limit
        }

        url = f"{self.base_url}/token/balance"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching token balance: {e}")


    def get_token_metrics(self, blockchain, token_address, offset=0, limit=30):
        """
        Retrieve token metrics details.

        :param blockchain: str, blockchain network (e.g., 'ethereum')
        :param token_address: str, address of the token
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30, max is 100)
        :return: dict, the JSON response containing token metrics details
        """
        if not blockchain:
            raise ValueError("blockchain is a required parameter.")
        if not token_address:
            raise ValueError("token_address is a required parameter.")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")

        params = {
            "blockchain": blockchain,
            "token_address": token_address,
            "offset": offset,
            "limit": limit
        }

        url = f"{self.base_url}/token/metrics"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching token metrics: {e}")



    def get_token_holders(self, blockchain, token_address, offset=0, limit=30):
        """
        Retrieve token holders details.

        :param blockchain: str, blockchain network (e.g., 'ethereum')
        :param token_address: str, address of the token
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30, max is 100)
        :return: dict, the JSON response containing token holders details
        """
        if not blockchain:
            raise ValueError("blockchain is a required parameter.")
        if not token_address:
            raise ValueError("token_address is a required parameter.")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")

        params = {
            "blockchain": blockchain,
            "token_address": token_address,
            "offset": offset,
            "limit": limit
        }

        url = f"{self.base_url}/token/holders"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching token holders: {e}")
        


    def get_token_transfers(self, token_address, blockchain="ethereum", time_range="all", offset=0, limit=30):
        """
        Get list of top token holders, including their percentage ownership, ranking, and relevant titles.

        :param token_address: str, address of the token
        :param blockchain: str, blockchain network (default is 'ethereum')
        :param time_range: str, time range to filter results (default is 'all')
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30, max is 100)
        :return: dict, the JSON response containing token transfer details
        """
        if not token_address:
            raise ValueError("token_address is a required parameter.")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")

        params = {
            "token_address": token_address,
            "blockchain": blockchain,
            "time_range": time_range,
            "offset": offset,
            "limit": limit
        }

        url = f"{self.base_url}/token/transfers"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching token transfers: {e}")
        

    def get_token_price_prediction(self, token_address, offset=0, limit=30):
        """
        Retrieve token price prediction details.
    
        :param token_address: str, address of the token
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30, max is 100)
        :return: dict, the JSON response containing token price prediction details
        """
        if not token_address:
            raise ValueError("token_address is a required parameter.")
        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")
    
        params = {
            "token_address": token_address,
            "offset": offset,
            "limit": limit
        }
    
        url = f"{self.base_url}/token/price_prediction"
    
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching token price prediction: {e}")