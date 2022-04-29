"""
responses.response_strings

By default, uses `english.json` file inside the `response_messages` responses folder.

If language changes, set `responses.response_strings.default_locale` and run `responses.response_strings.refresh()`.
"""
import os
import json

from api_university.config import api_dir

default_locale = "en"
cached_strings = {}
json_responses_dir = os.path.join(api_dir, "responses", "response_messages")
file_path = os.path.join(json_responses_dir, f"{default_locale}.json")


def refresh():
    print("Refreshing response strings...")
    global cached_strings
    with open(file_path) as f:
        cached_strings = json.load(f)


def gettext_(name):
    return cached_strings[name]


refresh()
