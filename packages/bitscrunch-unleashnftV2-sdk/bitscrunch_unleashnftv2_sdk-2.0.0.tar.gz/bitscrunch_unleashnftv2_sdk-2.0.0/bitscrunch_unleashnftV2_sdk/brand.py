import requests
from .exceptions import APIError

class NFT_Brand:
    def __init__(self, api_key: str):
        """Initialize the SDK with the API key."""
        self.api_key = api_key
        self.base_url = "https://api.unleashnfts.com/api/v2/nft/brand"

    def get_brand_metadata(self, blockchain: str = "ethereum", brand: list = None, offset: int = 0, limit: int = 30) -> dict:
        """Retrieve metadata for an NFT brand, including brand details, visuals, supported blockchains, and social media."""
        if brand is None:
            brand = []  # Default empty brand array
        params = {
            "blockchain": blockchain,
            "brand": ",".join(brand),  # Convert list to a comma-separated string
            "offset": offset,
            "limit": limit
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/metadata", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand metadata: {e}")

    def get_brand_metrics(
        self,
        blockchain: str = "ethereum",
        brand: list = None,
        time_range: str = "24h",
        offset: int = 0,
        limit: int = 30,
        sort_by: str = "mint_tokens",
        sort_order: str = "desc",
    ) -> dict:
        """
        Retrieve detailed metrics for an NFT brand, providing insights into key performance indicators.
        """
        if brand is None:
            brand = []  # Default empty brand array
        params = {
            "blockchain": blockchain,
            "brand": ",".join(brand),  # Convert list to a comma-separated string
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/metrics", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand metrics: {e}")


    def get_brand_profile(
        self,
        blockchain: str = "ethereum",
        brand: list = None,
        time_range: str = "24h",
        offset: int = 0,
        limit: int = 30,
        sort_by: str = "diamond_hands",
        sort_order: str = "desc",
    ) -> dict:
        """
        Retrieve profile information for an NFT brand, including key metrics and trading insights.
        """
        if brand is None:
            brand = []  # Default empty brand array
        params = {
            "blockchain": blockchain,
            "brand": ",".join(brand),  # Convert list to a comma-separated string
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/profile", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand profile: {e}")


    def get_brand_contract_metadata(
        self,
        blockchain: str = "ethereum",
        contract_address: list = None,
        offset: int = 0,
        limit: int = 30,
    ) -> dict:
        """
        Retrieve comprehensive metadata for an NFT brand, including key information 
        such as brand name, category, description, thumbnail URL, supported blockchains, 
        and social media URLs.
        """
        if contract_address is None:
            contract_address = []  # Default empty contract address array
        params = {
            "blockchain": blockchain,
            "contract_address": ",".join(contract_address),  # Convert list to a comma-separated string
            "offset": offset,
            "limit": limit,
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/contract_metadata", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand contract metadata: {e}")


    def get_brand_contract_metrics(
        self,
        blockchain: str = "ethereum",
        contract_address: list = None,
        time_range: str = "24h",
        offset: int = 0,
        limit: int = 30,
        sort_by: str = "mint_tokens",
        sort_order: str = "desc",
    ) -> dict:
        """
        Retrieve detailed contract metrics for an NFT brand, including contract-level
        performance and activity.
        """
        if contract_address is None:
            contract_address = []  # Default empty contract address array
        params = {
            "blockchain": blockchain,
            "contract_address": ",".join(contract_address),  # Convert list to a comma-separated string
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/contract_metrics", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand contract metrics: {e}")
        


    def get_brand_contract_profile(
        self,
        blockchain: str = "ethereum",
        contract_address: list = None,
        time_range: str = "24h",
        offset: int = 0,
        limit: int = 30,
        sort_by: str = "diamond_hands",
        sort_order: str = "desc",
    ) -> dict:
        """
        Retrieve profile information for an NFT brand contract, providing insights into
        engagement and trading characteristics.
        """
        if contract_address is None:
            contract_address = []  # Default empty contract address array
        params = {
            "blockchain": blockchain,
            "contract_address": ",".join(contract_address),  # Convert list to a comma-separated string
            "time_range": time_range,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/contract_profile", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand contract profile: {e}")


    def get_brand_category(
        self,
        blockchain: str = "ethereum",
        category: list = None,
        offset: int = 0,
        limit: int = 30,
    ) -> dict:
        """
        Retrieve category information for an NFT brand, providing insights into its
        classification, blockchain, and relevant metadata.
        """
        if category is None:
            category = []  # Default empty category array
        params = {
            "blockchain": blockchain,
            "category": ",".join(category),  # Convert list to a comma-separated string
            "offset": offset,
            "limit": limit,
        }
        headers = {"accept": "application/json", "x-api-key": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/category", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"Error fetching brand category information: {e}")
