import requests
from .exceptions import APIError

class NFT_Price_Estimate:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_price_estimate(self, blockchain, contract_address, token_id):
        """
        Retrieve the predicted price details for a specific NFT within the requested collection.
        """
        if not blockchain or not contract_address or not token_id:
            raise ValueError("blockchain, contract_address, and token_id are required parameters.")

        params = {
            "blockchain": blockchain,
            "contract_address": contract_address,
            "token_id": token_id
        }

        url = f"{self.base_url}/nft/liquify/price_estimate"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching NFT price estimate: {e}")

    def get_collection_price_estimate(self, blockchain, contract_address, offset=0, limit=30):
        """
        Retrieve the predicted price details for the requested NFT collection and specific NFTs.
        """
        if not blockchain or not contract_address:
            raise ValueError("blockchain and contract_address are required parameters.")

        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")

        params = {
            "blockchain": blockchain,
            "contract_address": contract_address,
            "offset": offset,
            "limit": limit
        }

        url = f"{self.base_url}/nft/liquify/collection/price_estimate"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching collection price estimate: {e}")

    def get_supported_collections(self, blockchain, offset=0, limit=30):
        """
        Retrieve metadata for supported collections with AI-generated price predictions.

        :param blockchain: str, blockchain to filter data, e.g., 'ethereum'
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30)
        :return: dict, the JSON response containing metadata for supported collections
        """
        if not blockchain:
            raise ValueError("blockchain is a required parameter.")

        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100.")

        params = {
            "blockchain": blockchain,
            "offset": offset,
            "limit": limit
        }

        url = f"{self.base_url}/nft/liquify/collection/supported_collections"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching supported collections: {e}")
