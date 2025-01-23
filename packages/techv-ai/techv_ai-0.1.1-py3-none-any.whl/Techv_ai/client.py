import os
from groq import Groq

class TechV_AIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in the GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=self.api_key)

    def get_client(self):
        return self.client
