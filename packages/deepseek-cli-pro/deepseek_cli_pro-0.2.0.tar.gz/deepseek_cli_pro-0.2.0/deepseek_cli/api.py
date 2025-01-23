from openai import OpenAI
from typing import Generator

class DeepSeekClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
    
    def chat_completion(self, messages, model="deepseek-chat", **kwargs):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
    
    def stream_response(self, messages, model="deepseek-chat", **kwargs):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            **kwargs
        )