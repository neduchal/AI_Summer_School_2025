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

def call_openai_api(
        client, 
        image_path, 
        command,
        prompt
    ):
    ret = None

    # OpenAI API call

    return ret


# KKY_OLLAMA_SERVER = 'https://ollama.kky.zcu.cz'
def call_kky_ollama_api(
        client, 
        image_path, 
        command,
        prompt,
        model='gemma3:27b'
    ):

    ret = None

    # KKY ollama API call

    return ret

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
