import requests

class Wallet:
    def __init__(self, api_key, base_url="https://api.unleashnfts.com/api/v2"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "x-api-key": self.api_key
        }

    def get_defi_portfolio(self, addresses, blockchain='ethereum', time_range='all', offset=0, limit=30):
        """
        Fetch DeFi portfolio balances for specified wallet addresses.

        :param addresses: list of str, wallet addresses to query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param time_range: str, time range for filtering the results, defaults to 'all'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing DeFi portfolio balances
        """
        address_param = ','.join(addresses) if isinstance(addresses, list) else addresses
        url = f"{self.base_url}/wallet/balance/defi?address={address_param}&blockchain={blockchain}&time_range={time_range}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch DeFi portfolio balances: {str(e)}")
        

    def get_nft_portfolio(self, wallet, blockchain='ethereum', time_range='all', offset=0, limit=30):
        """
        Fetch NFT portfolio balances for a specified wallet address.

        :param wallet: str, wallet address to query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param time_range: str, time range for filtering the results, defaults to 'all'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing NFT portfolio balances
        """
        url = f"{self.base_url}/wallet/balance/nft?wallet={wallet}&blockchain={blockchain}&time_range={time_range}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch NFT portfolio balances: {str(e)}")

    def get_erc20_portfolio(self, address, blockchain='ethereum', time_range='all', offset=0, limit=30):
        """
        Fetch ERC-20 token balances for a specified wallet address.

        :param address: str, wallet address to query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param time_range: str, time range for filtering the results, defaults to 'all'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing ERC-20 token balances
        """
        url = f"{self.base_url}/wallet/balance/token?address={address}&blockchain={blockchain}&time_range={time_range}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch ERC-20 token balances: {str(e)}")

    def get_wallet_labels(self, address, blockchain='ethereum', offset=0, limit=30):
        """
        Fetch labels for a specified wallet address.

        :param address: str, wallet address to query
        :param blockchain: str, blockchain type, defaults to 'ethereum'
        :param offset: int, pagination offset, defaults to 0
        :param limit: int, number of items to return, defaults to 30
        :return: dict, the JSON response containing wallet labels
        """
        url = f"{self.base_url}/wallet/label?address={address}&blockchain={blockchain}&offset={offset}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Failed to fetch wallet labels: {str(e)}")
