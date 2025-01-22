from typing import Dict, Optional, List, Any
from pydantic import TypeAdapter
from ..utils.response_format import type_to_response_format_param
import json
class Completions:
    def __init__(self, client):
        """
        Initialize the Completions client.
        
        :param client: API client instance
        """
        self._client = client

    def create(self, 
               prompt_id: str, 
               variables: Optional[Dict[str, Any]] = None, 
               messages: Optional[List[Dict[str, Any]]] = None,
               chain_id: str = None,
               metadata: Optional[Dict[str, Any]] = None,
               tags: Optional[List[str]] = None,
               response_format: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a chat completion.
        
        :param prompt_id: Identifier for the prompt
        :param variables: Optional dictionary of variables
        :param messages: Optional list of message dictionaries
        :return: Chat completion response
        """
        input_data = {'prompt_id': prompt_id}
        
        if variables:
            input_data['variables'] = variables

        if chain_id:
            input_data['chain_id'] = chain_id

        if metadata:
            input_data['metadata'] = metadata
        
        if messages:
            input_data['messages'] = messages

        if tags:
            input_data['tags'] = tags

        if response_format:
            input_data['response_format'] = type_to_response_format_param(response_format)

        response = self._client.post('/v1/chat/completions', input_data)

        if response_format:
            response = TypeAdapter(response_format).validate_json(response['text'])

        return response
