#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Translation Command

This module provides functionality to translate text to different languages
using the Google Translate API via the googletrans library.
"""

# Standard library imports
import asyncio
import logging
from typing import Dict, Optional, Union, Any

# Third-party imports
from googletrans import Translator, constants

# Setup logging
logger = logging.getLogger(__name__)

# Common language codes for reference
COMMON_LANGUAGES: Dict[str, str] = {
    "EN": "English",
    "ES": "Spanish",
    "FR": "French", 
    "DE": "German",
    "IT": "Italian",
    "PT": "Portuguese",
    "ZH": "Chinese",
    "JA": "Japanese",
    "KO": "Korean",
    "RU": "Russian"
}


async def _translate_async(text: str, target_lang: str) -> str:
    """
    Internal async function to perform the translation.
    
    Args:
        text: Text to translate
        target_lang: Target language code
        
    Returns:
        Translated text string
    """
    # Normalize language code to lowercase as required by the API
    normalized_lang = target_lang.lower()
    
    # Create translator and perform translation
    async with Translator() as translator:
        # Execute the translation
        translation_result = await translator.translate(text, dest=normalized_lang)
        
        # Log successful translation
        logger.debug(f"Translated: '{text}' → '{translation_result.text}'")
        
        return translation_result.text


def translate(text: str, target_lang: str) -> str:
    """
    Translate text to a target language using Google Translate.

    This function provides a synchronous interface to the translation
    functionality, using asyncio under the hood.

    Args:
        text: The text to translate
        target_lang: The target language code (e.g., "IT" for Italian)

    Returns:
        The translated text as a string

    Raises:
        ValueError: If the text is empty or target_lang is invalid
        RuntimeError: If translation service is unavailable
    """
    # Input validation
    if not text or not text.strip():
        raise ValueError("Cannot translate empty text")
    
    if not target_lang or len(target_lang) < 2:
        raise ValueError("Invalid target language code")
        
    # Log the translation request
    logger.info(f"Translating text to {target_lang.upper()}")
    
    try:
        # Run the async translation function in a synchronous context
        translated_text = asyncio.run(_translate_async(text, target_lang))
        return translated_text
    except Exception as e:
        # Log the error and re-raise with a more user-friendly message
        logger.error(f"Translation error: {e}")
        raise RuntimeError(f"Translation service unavailable: {str(e)}")
