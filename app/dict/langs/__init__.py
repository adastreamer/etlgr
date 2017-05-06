import os
import numpy

__all__ = {}
DEFAULT_LANG = 'EN'
LANG_POSTFIX = '_LANG'
KEY_PROPERTY = 'LANG_KEY'

# some helpers
def postfixed_lang(lang):
    return "{}{}".format(lang, LANG_POSTFIX)

# getting current directory
directory = os.path.dirname(os.path.abspath(__file__))

# going through the lang files list and do a dynamic import
for filename in os.listdir(directory):
    if (    filename.endswith('.py') and
        not filename.startswith('.') and
        not filename.startswith('_')
    ):
        module = os.path.splitext(filename)[0]
        exec("from . import {}".format(module))
        exec("__all__[{0}.{1}] = {0}".format(module, KEY_PROPERTY))

# define an initial state of lang keyboard elements
kbrd_langs = [
    DEFAULT_LANG,
]

# do an append of all the languages except the default one
for lang in (l for l in __all__ if l != DEFAULT_LANG):
    kbrd_langs.append(lang)

# all langs count
langs_count = len(kbrd_langs)

KEYBOARD = []

# if we have an odd number of languages,
# we place the first default language on the whole keyboard row
if langs_count % 2:
    KEYBOARD.append(
        [
            postfixed_lang(kbrd_langs[0])
        ]
    )
    kbrd_langs.remove(kbrd_langs[0])

# here we have all the remain languages if the previous condition is reached
# we need to reshape the array of the languages to 2-dimentional array
remain_languages = numpy.reshape(kbrd_langs, (-1, 2))

# append all the remain languages to the KEYBOARD variable
# as a 2-cols row each pair
for lang_line in remain_languages:
    KEYBOARD.append([
        postfixed_lang(lang_line[0]),
        postfixed_lang(lang_line[1]),
    ])

