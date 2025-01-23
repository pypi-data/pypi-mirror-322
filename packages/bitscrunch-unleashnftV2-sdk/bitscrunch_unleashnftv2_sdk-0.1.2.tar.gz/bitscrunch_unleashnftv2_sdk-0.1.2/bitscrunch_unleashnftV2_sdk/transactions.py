import requests
from .exceptions import APIError

class NFT_Transactions:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_transactions(self, blockchain="ethereum", time_range="24h", contract_address=None, token_id=None, offset=0, limit=30):
        """
        Retrieve a paginated and sorted list of NFT transactions.

        :param blockchain: str, blockchain to filter or aggregate data, defaults to 'ethereum'
        :param time_range: str, time range to filter results, defaults to '24h'
        :param contract_address: str, specific contract address to filter data
        :param token_id: str, specific token ID to filter data
        :param offset: int, index of the page to return, defaults to 0
        :param limit: int, number of items to return in the result set, defaults to 30
        :return: dict, the JSON response containing the transaction data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "offset": offset,
            "limit": limit
        }

        # Optional parameters
        if contract_address:
            params["contract_address"] = contract_address
        if token_id:
            params["token_id"] = token_id

        url = f"{self.base_url}/nft/transactions"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching NFT transactions: {e}")
