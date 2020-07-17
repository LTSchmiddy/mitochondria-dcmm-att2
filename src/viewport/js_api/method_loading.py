import os
import json

from typing import Type

# import viewport
from data import pak_tools

from viewport.js_api import JsApi
import viewport


from viewport.js_api.modules import file, pak, std, mod_settings, save_info, dc_game


def create_api_modules(api: Type[JsApi]):
    create_base_module(api)
    pak.create_pak_module(api)
    file.create_files_module(api)
    std.create_std_module(api)
    mod_settings.create_settings_module(api)
    save_info.create_saves_module(api)
    dc_game.create_game_module(api)



def create_base_module(api: Type[JsApi]):
    # General Methods:
    def pyprint(self, msg):
        print(msg)

    def open_debug(self):
        browser = viewport.get_cef_instance()
        if browser is not None:
            browser.ShowDevTools()


    def close_debug(self):
        browser = viewport.get_cef_instance()
        if browser is not None:
            browser.CloseDevTools()

    def py_quit(self):
        # sys.exit(0)
        # interface_flask.stop_server()
        # viewport.end_window()
        viewport.window.destroy()

    # def py_exec(self, code: str, newline_marker: str = "; "): #, args=None):
    def py_exec(self, code: str): #, args=None):
        # if args is None:
        #     args = {}

        # if newline_marker != "" or newline_marker is not None:
        #     code = code.replace(newline_marker, "\n")

        exec("global retVal\n" + code)
        global retVal

        try:
            return retVal
        except NameError:
            return None

    def run_game():
        pass


    api.add_attr(pyprint, 'print')
    api.add_attr(open_debug)
    api.add_attr(close_debug)
    api.add_attr(py_quit, 'quit')
    api.add_attr(py_exec, 'exec')

