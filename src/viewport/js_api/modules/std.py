import os
import json

from typing import Type

# import viewport
from data import pak_tools, std_handler

from viewport.js_api import JsApi
import viewport
import mitochondria


def create_std_module(api: Type[JsApi]):
    def get_stdout(self):
        # return std_handler.my_stdout.get_all().replace("\n", "\n<br/>")
        return std_handler.my_stdout.get_all()

    api.add_module_method_list("std", [get_stdout])