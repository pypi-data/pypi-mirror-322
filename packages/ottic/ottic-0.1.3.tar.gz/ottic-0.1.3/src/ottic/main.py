import os
from typing import Optional

from .client.client import Client
from .constants import OTTIC_URL
from .modules.chat import Chat
from .modules.prompt import Prompt
class OtticAI:
    def __init__(self, api_key: Optional[str] = None, endpoint: str = OTTIC_URL):
        """
        Initialize the OtticAI client.
        
        :param api_key: Optional API key. If not provided, tries to read from environment variable.
        :param endpoint: API endpoint URL
        """
        # Try to get API key from parameter or environment variable
        api_key = api_key or os.getenv('OTTIC_API_KEY')
        
        if not api_key:
            raise ValueError(
                "The OTTIC_API_KEY environment variable is missing. "
                "Either provide it, or instantiate the OtticAI client with an api_key option. "
                "Example: OtticAI(api_key='Your API Key')."
            )
        
        self._client = Client(api_key, endpoint)
        self.prompts = Prompt(self._client)
        self.chat = Chat(self._client)