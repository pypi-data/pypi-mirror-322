from .completions import Completions

class Data:
    def __init__(self, client):
        """
        Initialize the Data client.
        
        :param client: API client instance
        """
        self._client = client

    def upload(self, text_data: str, prompt_id: str):
        """
        Upload a file to the data store.
        
        :param file_path: Path to the file to upload
        """
        self._client.post_direct('http://localhost:8081/import/from_text', {'prompt_dataset': text_data, 'prompt_id': prompt_id})
    
    def retrieve(self,  prompt_id: str, search_string: str):
        """
        Retrieve data from the data store.
        
        :param search_string: String to search for
        """
        return self._client.post_direct('http://localhost:8081/search/from_prompt', {'prompt_id': prompt_id, 'user_input': search_string})