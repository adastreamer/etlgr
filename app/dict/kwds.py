import langs

ALL_LANGS = langs.__all__

KWDS = {}

for lang_code in ALL_LANGS:
    lang_module = ALL_LANGS[lang_code]

    # insert the languages names into the related sections
    lang_names_section_key = langs.postfixed_lang(lang_code)
    lang_names_section = KWDS.get(lang_names_section_key, {})
    KWDS[lang_names_section_key] = lang_names_section
    for l_code in ALL_LANGS:
        KWDS[lang_names_section_key][l_code] = lang_module.LANG_NATIVE_NAME

    # insert the main values
    for phrase_key in lang_module.KWDS:
        possible_existing_value = KWDS.get(phrase_key)
        if not possible_existing_value:
            KWDS[phrase_key] = {}
        KWDS[phrase_key][lang_code] = lang_module.KWDS[phrase_key]

