import requests
from .exceptions import APIError

class MarketplaceAPI:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_marketplace_metadata(self, sort_order='desc', offset=0, limit=30):
        """
        Retrieve metadata for all available NFT marketplaces.

        :param sort_order: str, order to sort the result set, defaults to 'desc'
        :param offset: int, index of the page to return, defaults to 0
        :param limit: int, number of items to return in the result set, defaults to 30
        :return: dict, the JSON response containing the metadata
        """
        params = {
            "sort_order": sort_order,
            "offset": offset,
            "limit": limit
        }
        url = f"{self.base_url}/nft/marketplace/metadata"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching marketplace metadata: {e}")
    

    def get_marketplace_analytics(self, blockchain="ethereum", time_range="24h", 
                                  sort_by="name", sort_order="desc", 
                                  offset=0, limit=30, name=None):
        """
        Retrieve detailed analytics and trend data for a specific marketplace.

        :param blockchain: str, the blockchain to filter by (default is 'ethereum')
        :param time_range: str, the time range for filtering results (default is '24h')
        :param sort_by: str, the property to sort the result set by (default is 'name')
        :param sort_order: str, the order to sort the result set (default is 'desc')
        :param offset: int, index of the page to return (default is 0)
        :param limit: int, number of items to return in the result set (default is 30)
        :param name: list of strings, specific metric group values to return (optional)
        :return: dict, the JSON response containing the analytics data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "offset": offset,
            "limit": limit
        }

        if name:
            params["name"] = ",".join(name)

        url = f"{self.base_url}/nft/marketplace/analytics"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching marketplace analytics: {e}")
            return None



    def get_marketplace_holders(self, blockchain="ethereum", time_range="24h", sort_by="name", 
                                sort_order="desc", offset=0, limit=30, name=None):
        """
        Retrieve detailed metrics and trend data for all holders within a specific marketplace.

        :param blockchain: str, Filter or get aggregate blockchain data (defaults to ethereum)
        :param time_range: str, Time range to filter results (defaults to 24h)
        :param sort_by: str, Property to sort result set by (defaults to 'name')
        :param sort_order: str, Order to sort the result set in (defaults to 'desc')
        :param offset: int, Index of the page to return (defaults to 0)
        :param limit: int, Number of items to return (defaults to 30)
        :param name: list of strings, Metric group values to return (optional, e.g., "opensea")
        :return: dict, the JSON response containing the marketplace holder data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "offset": offset,
            "limit": limit
        }
        
        if name:
            params["name"] = name
        
        url = f"{self.base_url}/nft/marketplace/holders"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching marketplace holders data: {e}")
    


    def get_marketplace_traders(self, blockchain="ethereum", time_range="24h", sort_by="name", 
                                sort_order="desc", offset=0, limit=30, name=None):
        """
        Retrieve detailed metrics and trend data for all traders within a specific marketplace.

        :param blockchain: str, Filter or get aggregate blockchain data (defaults to ethereum)
        :param time_range: str, Time range to filter results (defaults to 24h)
        :param sort_by: str, Property to sort result set by (defaults to 'name')
        :param sort_order: str, Order to sort the result set in (defaults to 'desc')
        :param offset: int, Index of the page to return (defaults to 0)
        :param limit: int, Number of items to return (defaults to 30)
        :param name: list of strings, Metric group values to return (optional, e.g., "opensea")
        :return: dict, the JSON response containing the marketplace trader data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "offset": offset,
            "limit": limit
        }
        
        if name:
            params["name"] = name
        
        url = f"{self.base_url}/nft/marketplace/traders"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching marketplace traders data: {e}")




    def get_marketplace_washtrade(self, blockchain="ethereum", time_range="24h", sort_by="name", 
                                  sort_order="desc", offset=0, limit=30, name=None):
        """
        Retrieve detailed washtrade metrics and trend data for a specific marketplace.

        :param blockchain: str, Filter or get aggregate blockchain data (defaults to ethereum)
        :param time_range: str, Time range to filter results (defaults to 24h)
        :param sort_by: str, Property to sort result set by (defaults to 'name')
        :param sort_order: str, Order to sort the result set in (defaults to 'desc')
        :param offset: int, Index of the page to return (defaults to 0)
        :param limit: int, Number of items to return (defaults to 30)
        :param name: list of strings, Metric group values to return (optional, e.g., "opensea")
        :return: dict, the JSON response containing the marketplace washtrade data
        """
        params = {
            "blockchain": blockchain,
            "time_range": time_range,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "offset": offset,
            "limit": limit
        }
        
        if name:
            params["name"] = name
        
        url = f"{self.base_url}/nft/marketplace/washtrade"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching marketplace washtrade data: {e}")
