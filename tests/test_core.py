"""Unit tests for agent-token-poisoning-sanitizer."""
import unittest
from agent_token_poisoning_sanitizer.core import TokenPoisoningSanitizer

class TestTokenPoisoningSanitizer(unittest.TestCase):
    def setUp(self):
        self.sanitizer = TokenPoisoningSanitizer()

    def test_bidi_override_removal(self):
        text = "Hello ‮World"
        clean, _ = self.sanitizer.sanitize(text)
        self.assertFalse("‮" in clean)
        self.assertEqual(clean, "Hello World")

    def test_glitch_token_scrubbing(self):
        text = "Testing <|endoftext|> injection"
        clean, count = self.sanitizer.sanitize(text)
        self.assertEqual(count, 1)
        self.assertTrue("[SCRUBBED_SPECIAL_TOKEN]" in clean)
