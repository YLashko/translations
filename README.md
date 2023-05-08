# Translations

## Setup

```
pip install pytranslations
```

## Usage


```python
from pytranslations import Translations

translations = Translations()
```

First, you need to import the translations file


```python 
with open("translations.json", "r") as tr_file:
    translations.get_translations_from_json(tr_file.read())
```

#### Example translations file

translations.json 
```json
{
    "en": {
        "hello": {
            "phrase": "Hello {name}",
            "variables": ["name"]
        },

        "mynameis": {
            "phrase": "Hello {companion}! My name is {name}.",
            "variables": ["companion", "name"]
        }
    },

    "fr": {
        "hello": {
            "phrase": "Bonjour {name}",
            "variables": ["name"]
        }
    }
}
```

Then you can use `t_lang()` to translate phrase to the specified language. For example, 

```python
translations.t_lang("en", "mynameis", "John", "Bob")
```
will output `Hello John! My name is Bob.`

you can also set the `set_default_language()`. The default language is used when there is no translations for the specified one in `t_lang()`. Now, with the default language set to "en", let's try translating "mynameis" phrase to french.

```python
translations.t_lang("fr", "mynameis", "John", "Bob")
``` 
This will output `Hello John! My name is Bob.`, because there is no translation in the french dictionary for the phrase "mynameis".

You can also add users to track their specified language using `add_user(user_id, language)`

```python
translations.add_user("user_1", "en")
```

Then you can call `t_id()` to translate the phrase for the specific user.

```python
translations.t_id("user_1", "hello", "Bob")
```
will output `Hello Bob`.

