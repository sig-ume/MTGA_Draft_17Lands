import unittest

from src import constants, localization


class TestLocalization(unittest.TestCase):
    def setUp(self):
        localization.load_card_name_mapping()
        localization.set_language(constants.LANGUAGE_JP)

    def test_basic_translation(self):
        english = "Dazzling Theater // Prop Room"
        translated = localization.get_display_card_name(english)
        self.assertNotEqual(translated, "")
        self.assertNotEqual(translated, english)

    def test_slash_normalization(self):
        canonical = "Dazzling Theater // Prop Room"
        alt = "Dazzling Theater /// Prop Room"
        self.assertEqual(
            localization.get_display_card_name(canonical),
            localization.get_display_card_name(alt),
        )

    def test_english_fallback(self):
        localization.set_language(constants.LANGUAGE_EN)
        english = "Dazzling Theater // Prop Room"
        translated = localization.get_display_card_name(english)
        self.assertEqual(translated, english)


if __name__ == "__main__":
    unittest.main()
