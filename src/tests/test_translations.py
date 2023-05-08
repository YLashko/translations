from pytranslations import translations

def test_no_users():
    tr = translations.Translations()
    with open("src/tests/test_data.json", 'r') as f:
        tr.get_translations_from_json(f.read())
    tr.default_language = "en"
    assert tr.t_lang("ru", "translation_1", "abc", "cde") == "Result abc abc phrase cde ru"
    assert tr.t_lang("ru", "translation_3", "abc") == "Result phrase abc en 3"

def test_users():
    tr = translations.Translations()
    with open("src/tests/test_data.json", 'r') as f:
        tr.get_translations_from_json(f.read())
    tr.default_language = "en"
    tr.add_user("1", "en")
    tr.add_user("2", "en")
    tr.add_user("3", "ru")
    assert tr.t_id("3", "translation_3", "qweqwe") == "Result phrase qweqwe en 3"
    
