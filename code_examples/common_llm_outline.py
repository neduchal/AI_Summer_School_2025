import base64
from pydantic import BaseModel
from openai import OpenAI
from ollama import Client
from enum import Enum
from typing import Optional
from httpx import DigestAuth
import json

class Colors(str, Enum):
    property = 'property' # placeholder. Replace with actual values.


class Shapes(str, Enum):
    property = 'property' # placeholder. Replace with actual values.

class AnswerLLM(BaseModel):
    response: str
    # property: Optional[Property] # placeholder. Replace with actual values.

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_openai_api(
        client, 
        image, 
        command,
        prompt
    ):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        temperature=0,
        messages=[
            {
                "role": "developer", 
                "content": prompt
            },
            {
                "role": "user",
                "content": [
                    {
                      "type": "text",
                      "text": command
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{image}"
                      }
                    }
                ]
            }
        ],
        response_format=AnswerLLM,
    )

    return completion.choices[0].message.parsed


# KKY_OLLAMA_SERVER = 'https://ollama.kky.zcu.cz'
def call_kky_ollama_api(
        client, 
        image, 
        command,
        prompt,
        model='gemma3:27b'
    ):

    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": prompt
            },
            {
                "role": "user",
                "content": command,
                'images': [image]
            },
        ],
        format=AnswerLLM.model_json_schema(),        
    )
    return response.message.content

def call_llm(image, command, prompt, openai=True, openai_api_key=None,
             kky_ollama_uname=None, kky_ollama_password=None, kky_ollama_server=None):

    answer_dict = {}

    if openai:
        # OpenAI API
        client = OpenAI(api_key=openai_api_key)

        answer = call_openai_api(
            client,
            image_path=image,
            command=command,
            prompt=prompt
        )

        answer_dict = answer.__dict__
    else:
        # KKY ollama server
        client = Client(
            host=kky_ollama_server,
            auth=DigestAuth(
                kky_ollama_uname, 
                kky_ollama_password
            ),
        )

        answer = call_kky_ollama_api(
            client,
            image_path=image,
            command=command,
            prompt=prompt
        )
        answer_dict = json.loads(answer)

    return answer_dict
