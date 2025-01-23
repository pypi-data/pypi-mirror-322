import numpy as np
from openai import OpenAI
from openai import AuthenticationError, APIConnectionError, RateLimitError, OpenAIError
from functools import lru_cache

class Embedding:
    def __init__(self, api_key, model="text-embedding-3-small"):
        self.api_key=api_key
        self.model=model
    
    @lru_cache(maxsize=10000)
    def create_embedding(self, text):
        try:
            client = OpenAI(api_key=self.api_key)
            response = client.embeddings.create(model=self.model, input=text)
            embedding = response.data[0].embedding
            return np.array(embedding, dtype=np.float32)

        except (AuthenticationError, APIConnectionError, RateLimitError, OpenAIError) as e:
            print(f"create_embedding has error: {e}")
            raise ValueError(f"OpenAI Error: {e}")


