import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url="https://api.proxyapi.ru/openai/v1"  # This is the default and can be omitted
)

text_for_ai = '''напиши тест'''

print(f'Проверка корректности работы переменной {text_for_ai}')


chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{text_for_ai}",
        }
    ],
    model="gpt-4o",
)

print(chat_completion.choices[0].message.content)

