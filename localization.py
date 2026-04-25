import os
import yaml


class Localization:
    _cache = {}

    def __init__(self, locales_dir="localization", default_lang="ru"):
        self.locales_dir = locales_dir
        self.default_lang = default_lang
        self.current_lang = default_lang

        self.translations = self._load(default_lang)
        self.default_translations = self.translations

    def _load(self, lang):
        if lang in self._cache:
            return self._cache[lang]

        path = os.path.join(self.locales_dir, f"{lang}.yml")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Language file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        self._cache[lang] = data
        return data

    def set_language(self, lang):
        self.translations = self._load(lang)
        self.current_lang = lang

    def t(self, key, **kwargs):

        text = self.translations.get(key)

        if text is None:
            text = self.default_translations.get(key, f"[{key}]")

        if kwargs and isinstance(text, str):
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError, IndexError):
                pass
        return text
