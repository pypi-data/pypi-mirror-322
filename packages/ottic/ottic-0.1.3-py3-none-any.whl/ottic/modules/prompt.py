from typing import Dict, Optional, Any

class Prompt:
    def __init__(self, client):
        """
        Initialize the Prompt client.
        
        :param client: API client instance
        """
        self._client = client

    def render(self, prompt_id: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Render a prompt with optional variables.
        
        :param prompt_id: Identifier for the prompt
        :param variables: Optional dictionary of variables for the prompt
        :return: Prompt render response
        """
        data = {'variables': variables} if variables else {}
        response = self._client.post(f'/v1/prompts/{prompt_id}/render', data)
        return response