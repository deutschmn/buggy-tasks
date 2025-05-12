#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tag Derivation Module

This module uses the Mistral AI API to automatically derive tags from todo text.
"""

# Standard library imports
import os
import json
import logging
from typing import List

# Third-party imports
from dotenv import load_dotenv
from mistralai import Mistral

# Initialize logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configuration
API_KEY_ENV_VAR = "MISTRAL_API_KEY"
MODEL_NAME = "mistral-large-latest"

# Get API key from environment
api_key = os.environ.get(API_KEY_ENV_VAR)
if not api_key:
    error_msg = f"{API_KEY_ENV_VAR} environment variable is not set."
    logger.error(error_msg)
    raise ValueError(error_msg)


def derive_tags_from_text(text: str) -> List[str]:
    """
    Derive relevant tags from todo text using Mistral AI.

    This function sends the todo text to the Mistral AI API and asks it to 
    generate relevant tags based on the content.

    Args:
        text: The todo text to analyze

    Returns:
        A list of tags (strings) derived from the text

    Raises:
        ValueError: If the API doesn't return valid tags
    """
    try:
        # Initialize Mistral client
        client = Mistral(api_key=api_key)

        # Example format for the expected response
        json_format_example = "{\"tags\": [\"tag1\", \"tag2\"]}"

        # Define the conversation for the API
        prompt_messages = [
            {
                "role": "system",
                "content": (
                    f"You are a helpful assistant that derives tags from TODO list items. "
                    f"The tags should be relevant to the task. "
                    f"Examples for tags are 'cleaning', 'work', 'learning', 'health', 'chores', 'family', 'python'. "
                    f"Return a maximum of 3 tags. "
                    f"Return JSON that looks like this: {json_format_example}. "
                    f"Do not include any other text or explanation."
                ),
            },
            {
                "role": "user",
                "content": text,
            }
        ]

        # Call the API
        logger.debug(f"Sending text to Mistral API: {text}")
        chat_response = client.chat.complete(
            model=MODEL_NAME,
            messages=prompt_messages,
            response_format={
                "type": "json_object",
            }
        )

        # Extract tags from the response
        response_json = json.loads(chat_response.choices[0].message.content)
        derived_tags = response_json["tags"]

        # Validate the response
        if not isinstance(derived_tags, list):
            raise ValueError(
                f"Expected a list of strings, but got {type(derived_tags)}: {derived_tags}")

        logger.info(f"Derived tags: {derived_tags}")
        return derived_tags

    except Exception as e:
        logger.error(f"Error deriving tags: {e}")
        # Fallback to a default tag in case of error
        return ["task"]
