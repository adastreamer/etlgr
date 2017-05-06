# -*- coding: utf-8 -*-

from app.dict import KWDS
from app.dict import langs

class TestTranslations(object):
    def test_a_correct_type(self):
        assert type(KWDS) == dict

    def test_some_values(self):
        assert 'welcome' in KWDS['HI']['EN']
        langs = {
            'EN': u'English',
            'RU': u'Русский',
            'DE': u'Deutscher',
            'TR': u'Türkçe',
            'ES': u'Español',
        }

        for key in langs:
            assert langs[key] in KWDS[key + '_LANG'][key]

    def test_consistence(self):
        all_langs = langs.__all__
        en_lang = all_langs['EN']
        en_KWDS = en_lang.KWDS

        for kwd in en_KWDS:
            for lang in all_langs:
                assert kwd in all_langs[lang].KWDS

