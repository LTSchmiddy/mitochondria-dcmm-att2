import sys
import os
import threading
import time
import shutil

import webview as wv
import viewport
import interface_flask

import settings
import settings.paths
from cefpython3 import cefpython as cef
from viewport.bg_tasks import bg_startup
from data import pak_tools, std_handler, saves, deadcells_game

cef_bound_properties = [
    ('toolman__is_mproc_running', pak_tools.tool_man.is_mproc_all_running),
    ('std_handler__main_stdout', std_handler.my_stdout.get_all),
    ('std_handler__main_stdout_as_html', std_handler.my_stdout.get_html),
    ('game_man__is_game_detected', deadcells_game.game_man.is_game_detected),
    ('lambda_test', lambda: saves.save_man.last_mtimes)
]


# If the CEF window is going to be frequently checking a property or value,
# update that value here, using the CEF api, instead of the pywebview JS Bridge.
# performs much better, and prevents a number of bugs and errors.
def update_cef_properties():
    global cef_bound_properties

    cef_main = viewport.get_cef_instance()
    if cef_main is None:
        return

    bindings: cef.JavascriptBindings = cef_main.GetJavascriptBindings()
    for i in cef_bound_properties:
        bindings.SetProperty(i[0], i[1]())
    bindings.Rebind()


# Currently Experimental:
def declare_cef_callbacks():


    cef_main = viewport.get_cef_instance()
    if cef_main is None:
        return
    bindings: cef.JavascriptBindings = cef_main.GetJavascriptBindings()
    def callback_test(test_param: cef.JavascriptCallback):
        print(test_param)
        print(test_param.GetName())
        print(test_param.GetFrame())
        print(test_param.GetFunctionName())

        # for i in dir(test_param):
        #     print(i)


        test_param.Call()

    bindings.SetFunction("callback_test", callback_test)


    bindings.Rebind()


