import json
from typing import Union
from huggingface_hub import InferenceClient
from core.config_parser import read_config

config = read_config(filepath='core/config.cfg')
provider = config['provider']
api_key = config['hf_token']
model = config['model']


client = InferenceClient(
    provider=provider,
    api_key=api_key,
)


def get_chat_completion(prompt: str) -> dict:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    response: Union[str, None] = completion.choices[0].message.content

    if response is None:
        raise ValueError("API response none")
    cleaned = response.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)
