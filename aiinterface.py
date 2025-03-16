import os
import re
import openai
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
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key must be provided either directly or through OPENAI_API_KEY environment variable")
            
        self.base_url = base_url
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def request_to_ai(self, text_for_ai: str, max_retries: int = 5) -> str:
        """
        Send a request to the OpenAI API and ensure the response matches the required pattern
        
        Args:
            text_for_ai (str): The text prompt to send to the AI
            max_retries (int): The maximum number of attempts to get a valid response
        
        Returns:
            str: The AI's response content
        
        Raises:
            Exception: If a valid response is not obtained within max_retries attempts
        """
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
        """
        Internal method to send a request to OpenAI API
        """
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": text_for_ai}],
            model="gpt-4o",
        )
        return chat_completion.choices[0].message.content

    @staticmethod
    def _validate_response(response: str, pattern: str) -> bool:
        """
        Validate if the response matches the given regex pattern
        """
        return bool(re.search(pattern, response, re.DOTALL))

# Example usage:
if __name__ == "__main__":
    ai_client = OpenAIWrapper()
    characters = [item[:-4] for item in os.listdir("Assets/Characters")]
    locations = [item[:-4] for item in os.listdir("Assets/Locations")]
    s = f"""Создай короткую историю на русском в соответствии с этим шаблоном, выбрав случайных персонажней, не давая им имен, и локацию (не меняй шаблон и подписывай говорящих в диалоге):
            Characters_names: {', '.join(characters)}
            Location: {', '.join(locations)}
            Main_character:
            Dialog:"""
    try:
        response = ai_client.request_to_ai(s)
        print(response)
    except Exception as e:
        print(f"Failed to get a valid response: {e}")

''' Пример ответа:
Characters_names: character6, character12, character18, character3, character17  
Location: InsideARichCasino  
Main_character: character6  
Dialog:

В роскошном казино, где свет мерцал от игральных автоматов и звенели монеты, character6 разглядывал залы в поисках удачи.

character12: (наклоняясь ближе) "Сегодня вечер особый, не находишь? Кажется, фортуна на твоей стороне."

character6: (улыбаясь) "Если бы ты знал, как давно я этого жду. Может быть, сегодня всё изменится."

character18: (наблюдая за игрой) "Опасно доверять везению настолько. Главное, оставаться расчётливым."

character3: (мимоходом устраиваясь за соседним столиком) "Ты всегда питаешь оптимизм, character6. Это похвально."

character17: (подмигивая) "Ведь именно оптимизм когда-то завоевал весь этот мир, не так ли?"

character6: "Уверен, что сегодня удача благоволит мне. А если нет, то хотя бы мы хорошо проведем время."

И с этими словами character6 вновь сделал ставку, надеясь, что следующая карта принесёт ему долгожданный выигрыш.
'''