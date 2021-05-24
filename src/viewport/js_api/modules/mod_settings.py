import os
import json

from typing import Type

# import viewport
from data import pak_tools, std_handler

from viewport.js_api import JsApi
import viewport
import settings


def create_settings_module(api: Type[JsApi]):
    def get_current_settings(self):
        return settings.current

    def set_current_settings(self, new_settings):
        settings.current = new_settings

    def validate_settings(self):
        return settings.validate_settings()

    api.add_module_method_list("settings", [
        get_current_settings,
        set_current_settings,
        validate_settings
    ])