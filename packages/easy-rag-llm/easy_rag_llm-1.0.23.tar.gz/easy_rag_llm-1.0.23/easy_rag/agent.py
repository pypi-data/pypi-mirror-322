import requests
import numpy as np
from openai import OpenAI
import json
import openai

class Agent:
    def __init__(self, embedding_model, model, open_api_key=None, deepseek_api_key=None, deepseek_base_url=None):
        self.model = model
        self.embedding_model = embedding_model
        self.open_api_key = open_api_key
        self.deepseek_api_key = deepseek_api_key
        self.deepseek_base_url = deepseek_base_url
        self.last_prompt = None

    def default_query_embedding_fn(self, query, index_dim): # 테스트용 가짜 임베딩
        return np.random.random(index_dim).astype(np.float32)
    
    def real_query_embedding_fn(self, query, index_dim_f): # 실제 임베딩, dim_f 안씀   
        client = OpenAI(api_key=self.open_api_key)
        response = client.embeddings.create(model=self.embedding_model, input=query)
        embedding = response.data[0].embedding
        return np.array(embedding, dtype=np.float32)

    def generate_response(self, resource, query, return_prompt=False, evidence_num=3):
        index, metadata = resource
        TOP_K = evidence_num
        query_embedding = self.real_query_embedding_fn(query, index.d)
        distances, indices = index.search(query_embedding.reshape(1, -1), TOP_K)
        

        if indices.size == 0 or len(indices[0]) == 0:
            raise ValueError("No relevant evidence found.")

        evidence = [metadata[idx] for idx in indices[0] if idx < len(metadata)]
        if not evidence:
            raise ValueError("No valid evidence found.")

        """ legacy code
        formatted_evidence = "\n".join(
            [f"File: {e['file_name']}, Page: {e['page_number']}, Text: {e['text']}" for e in evidence[:TOP_K]]
        )
        """
        # capsulate with JSON
        formatted_evidence = json.dumps(
            [{"file_name": e['file_name'], "page_number": e['page_number'], "text": e['text']} for e in evidence[:TOP_K]],
            indent=4, ensure_ascii=False
        )


        prompt = f"""
        System: The following is the most relevant information from the Knowledge for your query.
        Given format of the Knowledge is JSON with the following structure:
        {{
            "file_name": "string",
            "page_number": "integer",
            "text": "string"
        }}
        Always answer in the same language as the User prompt and strictly based on the provided Knowledge.
        Do not speculate or create information beyond what is given.
        ==== Knowledge: start ====
        {formatted_evidence}
        ==== Knowledge: end ====

        User: Below is the User prompt:
        ==== User prompt: start ====
        {query}
        ==== User prompt: end ====
        """
        self.last_prompt = prompt.strip()
        if return_prompt:
            print(prompt)
            return self.last_prompt

        if self.model == "deepseek-chat":
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
            }
            try:
                client = OpenAI(api_key=self.deepseek_api_key, base_url=self.deepseek_base_url)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "system", "content": self.last_prompt}],
                    stream=False
                )
                return response.choices[0].message.content, formatted_evidence
            except Exception as e:
                print(f"Error while calling DeepSeek API: {e}")
                raise RuntimeError("DeepSeek API call failed.") from e
        else: # openai model
            client = OpenAI(api_key=self.open_api_key)
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.last_prompt},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=1500,
                    temperature=1.0
                )
                return response.choices[0].message.content, formatted_evidence
            except Exception as e:
                print(f"If you try to use deepseek, check your api_key. If you try to use open ai, Error while calling OpenAI API: {e}")
                raise RuntimeError("If you try to use deepseek, check your api_key. If you try to use open ai, Error while calling OpenAI API") from e


        return "DeepSeek API key not provided. Returning prompt only."

