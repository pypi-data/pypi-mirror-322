import requests
from .exceptions import APIError

class NFT_GamingApi:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_wallet_gaming_metrics(self, blockchain="ethereum", contract_addresses=None, time_range="24h", offset=0, limit=30, sort_by="total_users", sort_order="desc"):
        """
        Retrieve detailed information and trend data for all gaming contracts associated with specified contract addresses.

        :param blockchain: str, blockchain to filter or aggregate data, defaults to 'ethereum'
        :param contract_addresses: list, array of contract addresses to retrieve metrics for, defaults to None
        :param time_range: str, time range to filter results, defaults to '24h'
        :param offset: int, index of the page to return, defaults to 0
        :param limit: int, number of items to return in the result set, defaults to 30
        :param sort_by: str, property to sort the result set by, defaults to 'total_users'
        :param sort_order: str, order to sort the result set, defaults to 'desc'
        :return: dict, the JSON response containing the gaming metrics data
        """
        params = {
            "blockchain": blockchain,
            "contract_address": contract_addresses,
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        url = f"{self.base_url}/nft/wallet/gaming/metrics"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching wallet gaming metrics: {e}")



    def get_wallet_gaming_collection_metrics(self, blockchain="ethereum", contract_addresses=None, time_range="24h", offset=0, limit=30, sort_by="total_users", sort_order="desc"):
        """
        Retrieve detailed information about the value and trends of gaming contract collections, given a specific contract address.
        
        :param blockchain: str, blockchain to filter or aggregate data, defaults to 'ethereum'
        :param contract_addresses: str, comma-separated string of contract addresses to retrieve metrics for, defaults to None
        :param time_range: str, time range to filter results, defaults to '24h'
        :param offset: int, index of the page to return, defaults to 0
        :param limit: int, number of items to return in the result set, defaults to 30
        :param sort_by: str, property to sort the result set by, defaults to 'total_users'
        :param sort_order: str, order to sort the result set, defaults to 'desc'
        :return: dict, the JSON response containing the collection metrics data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        
        # If contract_addresses is provided, add it to the params
        if contract_addresses:
            params["contract_address"] = contract_addresses
        
        url = f"{self.base_url}/nft/wallet/gaming/collection/metrics"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching wallet gaming collection metrics: {e}")



    def get_wallet_gaming_collection_trend(self, blockchain="ethereum", contract_addresses=None, time_range="24h", offset=0, limit=30, sort_by="active_users", sort_order="desc"):
        """
        Retrieve detailed trend metrics for all gaming contracts associated with a specified contract address.
        
        :param blockchain: str, blockchain to filter or aggregate data, defaults to 'ethereum'
        :param contract_addresses: str, comma-separated string of contract addresses to retrieve trend metrics for, defaults to None
        :param time_range: str, time range to filter results, defaults to '24h'
        :param offset: int, index of the page to return, defaults to 0
        :param limit: int, number of items to return in the result set, defaults to 30
        :param sort_by: str, property to sort the result set by, defaults to 'active_users'
        :param sort_order: str, order to sort the result set, defaults to 'desc'
        :return: dict, the JSON response containing the collection trend data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        
        # If contract_addresses is provided, add it to the params
        if contract_addresses:
            params["contract_address"] = contract_addresses
        
        url = f"{self.base_url}/nft/wallet/gaming/collection/trend"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching wallet gaming collection trend: {e}")
