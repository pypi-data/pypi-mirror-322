import requests

class Client:
    def __init__(self, api_key: str, endpoint: str):
        """
        Initialize the Ottic API client.
        
        :param api_key: API key for authentication
        :param endpoint: Base endpoint URL
        """
        self._api_key = api_key
        self._endpoint = endpoint
        self._session = requests.Session()

    def _get_headers(self):
        """
        Generate standard headers for API requests.
        
        :return: Dictionary of headers
        """
        return {
            'Content-Type': 'application/json',
            'x-ottic-api-key': self._api_key,
            'x-ottic-sdk-version': '0.0.30'  # Replace with actual version
        }

    def post(self, url: str, data: dict = None):
        """
        Perform a POST request to the specified URL.
        
        :param url: Endpoint URL path
        :param data: Optional request payload
        :return: Response data
        """
        try:
            full_url = f"{self._endpoint}{url}"
            response = self._session.post(
                full_url, 
                json=data, 
                headers=self._get_headers()
            )
            response.raise_for_status()  # Raise an exception for bad responses
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Error post request: {str(error)}")
        
    def post_direct(self, url: str, data: dict = None):
        """
        Perform a POST request to the specified URL.
        
        :param url: Endpoint URL path
        :param data: Optional request payload
        :return: Response data
        """
        print(url)
        try:
            full_url = f"{url}"
            response = self._session.post(
                full_url, 
                json=data, 
            )
            response.raise_for_status()  # Raise an exception for bad responses
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Error post request")        

    def get(self, url: str):
        """
        Perform a GET request to the specified URL.
        
        :param url: Endpoint URL path
        :return: Response data
        """
        try:
            full_url = f"{self._endpoint}{url}"
            response = self._session.get(
                full_url, 
                headers=self._get_headers()
            )
            response.raise_for_status()  # Raise an exception for bad responses
            return response.json()
        except requests.RequestException as error:
            raise RuntimeError(f"Error rendering prompt: {str(error)}")