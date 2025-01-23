import requests
from .exceptions import APIError

class NFT_Market_Insights:
    def __init__(self, api_key: str):
        """Initialize the SDK with the API key."""
        self.api_key = api_key
        self.base_url = "https://api.unleashnfts.com/api/v2/nft/market-insights"

    def get_market_analytics(self, blockchain: str = "ethereum", time_range: str = "24h") -> dict:
        """Retrieve NFT market analytics report."""
        url = f"{self.base_url}/analytics"
        params = {"blockchain": blockchain, "time_range": time_range}
        headers = {"accept": "application/json", "x-api-key": self.api_key}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching market analytics: {e}")

    def get_holders_insights(self, blockchain: str = "ethereum", time_range: str = "24h") -> dict:
        """Retrieve aggregated values and trends for NFT holders' metrics."""
        url = f"{self.base_url}/holders"
        params = {"blockchain": blockchain, "time_range": time_range}
        headers = {"accept": "application/json", "x-api-key": self.api_key}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching holders insights: {e}")
    
    def get_scores_insights(self, blockchain: str = "ethereum", time_range: str = "24h") -> dict:
        """Retrieve aggregated values and trends for scores in the NFT market."""
        url = f"{self.base_url}/scores"
        params = {"blockchain": blockchain, "time_range": time_range}
        headers = {"accept": "application/json", "x-api-key": self.api_key}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching scores insights: {e}")

    def get_traders_insights(self, blockchain: str = "ethereum", time_range: str = "24h") -> dict:
        """Retrieve aggregated values and trends for trader metrics in the NFT market."""
        url = f"{self.base_url}/traders"
        params = {"blockchain": blockchain, "time_range": time_range}
        headers = {"accept": "application/json", "x-api-key": self.api_key}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching traders insights: {e}")

    def get_washtrade_insights(self, blockchain: str = "ethereum", time_range: str = "24h") -> dict:
        """Retrieve aggregated values and trends for washtrade metrics in the NFT market."""
        url = f"{self.base_url}/washtrade"
        params = {"blockchain": blockchain, "time_range": time_range}
        headers = {"accept": "application/json", "x-api-key": self.api_key}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching washtrade insights: {e}")
