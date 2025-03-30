import asyncio

from googletrans import Translator


async def _translate(text: str, target_lang: str) -> str:
    async with Translator() as translator:
        result = await translator.translate(text, dest=target_lang.lower())
        return result.text


def translate(text: str, target_lang: str) -> str:
    """Translate text to a target language using Google Translate.

    Args:
        text: The text to translate
        target_lang: The target language code (e.g., "it" for Italian)

    Returns:
        The translated text

    Raises:
        Exception: If translation fails or service is unavailable
    """

    try:
        return asyncio.run(_translate(text, target_lang))
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
