import requests
from .exceptions import APIError

class CollectionAPI:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_collection_metadata(self, sort_order='desc', offset=0, limit=30, contract_address=None):
        """
        Fetch metadata for NFT collections.

        :param sort_order: str, the order to sort the result set, defaults to 'desc'
        :param offset: int, index of the page to return, defaults to 0
        :param limit: int, number of items to return in the result set, defaults to 30
        :param contract_address: str or list, contract addresses as a comma-separated string or list of addresses
        :return: dict, the JSON response containing the metadata
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        
        params = {
            "sort_order": sort_order,
            "offset": offset,
            "limit": limit,
            "contract_address": contract_address
        }
        url = f"{self.base_url}/nft/collection/metadata"
        response = requests.get(url, headers=self.headers, params={k: v for k, v in params.items() if v is not None})
        return response.json()

    def get_collection_analytics_data(self, blockchain='ethereum', contract_address=None, offset=0, limit=30, sort_by='sales', time_range='24h', sort_order='desc'):
        """
        Fetch aggregate data for blockchain and NFT collections based on various metrics.

        :param blockchain: str, blockchain type, default 'ethereum'
        :param contract_addresses: list, contract addresses to include in the aggregation
        :param offset: int, pagination offset
        :param limit: int, pagination limit
        :param sort_by: str, property to sort the results by
        :param time_range: str, time range for filtering the results
        :param sort_order: str, order to sort the result set by
        :return: dict, the JSON response containing aggregated data
        """

        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/analytics?blockchain={blockchain}&contract_address={contract_address}&offset={offset}&limit={limit}&sort_by={sort_by}&time_range={time_range}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch aggregate blockchain data: {str(e)}")
        
    
    def get_collection_holders_data(self, blockchain='ethereum', contract_address=None, time_range='24h', offset=0, limit=30, sort_by='holders', sort_order='desc'):
        """
        Fetch data about NFT holders for specified contracts over a given time range, sorted by specified criteria.

        :param blockchain: str, the type of blockchain, defaults to 'ethereum'
        :param contract_addresses: list of str, contract addresses to include in the query
        :param time_range: str, the time range over which to filter results, defaults to '24h'
        :param offset: int, the pagination offset, defaults to 0
        :param limit: int, the number of results to return, defaults to 30
        :param sort_by: str, the property by which to sort results, defaults to 'holders'
        :param sort_order: str, the order of sorting, defaults to 'desc'
        :return: dict, the JSON response containing data about NFT holders
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/holders?blockchain={blockchain}&contract_address={contract_address}&time_range={time_range}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch collection holders data: {str(e)}")


    def get_collection_scores(self, blockchain='ethereum', contract_address=None, time_range='24h', offset=0, limit=30, sort_by='market_cap', sort_order='desc'):
        """
        Fetch NFT collection scores filtered by blockchain, contract address, and other parameters.

        :param blockchain: str, the blockchain type, defaults to 'ethereum'
        :param contract_address: str, the contract address to include in the query
        :param time_range: str, the time range for filtering results, defaults to '24h'
        :param offset: int, the pagination offset, defaults to 0
        :param limit: int, the number of items to return, defaults to 30
        :param sort_by: str, the property to sort results by, defaults to 'market_cap'
        :param sort_order: str, the order of sorting, defaults to 'desc'
        :return: dict, the JSON response containing the collection scores
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/scores?blockchain={blockchain}&contract_address={contract_address}&time_range={time_range}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch collection scores: {str(e)}")
        
    def get_collection_traders_data(self, blockchain='ethereum', contract_address=None, time_range='24h', offset=0, limit=30, sort_by='traders', sort_order='desc'):
        """
        Fetch NFT collection Traders Data filtered by blockchain, contract address, and other parameters.

        :param blockchain: str, the blockchain type, defaults to 'ethereum'
        :param contract_address: str, the contract address to include in the query
        :param time_range: str, the time range for filtering results, defaults to '24h'
        :param offset: int, the pagination offset, defaults to 0
        :param limit: int, the number of items to return, defaults to 30
        :param sort_by: str, the property to sort results by, defaults to 'traders'
        :param sort_order: str, the order of sorting, defaults to 'desc'
        :return: dict, the JSON response containing the collection scores
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/traders?blockchain={blockchain}&contract_address={contract_address}&time_range={time_range}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch collection traders data: {str(e)}")

    def get_collection_washtrade_data(self, blockchain='ethereum', contract_address=None, time_range='24h', offset=0, limit=30, sort_by='washtrade_assets', sort_order='desc'):
        """
        Fetch NFT collection Traders Data filtered by blockchain, contract address, and other parameters.

        :param blockchain: str, the blockchain type, defaults to 'ethereum'
        :param contract_address: str, the contract address to include in the query
        :param time_range: str, the time range for filtering results, defaults to '24h'
        :param offset: int, the pagination offset, defaults to 0
        :param limit: int, the number of items to return, defaults to 30
        :param sort_by: str, the property to sort results by, defaults to 'washtrade_assets'
        :param sort_order: str, the order of sorting, defaults to 'desc'
        :return: dict, the JSON response containing the collection scores
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/washtrade?blockchain={blockchain}&contract_address={contract_address}&time_range={time_range}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch collection washtrade data: {str(e)}")

    def get_collection_whales_data(self, blockchain='ethereum', contract_address=None, time_range='24h', offset=0, limit=30, sort_by='nft_count', sort_order='desc'):
        """
        Fetch NFT collection Traders Data filtered by blockchain, contract address, and other parameters.

        :param blockchain: str, the blockchain type, defaults to 'ethereum'
        :param contract_address: str, the contract address to include in the query
        :param time_range: str, the time range for filtering results, defaults to '24h'
        :param offset: int, the pagination offset, defaults to 0
        :param limit: int, the number of items to return, defaults to 30
        :param sort_by: str, the property to sort results by, defaults to 'nft_count'
        :param sort_order: str, the order of sorting, defaults to 'desc'
        :return: dict, the JSON response containing the collection scores
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/whales?blockchain={blockchain}&contract_address={contract_address}&time_range={time_range}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch collection whales data: {str(e)}")

    def get_collection_profile_data(self, blockchain='ethereum', contract_address=None, time_range='all', offset=0, limit=30, sort_by='washtrade_index', sort_order='desc'):
        """
        Fetch NFT collection Traders Data filtered by blockchain, contract address, and other parameters.

        :param blockchain: str, the blockchain type, defaults to 'ethereum'
        :param contract_address: str, the contract address to include in the query
        :param time_range: str, the time range for filtering results, defaults to '24h'
        :param offset: int, the pagination offset, defaults to 0
        :param limit: int, the number of items to return, defaults to 30
        :param sort_by: str, the property to sort results by, defaults to 'washtrade_index'
        :param sort_order: str, the order of sorting, defaults to 'desc'
        :return: dict, the JSON response containing the collection scores
        """
        if isinstance(contract_address, list):
            contract_address = ",".join(contract_address)
        url = f"{self.base_url}/nft/collection/profile?blockchain={blockchain}&contract_address={contract_address}&time_range={time_range}&offset={offset}&limit={limit}&sort_by={sort_by}&sort_order={sort_order}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch collection profile data: {str(e)}")
