from .completions import Completions

class Chat:
    def __init__(self, client, data):
        """
        Initialize the Chat client.
        
        :param client: API client instance
        """
        self._client = client
        self.completions = Completions(self._client, data)