import os
import re
import openai
from typing import Optional


class OpenAIWrapper:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.proxyapi.ru/openai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = None

    def tryCreateClient(self):
        try:
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        except Exception:
            return False
        return True

    def updateAPIKEY(self, api_key):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def request_to_ai(self, text_for_ai: str, max_retries: int = 5) -> str:
        pattern1 = r"\*\*Characters_names:\s*.*\n*\*\*Location:\s*.*\n*\*\*Main_character:\s*.*\n*\*\*Dialog:\s*.*\n*"
        pattern2 = r"Characters_names:\s*.*\n*Location:\s*.*\n*Main_character:\s*.*\n*Dialog:\s*.*\n"
        for attempt in range(max_retries):
            try:
                response = self._get_ai_response(text_for_ai)
                if self._validate_response(response, pattern1) or self._validate_response(response, pattern2):
                    return response
                print(f"Attempt {attempt + 1}: Response did not match the pattern, retrying...")
            except Exception as e:
                print(f"Error in OpenAI API request: {e}")
                raise
        raise Exception("Failed to get a valid response after multiple attempts")

    def _get_ai_response(self, text_for_ai: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": text_for_ai}],
            model="gpt-4o",
        )
        return chat_completion.choices[0].message.content

    @staticmethod
    def _validate_response(response: str, pattern: str) -> bool:
        return bool(re.search(pattern, response, re.DOTALL))