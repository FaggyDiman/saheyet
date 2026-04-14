import json
import os


class Localization:
    def __init__(self, locales_dir="localization", default_lang="ru"):
        self.locales_dir = locales_dir
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.translations = {}

        self.load_language(default_lang)

    def load_language(self, lang):
        path = os.path.join(self.locales_dir, f"{lang}.json")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Language file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

        self.current_lang = lang

    def set_language(self, lang):
        self.load_language(lang)

    def get(self, key, **kwargs):
        text = self.translations.get(key)

        if text is None:
            # fallback
            default_path = os.path.join(self.locales_dir, f"{self.default_lang}.json")
            with open(default_path, "r", encoding="utf-8") as f:
                default_translations = json.load(f)
            text = default_translations.get(key, key)

        try:
            return text.format(**kwargs)
        except Exception:
            return text
