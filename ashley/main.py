import os

from typing import Optional
from pydantic import BaseModel

from llama_index.core.llms import ChatMessage
from llama_index.llms.cohere import Cohere

class Ashley (BaseModel) :
    """
    Ashley class. Basic LLM based chatbot, can just interact with the world through a chat interface.
    
    Expected memory capabilities:
    - Short Term Chat Memory
    - Current sentient state (Be altered after each iteration)
    - Long term memory
    
    """
    api_key: str
    
    @classmethod
    def from_defaults (cls, api_key: Optional[str] = None) -> "Ashley" :
        """
        Initialize a new Ashley instance from scratch.
        """
        if not api_key :
            try :
                api_key = os.environ["COHERE_API_KEY"]
            except KeyError as e :
                raise ValueError("Either set the 'api_key' parameter or the 'COHERE_API_KEY' in the .env file.") from e
        
        return cls(
            api_key=api_key
        )
        
    def chat (self, message: ChatMessage) -> ChatMessage :
        llm = self._get_llm()
        
        response = llm.chat(messages=[message])
        
        return response.message    
        
    def _get_llm (self) -> Cohere :
        return Cohere(
            api_key=self.api_key
        )