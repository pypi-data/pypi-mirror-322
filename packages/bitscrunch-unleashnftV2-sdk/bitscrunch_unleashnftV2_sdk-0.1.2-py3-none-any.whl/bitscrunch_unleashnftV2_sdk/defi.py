import requests
from .exceptions import APIError
class DeFi:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_defi_pool_metadata(self, blockchains=None, pair_addresses=None, offset=0, limit=30):
        """
        Fetch metadata for specified DeFi pools.

        :param blockchains: list of str, blockchain types
        :param pair_addresses: list of str, pair addresses of the DeFi pools
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing DeFi pool metadata
        """
        blockchain_param = ','.join(blockchains) if isinstance(blockchains, list) else blockchains
        pair_address_param = ','.join(pair_addresses) if isinstance(pair_addresses, list) else pair_addresses
        url = f"{self.base_url}/defi/pool/metadata?blockchain={blockchain_param}&pair_address={pair_address_param}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand metadata: {e}")

    def get_defi_pool_metrics(self, blockchain, pair_address, offset=0, limit=30):
        """
        Fetch metrics for a specified DeFi pool.

        :param blockchain: str, blockchain type
        :param pair_address: str, address of the pool
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing DeFi pool metrics
        """
        url = f"{self.base_url}/defi/pool/metrics?blockchain={blockchain}&pair_address={pair_address}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch DeFi pool metrics: {str(e)}")

    def get_defi_protocol_metadata(self, blockchain, protocol, offset=0, limit=30):
        """
        Fetch metadata for a specified DeFi protocol.

        :param blockchain: str, blockchain type
        :param protocol: str, identifier for the protocol
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing DeFi protocol metadata
        """
        url = f"{self.base_url}/defi/pool?blockchain={blockchain}&protocol={protocol}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch DeFi protocol metadata: {str(e)}")
        
    def get_supported_defi_protocols(self, blockchains, offset=0, limit=30):
        """
        Fetch supported DeFi protocols for specified blockchains.

        :param blockchains: list of str, blockchains to query
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, maximum 100, defaults to 30
        :return: dict, the JSON response containing supported DeFi protocols
        """
        blockchain_param = ','.join(blockchains) if isinstance(blockchains, list) else blockchains
        url = f"{self.base_url}/defi/pool/supported_protocols?blockchain={blockchain_param}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch supported DeFi protocols: {str(e)}")
