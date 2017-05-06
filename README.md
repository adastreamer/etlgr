# Common
This is a public part of source code of the Telegram Email Bot http://etlgr.com

# Requirements
- python 2.7

# Local development setup

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
Note that requirements.txt contains all the packages we're using in Etlgr project.
You may think that it's pretty much overkilled, but it isn't, we keep it to track our main repo being in up-to-date state according to this public part.
We have all other components available in this repo when they're test-covered.

# Translations
Feel free to add your translation file into the app/dict/langs folder.
There is no need to do anything else. The translation file is the only one thing that is required to add a new language.

## Scheme
The file format is pretty simple:

```python
# -*- coding: utf-8 -*-

LANG_KEY = u"EN"
LANG_NATIVE_NAME = u"English"

KWDS = {
    ... #
}
```

You may copy the EN.py file, rename it using some other unique name and then translate all the phrases.

## Testing
We use py.test, so to run tests, execute the following command:
```bash
py.test tests
```

## Workflow
1. Do a fork of this repo
1. Do all the necessary modifications
1. Run tests, be sure that everything is alright
1. Commit your changes
1. Do a pull request

# Credentials
http://etlgr.com, support by http://t.me/adastreamer
