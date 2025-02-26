import os


class TemplateParser:
    def __init__(self, default: str = "en"):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default = default
        self.language = default

    def set_language(self, language: str):
        language_path = os.path.join(self.current_path, "locales", language)
        if os.path.exists(language_path):
            self.language = language

    def get(self, group: str, key: str, vars: dict = {}):
        group_path = os.path.join(
            self.current_path, "locales", self.language, f"{group}.py"
        )
        target_lang = self.language

        if not os.path.exists(group_path):
            group_path = os.path.join(
                self.current_path, "locales", self.default, f"{group}.py"
            )
            target_lang = self.default

        if not os.path.exists(group_path):
            return None

        module = __import__(
            f"src.bots.templates.locales.{target_lang}.{group}",
            fromlist={group},
        )

        if not module:
            return None

        key_attr = getattr(module, key)
        return key_attr.substitute(vars)
