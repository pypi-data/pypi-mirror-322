# Transify: A Multi-Language Translator for Web Applications
Transify is a Python library designed for easy integration of multi-language translation functionality in web applications. It allows you to use custom translation files (in JSON format) for various languages and locales. This tool is ideal for web frameworks like FastAPI, Flask, or any other platform where dynamic translations are necessary.

## Features
- Multiple Language Support: Add and manage different languages by simply providing JSON files for each language.
- Dynamic Replacements: Supports dynamic replacements like variable insertion into translated strings.
- Nested Translation Keys: Allows translation via nested keys (e.g., captions.hello).
- Locale Switching: Switch between different locales on-the-fly.
- Works with Jinja2 Templates: Easily integrate with Jinja2 templates for real-time translations in your web pages.

## Installation
You can install transify via pip or poetry:

Using pip:
```bash
pip install transify
```
Using poetry:
```bash
poetry add transify
```
## Setting Up Translations
1. Create Language Folders: In your project, create a folder named lang to hold your translation files.

2. Add Translation Files: Inside the lang folder, create subdirectories for each language (e.g., en, fa) and add the respective translation JSON files.

Example structure:
```text
lang/
  en/
    captions.json
    messages.json
    validations.json
  fa/
    captions.json
    messages.json
    validations.json
  ...
```
## Example JSON Files
Below are examples of the translation files in JSON format:

captions.json
```json
{
  "name": "Azadjalal",
  "first_name": "First name",
  "hello": "Hello",
  "goodbye": "Goodbye",
  "username": "username",
  "good_score": "Good score"
}
```
messages.json
```json
{
  "welcome": "Welcome, :name to my website :website.",
  "errors": {
    "create": "Create item failed.",
    "user": {
      "not_found": "The user not found."
    }
  }
}
```
validations.json
```json
{
  "required": "The :attr is required.",
  "between": "The :attr must be between :min and :max values."
}
```
## Using Transify in a Project
Here’s an example of how you can integrate transify into a **FastAPI** project:
```python
import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from transify import *

app = FastAPI(title='transify', version='1.0.0')

# Mount static resources
app.mount(
    '/resources',
    StaticFiles(directory=f'{pathlib.Path(__file__).resolve().parent}/resources', html=False),
    name='static'
)

# Jinja2 template setup
templates = Jinja2Templates(
    directory=f'{pathlib.Path(__file__).resolve().parent}/resources'
)

# Update the template environment with the trans function
templates.env.globals.update(trans=trans)

def startup():
    load_languages(path='tests/lang', default_fallback='en')

app.add_event_handler('startup', startup)

@app.get('/', response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request, 'lang': get_locale()})

if __name__ == '__main__':
    uvicorn.run('test_webapp:app', host='localhost', port=8000, reload=True)
```

Then in your Jinja2 templates, you can use the translations like this:
```html
<!DOCTYPE html>
<html lang={{ lang }}>
    <head>
        <title>Transify Example</title>
    </head>
    <body>
        <!-- Example: Display translation for 'hello' -->
        <span>{{ trans('captions.hello') }}</span> <!-- Outputs: Hello -->
    </body>
    <footer>
        <!-- Example: Display translation for 'welcome' -->
        {{ trans('messages.welcome', 'name:Azadjalal|website:azadjalal.ir') }} <!-- Outputs: Welcome, Azadjalal to my website azadjalal.ir -->
    </footer>
</html>
```

## Functions and Methods

> load_languages(path: str = 'lang', default_fallback: str = 'en') 

oads translation files from the given path and sets up the languages. If a language file is missing, it falls back to the default_fallback language (usually 'en').

> set_locale(locale: str)

Sets the active locale to the desired language. For example, you can switch between "en" (English) and "fa" (Farsi) by calling:

```python
set_locale('fa')
```

> get_locale()

Returns the current active locale.

> trans(key: str, value: str = None)

This is the core translation function. It takes the key (e.g., captions.hello) and looks up the corresponding translation in the active language files. If a value is provided, it performs dynamic replacements.

- For simple translation:
```python
trans('captions.hello')  # Output: "Hello"
```

- For translations with dynamic replacements (using : syntax):
```python
trans('messages.welcome', value='name:Azadjalal|website:azadjalal.ir')  
# Output: "Welcome, Azadjalal to my website azadjalal.ir."
```

## Testing the Library
We have included a test_transify.py file to help you verify the functionality of the library. It uses Python’s unittest framework and covers various scenarios such as loading languages, setting locales, basic translations, dynamic replacements, and nested keys.

```bash
python test_transify.py
```

## Sample Test Cases in test_transify.py

1. Load Languages
Test if the languages are correctly loaded:

```python
self.assertIn('en', lang.languages)
self.assertIn('fa', lang.languages)
```

2. Set Locale
Test switching between locales:
```python
set_locale('fa')
self.assertEqual(get_locale(), 'fa')
set_locale('en')
```
3. Basic Translation
Test basic translations:
```python
self.assertEqual(trans('captions.hello'), 'Hello')
```

4. Dynamic Replacements
Test translations with dynamic replacements:
```python
self.assertEqual(
    trans('validations.between', value='score|min:1|max:20'),
    'The score must be between 1 and 20 values.'
)
```

5. Nested Keys
Test translations with nested keys:
```python
self.assertEqual(trans('messages.errors.user.not_found'), 'The user not found.')
```

6. Locale-Specific Translations
Test translations in different locales:
```python
set_locale('fa')
self.assertEqual(trans('captions.hello'), 'سلام')
```
## Error Handling
If a key is missing or there’s an error during the translation process, the library will log an error and return the original key as a fallback. For example:
```python
trans('messages.nonexistent')  # Returns 'messages.nonexistent'
```

## Customization
You can customize the load_languages function to load translations from any directory structure or path you prefer. This makes it easy to fit into different project setups.

## Conclusion
With transify, you can easily manage multi-language support in your web application, with simple setup, dynamic translations, and seamless integration into Jinja2 templates. Whether you’re working with FastAPI or another web framework, this library provides everything you need for language management.

