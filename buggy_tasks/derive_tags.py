import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable is not set.")
model = "mistral-large-latest"


def derive_tags_from_text(text):
    client = Mistral(api_key=api_key)
    expected_example = "{\"tags\": [\"tag1\", \"tag2\"]}"
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant that derives tags from TODO list items. The tags should be relevant to the task. Don't return too many. Return JSON that looks like this: {expected_example}. Do not include any other text or explanation.",
        },
        {
            "role": "user",
            "content": text,
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
        response_format={
            "type": "json_object",
        }
    )
    tags = json.loads(chat_response.choices[0].message.content)["tags"]

    # check if tags is a list of strings
    if not isinstance(tags, list):
        raise ValueError(
            f"Expected a list of strings, but got {type(tags)}: {tags}"
        )

    return tags
