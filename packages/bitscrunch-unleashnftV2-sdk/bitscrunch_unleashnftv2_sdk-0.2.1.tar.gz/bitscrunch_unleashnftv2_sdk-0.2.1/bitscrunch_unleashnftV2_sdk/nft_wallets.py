import requests
from .exceptions import APIError

class NFTWalletAPI:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_wallet_analytics(self, wallets, blockchain='ethereum', time_range='24h', sort_by='volume', sort_order='desc', offset=0, limit=30):
        """
        Fetch analytics data for specified wallets over a given time range.

        :param wallets: list of str, wallets to include in the query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param time_range: str, time range for filtering the results, defaults to '24h'
        :param sort_by: str, property to sort the results by, defaults to 'volume'
        :param sort_order: str, order to sort the result set by, defaults to 'desc'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing wallet analytics data
        """
        if isinstance(wallets, list):
            wallets = ",".join(wallets)
        url = f"{self.base_url}/nft/wallet/analytics?wallet={wallets}&blockchain={blockchain}&time_range={time_range}&sort_by={sort_by}&sort_order={sort_order}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch wallet analytics data: {str(e)}")
        
    def get_wallet_scores(self, wallets, blockchain='ethereum', sort_by='portfolio_value', sort_order='desc', time_range='24h', offset=0, limit=30):
        """
        Fetch score data for specified wallets over a given time range.

        :param wallets: list of str, wallets to include in the query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param sort_by: str, property to sort the results by, defaults to 'portfolio_value'
        :param sort_order: str, order to sort the result set by, defaults to 'desc'
        :param time_range: str, time range for filtering the results, defaults to '24h'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing wallet scores data
        """
        if isinstance(wallets, list):
            wallets = ",".join(wallets)
        url = f"{self.base_url}/nft/wallet/scores?wallet={wallets}&blockchain={blockchain}&time_range={time_range}&sort_by={sort_by}&sort_order={sort_order}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch wallet scores data: {str(e)}")

    def get_wallet_traders(self, wallets, blockchain='ethereum', sort_by='traders', sort_order='desc', time_range='24h', offset=0, limit=30):
        """
        Fetch trader data for specified wallets.

        :param wallets: list of str, wallets to include in the query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param sort_by: str, property to sort the results by, defaults to 'traders'
        :param sort_order: str, order to sort the result set by, defaults to 'desc'
        :param time_range: str, time range for filtering the results, defaults to '24h'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing wallet trader data
        """
        if isinstance(wallets, list):
            wallets = ",".join(wallets)
        url = f"{self.base_url}/nft/wallet/traders?wallet={wallets}&blockchain={blockchain}&time_range={time_range}&sort_by={sort_by}&sort_order={sort_order}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch wallet traders data: {str(e)}")

    def get_wallet_washtrade(self, wallets, blockchain='ethereum', sort_by='washtrade_volume', sort_order='desc', time_range='24h', offset=0, limit=30):
        """
        Fetch washtrade data for specified wallets.

        :param wallets: list of str, wallets to include in the query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param sort_by: str, property to sort the results by, defaults to 'washtrade_volume'
        :param sort_order: str, order to sort the result set by, defaults to 'desc'
        :param time_range: str, time range for filtering the results, defaults to '24h'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing wallet washtrade data
        """
        if isinstance(wallets, list):
            wallets = ",".join(wallets)
        url = f"{self.base_url}/nft/wallet/washtrade?wallet={wallets}&blockchain={blockchain}&time_range={time_range}&sort_by={sort_by}&sort_order={sort_order}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch wallet washtrade data: {str(e)}")

    def get_wallet_profile(self, wallets, offset=0, limit=30):
        """
        Fetch profile data for specified wallets.

        :param wallets: list of str or str, wallets to include in the query
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing wallet profile data
        """
        if isinstance(wallets, list):
            wallets = ",".join(wallets)
        url = f"{self.base_url}/nft/wallet/profile?wallet={wallets}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch wallet profile data: {str(e)}")
        
    