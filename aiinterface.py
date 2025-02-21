import os
from openai import OpenAI

def request_to_ai (text_for_ai):

	client = OpenAI(
		api_key=os.getenv('OPENAI_API_KEY'),
		base_url="https://api.proxyapi.ru/openai/v1" 
	)
	try:
		chat_completion = client.chat.completions.create(
			messages=[
				{
				    "role": "user",
				    "content": f"{text_for_ai}",
				}
			],
			model="gpt-4o",
		)
	except:
		print('Error in amlibsik code')

	return chat_completion.choices[0].message.content
	

