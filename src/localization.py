"""Card name localization module for Japanese language support."""

import json

from src import constants
from src.logger import create_logger

logger = create_logger()

# Global state
_card_name_mapping: dict = {}
_current_language: str = constants.LANGUAGE_DEFAULT


def load_card_name_mapping(file_path: str = constants.TRANSLATION_FILE) -> bool:
    """Load English-to-Japanese card name mapping from JSON file.

    This should be called once at application startup.

    Args:
        file_path: Path to the translation JSON file.

    Returns:
        True if mapping was loaded successfully, False otherwise.
    """
    global _card_name_mapping
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _card_name_mapping = json.load(f)
        logger.info(f"Loaded {len(_card_name_mapping)} Japanese card names")
        return True
    except FileNotFoundError:
        logger.warning(f"Translation file not found: {file_path}")
        _card_name_mapping = {}
        return False
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse translation file: {e}")
        _card_name_mapping = {}
        return False


def set_language(language: str) -> None:
    """Set the current display language.

    Args:
        language: Language code (EN or JP).
    """
    global _current_language
    if language in constants.LANGUAGE_OPTIONS:
        _current_language = language
        logger.info(f"Display language set to: {language}")


def get_language() -> str:
    """Get the current display language.

    Returns:
        Current language code (EN or JP).
    """
    return _current_language


def get_display_card_name(english_name: str) -> str:
    """Get the display name for a card based on current language setting.

    Args:
        english_name: The English card name.

    Returns:
        Japanese name if language is JP and mapping exists,
        otherwise returns the English name.
    """
    if _current_language == constants.LANGUAGE_EN:
        return english_name

    # Return Japanese name if available, fallback to English
    return _card_name_mapping.get(english_name, english_name)


def is_translation_available() -> bool:
    """Check if translation mapping is loaded and available.

    Returns:
        True if translation mapping is loaded with at least one entry.
    """
    return len(_card_name_mapping) > 0
