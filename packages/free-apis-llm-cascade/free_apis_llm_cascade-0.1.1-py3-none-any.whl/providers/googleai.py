from typing import List, Dict, Optional, Union
import asyncio
import os
import google.generativeai as genai

class GoogleaiProvider:
    def __init__(self,
                 googleai_key):
        genai.configure(api_key=googleai_key)

    async def call_googleai(self,
                        model: str,
                        messages: List[Dict[str, str]],
                        max_tokens: Optional[int] = None,
                        temperature: Optional[float] = 1.0,
                        top_p: Optional[float] = 1.0,
                        n: Optional[int] = 1,
                        stream: Optional[bool] = False,
                        stop: Optional[Union[str, List[str]]] = None,
                        presence_penalty: Optional[float] = 0,
                        frequency_penalty: Optional[float] = 0,
                        **kwargs) -> Dict:

        model = genai.GenerativeModel(model)
        response = model.generate_content(messages) # likely needs editing
        return response.text