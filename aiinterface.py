import os
from openai import OpenAI
from typing import Optional

class OpenAIWrapper:
    """
    A wrapper class for the OpenAI API client that stores API key and custom base URL
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        base_url: str = "https://api.proxyapi.ru/openai/v1"
    ):
        """
        Initialize the OpenAI wrapper with API key and optional base URL
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, will try to get from environment
            base_url (str, optional): Custom base URL for API requests
        """
        # Use provided API key or fall back to environment variable
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key must be provided either directly or through OPENAI_API_KEY environment variable")
            
        self.base_url = base_url
        
        # Initialize the OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def request_to_ai(self, text_for_ai: str) -> str:
        """
        Send a request to the OpenAI API
        
        Args:
            text_for_ai (str): The text prompt to send to the AI
            
        Returns:
            str: The AI's response content
            
        Raises:
            Exception: If there's an error in making the API request
        """
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": text_for_ai,
                    }
                ],
                model="gpt-4o",
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            error_msg = f'Error in OpenAI API request: {str(e)}'
            print(error_msg)
            raise Exception(error_msg)

# Example usage:
if __name__ == "__main__":
    # Example 1: Using environment variable for API key
    ai_client = OpenAIWrapper()
    
    # Example 2: Providing API key directly
    # ai_client = OpenAIWrapper(api_key="your-api-key-here")
    
    try:
        response = ai_client.request_to_ai("Hello, how are you?")
        print(response)
    except Exception as e:
        print(f"Failed to get response: {e}")
