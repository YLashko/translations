import json
from copy import copy

class InvalidSetupError(Exception):
    pass

class TranslationError(Exception):
    pass

class NoLanguageDataError(Exception):
    pass

class Translations:

    def __init__(self) -> None:
        self.language_codes: list[str] = []
        self.users_languages: dict = {}
        self.default_language: str = ""
        self.translations: dict = {}
    

    def get_translations_from_json(self, json_str: str):
        """
            Get translations from a JSON string
        """
        data = json.loads(json_str)
        self.translations = data

        self.language_codes = list(self.translations.keys())


    def set_default_language(self, language: str):
        """
            Set default language, it is used if there is no translation 
            data for the specific message in another language.
        """
        if not language in self.language_codes:
            raise InvalidSetupError("You need to provide translations data first! use get_translations_from_json()")
        self.default_language = language


    def __getitem__(self, key: str) -> dict:
        if key not in list(self.translations.keys()):
            raise NoLanguageDataError(f"There is no translations for language '{key}'")
        return self.translations[key]


    def call_translation(self, language, phrase, *args):

        def set_variables(message: str, var_names, var_values):
            out = copy(message)
            for i in range(min(len(var_names), len(var_values))):
                out = out.replace("{" + var_names[i] + "}", var_values[i])
            return out

        translations_for_lang = self[language]
        if phrase not in list(translations_for_lang.keys()):
            raise NoLanguageDataError(f"There is no translation for message {phrase} in '{language}'")
        out_message = set_variables(
            message=translations_for_lang[phrase]["phrase"],
            var_names=translations_for_lang[phrase]["variables"],
            var_values=args
        )
        return out_message
    

    def t_lang(self, language: str, phrase: str, *args):
        """
            Translate using a language specified for user_id
        """
        if language not in self.language_codes:
            raise NoLanguageDataError(f"There is no translations for language '{language}'")
        
        try: # first, try selected language
            translation = self.call_translation(
                language,
                phrase,
                *args
            )
            return translation
        
        except Exception: # if error, try the default language
            try:
                translation = self.call_translation(
                    self.default_language,
                    phrase,
                    *args
                )
                return translation
            except Exception:
                return phrase


    def t_id(self, user_id, phrase: str, *args):
        """
            Translate using a language specified for user_id
        """
        if self.users_languages == {}:
            raise InvalidSetupError("You must first add a user using add_user()")
        if not user_id in list(self.users_languages.keys()):
            raise NoLanguageDataError(f"No language data for user {user_id}")
        return self.t_lang(
            self.users_languages[user_id],
            phrase,
            *args
        )
    

    def toggle_language(self, user_id: str | int) -> str:
        if user_id not in list(self.users_languages.keys()):
            raise NoLanguageDataError(f"There is no language specification for {user_id}")
        
        index_ = self.language_codes.index(self.users_languages[user_id])
        index_ = (index_ + 1) % len(self.language_codes)
        self.users_languages[user_id] = self.language_codes[index_]
        return self.users_languages[user_id]


    def add_user(self, user_id, language = None):

        if len(self.language_codes) == 0:
            raise InvalidSetupError("You must first set the translations data! Use get_translations_from_json()")
        if language not in self.language_codes:
            raise NoLanguageDataError(f"Can not set language to {language}: this language is not on the available languages list")
        
        if language:
            self.users_languages[user_id] = language
    

    def set_users_languages(self, language_dict): 
        self.users_languages = language_dict
