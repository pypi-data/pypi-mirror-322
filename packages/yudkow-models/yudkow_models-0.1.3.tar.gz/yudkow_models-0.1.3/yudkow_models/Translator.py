from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES, MY_MEMORY_LANGUAGES_TO_CODES
from deep_translator import GoogleTranslator


class MyTranslator:
    def __init__(self, native="russian", foreign="english"):
        self.to_native = GoogleTranslator(source=GOOGLE_LANGUAGES_TO_CODES.get(foreign),
                                          target=GOOGLE_LANGUAGES_TO_CODES.get(native))
        self.to_foreign = GoogleTranslator(source=GOOGLE_LANGUAGES_TO_CODES.get(native),
                                           target=GOOGLE_LANGUAGES_TO_CODES.get(foreign))

    def translate(self, text: str, to: str) -> str:
        if to == "native":
            return self.to_native.translate(text)
        elif to == "foreign":
            return self.to_foreign.translate(text)