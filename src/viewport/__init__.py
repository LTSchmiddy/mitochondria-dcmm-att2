import sys
import os
import threading
import math

import interface_flask

import webview as wv
from webview.platforms import cef as wv_cef
# from webview.platforms import qt as wv_qt

from cefpython3 import cefpython as cef

import viewport.js_api
import viewport.bg_tasks

from settings import current

p_gui = current['window']['web-engine']
# p_gui = 'cef'
# p_gui = 'qt'
p_http_server = False
p_debug = False


window: wv.window = None

def create_window(auto_load_ui: bool = True, window_name: str = "Mitochondria - Dead Cells Mod Manager"):
    global window

    load_addr = interface_flask.get_blank_addr()
    if auto_load_ui:
        load_addr = interface_flask.get_main_addr()

    window = wv.create_window(window_name, load_addr, js_api=js_api.JsApi())

    if p_gui != 'cef':
        if current['window']['x'] is not None:
            window.initial_x = current['window']['x']

        if current['window']['y'] is not None:
            window.initial_y = current['window']['y']

    if current['window']['width'] is not None:
        window.initial_width = current['window']['width']

    if current['window']['height'] is not None:
        window.initial_height = current['window']['height']

    window.loaded += on_loaded
    window.closing += on_window_closing
    window.closed += on_window_closed


# windowThread = None
window_is_alive = False

def start_window():
    global p_gui, p_http_server, p_debug, window, window_is_alive
    window_is_alive = True
    wv.start(viewport.bg_tasks.background_thread, window, gui=p_gui, debug=p_debug, http_server=p_http_server)
    # wv.start(debug=p_debug, http_server=p_http_server)

def confirm_prompt(message: str):
    global window
    return window.evaluate_js(f"window.confirm(`{message}`)")
    # return window.evaluate_js(f"console.log(`{message}`);")


def on_loaded():
    # pass
    js_api.process_js_bindings()

def on_window_closing():
    current['window']['x'] = window.x
    current['window']['y'] = window.y
    current['window']['width'] = window.width
    current['window']['height'] = window.height



def on_window_closed():
    global window, window_is_alive
    window_is_alive = False


def get_cef_instance() -> cef.PyBrowser:
    global window, window_is_alive

    if not window_is_alive:
        # print ("ERROR: Window is not active.")
        return None

    if current['window']['web-engine'] != 'cef':
        # print ("ERROR: Not using CEF Rendering.")
        return None

    if not 'master' in window.gui.CEF.instances:
        # print ("ERROR: CEF missing 'master' instance.")
        return None

    return window.gui.CEF.instances['master'].browser

def get_wv_cef_instance() -> wv_cef.Browser:
    global window, window_is_alive

    if not window_is_alive:
        # print ("ERROR: Window is not active.")
        return None

    if current['window']['web-engine'] != 'cef':
        # print ("ERROR: Not using CEF Rendering.")
        return None

    return window.gui.CEF.instances['master']

#
# def get_qt_instance() -> wv_qt.BrowserView:
#     global window, window_is_alive
#
#     if not window_is_alive:
#         print("ERROR: Window is not active.")
#         return None
#
#     if settings['window']['web-engine'] != 'qt':
#         print("ERROR: Not using qt Rendering.")
#         return None
#
#     return window.gui.BrowserView.instances['master']





# import webview.platforms.cef as wcef
# import webview.platforms.qt as wqt
from cefpython3 import cefpython as cef
#
# def get_cef_instances():
#     return wcef.instances
#
# def get_cef_master() -> wcef.Browser:
#     return wcef.instances['master']
#
# def get_cef_window() -> cef.PyBrowser:
#     return wcef.instances['master'].browser

# def get_qt_handle():
#     return int(wqt.BrowserView.instances['master'].videoframe.winId())

