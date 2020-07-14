import sys
import os
import threading
import time
import shutil



import webview as wv
import viewport
from viewport.call_js import CallJS
import interface_flask

import settings
import settings.paths
from cefpython3 import cefpython as cef
from viewport.bg_tasks import bg_startup
from data import pak_tools, std_handler, saves, deadcells_game

import string

# update_seek_bar = CallJS("update-seek-bar.js")

cef_bound_properties = [
    'toolman__is_mproc_running',
    'std_handler__main_stdout',
    'std_handler__main_stdout_as_html',
    'game_man__is_game_detected'
]
# cef_run_props_thread = True

def background_thread(window: wv.window):
    # cef_props_thread = threading.Thread(None, target=update_js_properties, args=tuple([.5]))
    while viewport.get_cef_instance() is None:
        pass

    cef_props_thread = threading.Thread(None, target=update_js_properties_thread)
    cef_props_thread.start()

    bg_startup.run_startup(window)
    viewport.window.load_url(interface_flask.get_main_addr())

    cef_main = viewport.get_cef_instance()
    while viewport.window_is_alive:
        time.sleep(.5)
        saves.save_man.monitor_all_saves()
        deadcells_game.game_man.update()
        # update_js_properties()


# If the CEF window is going to be frequently checking a property or value,
# update that value here, using the CEF api, instead of the pywebview JS Bridge.
# performs much better, and prevents a number of bugs and errors.
def update_js_properties():
    cef_main = viewport.get_cef_instance()
    if cef_main is None:
        return

    bindings: cef.JavascriptBindings = cef_main.GetJavascriptBindings()

    bindings.SetProperty(cef_bound_properties[0], pak_tools.tool_man.is_mproc_all_running())
    bindings.SetProperty(cef_bound_properties[1], std_handler.my_stdout.get_all())
    bindings.SetProperty(cef_bound_properties[2], std_handler.my_stdout.get_html())
    bindings.SetProperty(cef_bound_properties[3], deadcells_game.game_man.is_game_detected())

    bindings.Rebind()

def update_js_properties_thread(freq: float = 0.5):
    while viewport.window_is_alive:
        update_js_properties()
        time.sleep(freq)