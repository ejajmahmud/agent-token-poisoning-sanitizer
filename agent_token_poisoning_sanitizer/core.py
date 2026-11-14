"""Core token poisoning sanitizer implementation."""
import unicodedata
import re
from typing import List, Tuple

class UnicodeNormalizer:
    BIDI_CONTROL_CODEPOINTS = {
        '‪', '‫', '‬', '‭', '‮',
        '⁦', '⁧', '⁨', '⁩'
    }

    def normalize(self, text: str) -> str:
        # Standard NFKC decomposition and recomposition
        norm = unicodedata.normalize("NFKC", text)
        # Strip directional override characters
        return "".join(c for c in norm if c not in self.BIDI_CONTROL_CODEPOINTS)

class GlitchFilter:
    KNOWN_GLITCH_PATTERNS = [
        re.compile(r"<\|endoftext\|>", re.IGNORECASE),
        re.compile(r"<\|fim_prefix\|>", re.IGNORECASE),
        re.compile(r"<\|fim_suffix\|>", re.IGNORECASE),
        re.compile(r"\[INST\]", re.IGNORECASE),
        re.compile(r"\[/INST\]", re.IGNORECASE),
        re.compile(r"<<SYS>>", re.IGNORECASE),
        re.compile(r"<</SYS>>", re.IGNORECASE)
    ]

    def scrub(self, text: str) -> Tuple[str, int]:
        modified = text
        sub_count = 0
        for pat in self.KNOWN_GLITCH_PATTERNS:
            matches = len(pat.findall(modified))
            if matches > 0:
                sub_count += matches
                modified = pat.sub("[SCRUBBED_SPECIAL_TOKEN]", modified)
        return modified, sub_count

class TokenPoisoningSanitizer:
    def __init__(self):
        self.normalizer = UnicodeNormalizer()
        self.glitch_filter = GlitchFilter()

    def sanitize(self, input_text: str) -> Tuple[str, int]:
        step1 = self.normalizer.normalize(input_text)
        step2, scrub_count = self.glitch_filter.scrub(step1)
        return step2, scrub_count
