"""
To identify unicode codes in the markdown content, this hook replaces

U+XXXX with a tag
"""

from xml.etree import ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

BASE_URL = "https://symbl.cc"

class UnicodeProcessor(InlineProcessor):
    def __init__(self, pattern, md, language="en"):
        super().__init__(pattern, md)
        self.language = language

    def handleMatch(self, m, data):
        unicode_code = m.group(1)
        el = etree.Element("a")
        el.set("href", f"{BASE_URL}/{self.language}/{unicode_code}")
        el.set("class", "ycr-pill ycr-unicode")
        el.set("target", "_blank")
        el.text = f"{unicode_code}"
        return el, m.start(0), m.end(0)

    def set_language(self, language):
        self.language = language


class UnicodeExtension(Extension):
    def __init__(self, language='en'):
        self.language = language

    def extendMarkdown(self, md):
        UNICODE_RE = r"\bU\+([0-9A-F]{4,5})\b"
        unicode_pattern = UnicodeProcessor(UNICODE_RE, md, self.language)
        md.inlinePatterns.register(unicode_pattern, "unicode", 175)
