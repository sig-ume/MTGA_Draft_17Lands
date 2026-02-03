import unittest
from src import localization, constants

class TestLocalization(unittest.TestCase):
    def setUp(self):
        # Ensure JP language is set
        localization.set_language(constants.LANGUAGE_JP)
        # Mock mapping if necessary, but we can use real data if it's there
        localization.load_card_name_mapping()

    def test_basic_translation(self):
        # Based on translation.json: "Dazzling Theater // Prop Room": "絢爛たる劇場/小道具部屋"
        name = "Dazzling Theater // Prop Room"
        translated = localization.get_display_card_name(name)
        self.assertEqual(translated, "絢爛たる劇場/小道具部屋")

    def test_slash_normalization(self):
        # Test if /// is normalized to //
        name = "Dazzling Theater /// Prop Room"
        translated = localization.get_display_card_name(name)
        self.assertEqual(translated, "絢爛たる劇場/小道具部屋")

    def test_english_fallback(self):
        localization.set_language(constants.LANGUAGE_EN)
        name = "Dazzling Theater // Prop Room"
        translated = localization.get_display_card_name(name)
        self.assertEqual(translated, name)

if __name__ == "__main__":
    unittest.main()
